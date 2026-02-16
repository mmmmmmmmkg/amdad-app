from app.models import Post
from app.services.scheduler import PublishingScheduler


class _FakeFacebookSuccess:
    def publish_post(self, message: str) -> str:
        return "123_456"

    def fetch_post_insights(self, post_id: str) -> dict:
        return {"data": [{"name": "post_impressions", "values": [{"value": 10}]}]}


class _FakeFacebookFailure:
    def publish_post(self, message: str) -> str:
        raise RuntimeError("temporary facebook outage")



def test_publish_one_post_success_updates_post_fields():
    scheduler = PublishingScheduler()
    scheduler.facebook = _FakeFacebookSuccess()

    post = Post(project_id=1, title="t", body="b", status="scheduled", publish_attempts=0)
    scheduler.publish_one_post(None, post)  # type: ignore[arg-type]

    assert post.status == "published"
    assert post.facebook_post_id == "123_456"
    assert post.publish_attempts == 1
    assert post.last_error is None



def test_publish_one_post_failure_marks_failed():
    scheduler = PublishingScheduler()
    scheduler.facebook = _FakeFacebookFailure()

    post = Post(project_id=1, title="t", body="b", status="scheduled", publish_attempts=1)
    scheduler.publish_one_post(None, post)  # type: ignore[arg-type]

    assert post.status == "failed"
    assert post.publish_attempts == 2
    assert "temporary facebook outage" in (post.last_error or "")
