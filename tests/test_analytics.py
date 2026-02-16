from app.models import Post
from app.services.analytics import AnalyticsService


def test_kpi_summary_aggregates_metrics():
    posts = [
        Post(status="published", insights_json='{"data":[{"name":"post_impressions","values":[{"value":100}]},{"name":"post_engaged_users","values":[{"value":15}]}]}'),
        Post(status="published", insights_json='{"data":[{"name":"post_impressions","values":[{"value":50}]},{"name":"post_engaged_users","values":[{"value":5}]}]}'),
        Post(status="scheduled", insights_json=None),
    ]

    summary = AnalyticsService().summarize_posts(posts)

    assert summary.total_posts == 3
    assert summary.published_posts == 2
    assert summary.scheduled_posts == 1
    assert summary.total_impressions == 150
    assert summary.total_engaged_users == 20
