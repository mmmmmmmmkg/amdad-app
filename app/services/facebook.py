import time

import httpx

from app.config import get_settings

settings = get_settings()


class FacebookService:
    def _base_url(self) -> str:
        return f"https://graph.facebook.com/{settings.fb_graph_version}"

    def is_configured(self) -> bool:
        return bool(settings.fb_page_id and settings.fb_page_access_token)

    def publish_post(self, message: str) -> str:
        if not self.is_configured():
            raise RuntimeError("Facebook credentials are missing. Add them to .env first.")

        url = f"{self._base_url()}/{settings.fb_page_id}/feed"
        data = {"message": message, "access_token": settings.fb_page_access_token}
        payload = self._request_with_retry("POST", url, data=data)
        return payload["id"]

    def fetch_post_insights(self, post_id: str) -> dict:
        if not self.is_configured():
            raise RuntimeError("Facebook credentials are missing. Add them to .env first.")

        metrics = "post_impressions,post_engaged_users,post_reactions_by_type_total"
        url = f"{self._base_url()}/{post_id}/insights"
        params = {"metric": metrics, "access_token": settings.fb_page_access_token}
        return self._request_with_retry("GET", url, params=params)

    def _request_with_retry(self, method: str, url: str, **kwargs) -> dict:
        last_error: Exception | None = None
        for attempt in range(1, settings.publish_retry_attempts + 1):
            try:
                with httpx.Client(timeout=30) as client:
                    response = client.request(method, url, **kwargs)
                    response.raise_for_status()
                    return response.json()
            except Exception as error:
                last_error = error
                if attempt < settings.publish_retry_attempts:
                    time.sleep(0.6 * attempt)

        raise RuntimeError(f"Facebook request failed after {settings.publish_retry_attempts} attempts") from last_error
