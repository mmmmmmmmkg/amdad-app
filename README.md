# Amdad App - Facebook Autonomous Marketing System

نظام تسويق ذكي احترافي يركز على Facebook مع أتمتة كاملة: تحليل، تخطيط، توليد، جدولة، نشر، وقياس.

## أهم التطويرات الاحترافية المضافة

- Autopilot كامل لإنشاء خطة نشر تلقائية.
- تحليل سوق + تحليل جمهور.
- نشر مجدول مع retry logic عند فشل الاتصال بـ Facebook.
- تتبع `publish_attempts` و `last_error` لكل منشور.
- endpoint نشر فوري `publish-now` لأي منشور.
- endpoint KPI ملخص لأداء المشروع.
- health endpoint يعرض حالة scheduler وهل مفاتيح Facebook مضبوطة.

## التشغيل

```bash
python -m pip install -e '.[dev]'
cp .env.example .env
python -m uvicorn app.main:app --reload
```

## الإعداد (`.env`)

```env
APP_ENV=development
DATABASE_URL=sqlite:///./amdad.db
TIMEZONE=Africa/Cairo

SCHEDULER_INTERVAL_SECONDS=60
PUBLISH_RETRY_ATTEMPTS=3

FB_PAGE_ID=your_page_id
FB_PAGE_ACCESS_TOKEN=your_page_access_token
FB_GRAPH_VERSION=v20.0

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```

## أهم الـ API

- `GET /health`
- `POST /projects`
- `GET /projects`
- `GET /projects/{project_id}/strategy`
- `GET /projects/{project_id}/market-analysis`
- `GET /projects/{project_id}/audience-analysis`
- `POST /projects/{project_id}/autopilot/run`
- `POST /projects/{project_id}/posts/generate?angle=...&schedule_at=...`
- `POST /projects/{project_id}/posts/{post_id}/publish-now`
- `GET /projects/{project_id}/posts`
- `GET /projects/{project_id}/kpis`

## مثال تطوير مستقبلي إضافي

- A/B testing تلقائي.
- queue production-grade (Celery/Redis).
- multi-tenant roles & permissions.
- dashboard React لإدارة العملاء والحملات.
