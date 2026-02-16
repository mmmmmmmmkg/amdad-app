from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app import crud, schemas
from app.models import Project
from app.services.content_generator import ContentGenerator
from app.services.intelligence import AudienceIntelligenceService, MarketIntelligenceService
from app.services.planner import StrategyPlanner


class AutopilotService:
    def __init__(self) -> None:
        self.strategy_planner = StrategyPlanner()
        self.content_generator = ContentGenerator()
        self.market_intelligence = MarketIntelligenceService()
        self.audience_intelligence = AudienceIntelligenceService()

    def run(self, db: Session, project: Project, request: schemas.AutopilotRunRequest) -> schemas.AutopilotRunResponse:
        strategy_data = self.strategy_planner.generate_strategy(project)
        market_data = self.market_intelligence.analyze_market(project)
        audience_data = self.audience_intelligence.analyze_audience(project)

        start = request.start_at or datetime.utcnow()
        slots = audience_data["best_posting_slots"]

        created_ids: list[int] = []
        for day in range(request.days):
            for post_number in range(request.posts_per_day):
                slot = slots[(day + post_number) % len(slots)]
                hour, minute = [int(part) for part in slot.split(":")]
                scheduled_for = (start + timedelta(days=day)).replace(hour=hour, minute=minute, second=0, microsecond=0)

                angle = self._resolve_angle(day, post_number, strategy_data["pillars"])
                generated = self.content_generator.generate_post(project, angle)
                payload = schemas.PostCreate(
                    title=generated["title"],
                    body=generated["body"],
                    scheduled_for=scheduled_for,
                )
                post = crud.create_post(db, project.id, payload)
                post.status = "scheduled"
                db.commit()
                db.refresh(post)
                created_ids.append(post.id)

        return schemas.AutopilotRunResponse(
            project_id=project.id,
            strategy=schemas.StrategyResponse(**strategy_data),
            market_analysis=schemas.MarketAnalysisResponse(**market_data),
            audience_analysis=schemas.AudienceAnalysisResponse(**audience_data),
            scheduled_posts_count=len(created_ids),
            scheduled_post_ids=created_ids,
        )

    @staticmethod
    def _resolve_angle(day: int, post_number: int, pillars: list[str]) -> str:
        return pillars[(day + post_number) % len(pillars)]
