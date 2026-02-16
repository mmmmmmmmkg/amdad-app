import json
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.config import get_settings
from app.crud import list_due_posts
from app.database import SessionLocal
from app.models import Post
from app.services.facebook import FacebookService

settings = get_settings()


class PublishingScheduler:
    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler()
        self.facebook = FacebookService()

    def start(self) -> None:
        if self.scheduler.running:
            return
        self.scheduler.add_job(
            self.publish_due_posts,
            "interval",
            seconds=settings.scheduler_interval_seconds,
            id="publish_due_posts",
            replace_existing=True,
        )
        self.scheduler.start()

    def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)

    def publish_due_posts(self) -> None:
        if not self.facebook.is_configured():
            return

        now = datetime.utcnow()
        with SessionLocal() as db:
            due_posts = list_due_posts(db, now)
            for post in due_posts:
                self.publish_one_post(db, post)
            db.commit()

    def publish_one_post(self, db: Session, post: Post) -> None:
        post.publish_attempts = (post.publish_attempts or 0) + 1

        try:
            fb_id = self.facebook.publish_post(post.body)
            post.facebook_post_id = fb_id
            post.status = "published"
            post.last_error = None
            try:
                insights = self.facebook.fetch_post_insights(fb_id)
                post.insights_json = json.dumps(insights, ensure_ascii=False)
            except Exception as error:
                post.insights_json = None
                post.last_error = f"insights_error: {error}"
        except Exception as error:
            post.status = "failed"
            post.last_error = str(error)
