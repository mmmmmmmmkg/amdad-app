import json

import httpx

from app.config import get_settings
from app.models import Project

settings = get_settings()


class ContentGenerator:
    def generate_post(self, project: Project, angle: str) -> dict[str, str]:
        if settings.openai_api_key:
            return self._generate_with_openai(project, angle)
        return self._fallback_post(project, angle)

    def _fallback_post(self, project: Project, angle: str) -> dict[str, str]:
        title = f"{project.name} | {angle}"
        body = (
            f"لو أنت من {project.target_audience}، فهذه الرسالة لك.\n"
            f"نساعدك في {project.business_type} داخل {project.region}.\n"
            f"هدفنا: {project.goals}.\n"
            "راسلنا الآن لمعرفة أفضل عرض مناسب لك."
        )
        return {"title": title, "body": body}

    def _generate_with_openai(self, project: Project, angle: str) -> dict[str, str]:
        prompt = (
            "اكتب منشور فيسبوك عربي احترافي بصيغة JSON يحتوي title و body فقط. "
            f"النشاط: {project.business_type}. الجمهور: {project.target_audience}. "
            f"المنطقة: {project.region}. الهدف التسويقي: {project.goals}. زاوية المحتوى: {angle}."
        )
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.openai_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
        with httpx.Client(timeout=40) as client:
            resp = client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return {"title": parsed["title"], "body": parsed["body"]}
