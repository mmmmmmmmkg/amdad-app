from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Post, Project
from app.schemas import PostCreate, ProjectCreate


def create_project(db: Session, payload: ProjectCreate) -> Project:
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def list_projects(db: Session) -> list[Project]:
    return list(db.scalars(select(Project).order_by(Project.created_at.desc())))


def get_project(db: Session, project_id: int) -> Project | None:
    return db.get(Project, project_id)


def create_post(db: Session, project_id: int, payload: PostCreate) -> Post:
    post = Post(project_id=project_id, **payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_post(db: Session, post_id: int) -> Post | None:
    return db.get(Post, post_id)


def list_project_posts(db: Session, project_id: int) -> list[Post]:
    stmt = select(Post).where(Post.project_id == project_id).order_by(Post.created_at.desc())
    return list(db.scalars(stmt))


def list_due_posts(db: Session, now: datetime) -> list[Post]:
    stmt = (
        select(Post)
        .where(Post.status == "scheduled")
        .where(Post.scheduled_for.is_not(None))
        .where(Post.scheduled_for <= now)
    )
    return list(db.scalars(stmt))
