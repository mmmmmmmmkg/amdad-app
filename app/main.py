from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal, init_db
from app.services.analytics import AnalyticsService
from app.services.autopilot import AutopilotService
from app.services.content_generator import ContentGenerator
from app.services.intelligence import AudienceIntelligenceService, MarketIntelligenceService
from app.services.planner import StrategyPlanner
from app.services.scheduler import PublishingScheduler

planner = StrategyPlanner()
content_generator = ContentGenerator()
market_intelligence = MarketIntelligenceService()
audience_intelligence = AudienceIntelligenceService()
autopilot = AutopilotService()
analytics = AnalyticsService()
scheduler = PublishingScheduler()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown()


app = FastAPI(title="Amdad Facebook Marketing System", version="1.2.0", lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "time": datetime.utcnow().isoformat(),
        "scheduler_running": scheduler.scheduler.running,
        "facebook_configured": scheduler.facebook.is_configured(),
    }


@app.post("/projects", response_model=schemas.ProjectRead)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, payload)


@app.get("/projects", response_model=list[schemas.ProjectRead])
def get_projects(db: Session = Depends(get_db)):
    return crud.list_projects(db)


@app.get("/projects/{project_id}/strategy", response_model=schemas.StrategyResponse)
def get_strategy(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return planner.generate_strategy(project)


@app.get("/projects/{project_id}/market-analysis", response_model=schemas.MarketAnalysisResponse)
def get_market_analysis(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return market_intelligence.analyze_market(project)


@app.get("/projects/{project_id}/audience-analysis", response_model=schemas.AudienceAnalysisResponse)
def get_audience_analysis(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return audience_intelligence.analyze_audience(project)


@app.post("/projects/{project_id}/autopilot/run", response_model=schemas.AutopilotRunResponse)
def run_autopilot(project_id: int, payload: schemas.AutopilotRunRequest, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return autopilot.run(db, project, payload)


@app.post("/projects/{project_id}/posts/generate", response_model=schemas.PostRead)
def generate_post(project_id: int, angle: str, schedule_at: datetime | None = None, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    generated = content_generator.generate_post(project, angle)
    payload = schemas.PostCreate(title=generated["title"], body=generated["body"], scheduled_for=schedule_at)
    created = crud.create_post(db, project_id, payload)

    if schedule_at:
        created.status = "scheduled"
        db.commit()
        db.refresh(created)

    return created


@app.post("/projects/{project_id}/posts", response_model=schemas.PostRead)
def create_post(project_id: int, payload: schemas.PostCreate, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    created = crud.create_post(db, project_id, payload)
    if payload.scheduled_for:
        created.status = "scheduled"
        db.commit()
        db.refresh(created)
    return created


@app.post("/projects/{project_id}/posts/{post_id}/publish-now", response_model=schemas.PostRead)
def publish_now(project_id: int, post_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    post = crud.get_post(db, post_id)
    if not post or post.project_id != project_id:
        raise HTTPException(status_code=404, detail="Post not found")

    scheduler.publish_one_post(db, post)
    db.commit()
    db.refresh(post)
    return post


@app.get("/projects/{project_id}/posts", response_model=list[schemas.PostRead])
def list_posts(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.list_project_posts(db, project_id)


@app.get("/projects/{project_id}/kpis", response_model=schemas.KpiSummaryResponse)
def get_project_kpis(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    posts = crud.list_project_posts(db, project_id)
    summary = analytics.summarize_posts(posts)
    return schemas.KpiSummaryResponse(project_id=project_id, **summary.__dict__)
