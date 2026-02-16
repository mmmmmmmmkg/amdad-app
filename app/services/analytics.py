import json
from dataclasses import dataclass

from app.models import Post


@dataclass
class KpiSummary:
    total_posts: int
    published_posts: int
    scheduled_posts: int
    total_impressions: int
    total_engaged_users: int


class AnalyticsService:
    def summarize_posts(self, posts: list[Post]) -> KpiSummary:
        published = 0
        scheduled = 0
        impressions = 0
        engaged = 0

        for post in posts:
            if post.status == "published":
                published += 1
            if post.status == "scheduled":
                scheduled += 1

            if not post.insights_json:
                continue

            try:
                raw = json.loads(post.insights_json)
            except json.JSONDecodeError:
                continue

            for item in raw.get("data", []):
                metric = item.get("name")
                values = item.get("values", [])
                value = 0
                if values:
                    value = values[0].get("value", 0)

                if metric == "post_impressions" and isinstance(value, int):
                    impressions += value
                if metric == "post_engaged_users" and isinstance(value, int):
                    engaged += value

        return KpiSummary(
            total_posts=len(posts),
            published_posts=published,
            scheduled_posts=scheduled,
            total_impressions=impressions,
            total_engaged_users=engaged,
        )
