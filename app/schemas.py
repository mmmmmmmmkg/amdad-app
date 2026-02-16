from datetime import datetime

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2)
    business_type: str
    region: str
    target_audience: str
    goals: str


class ProjectRead(ProjectCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class PostCreate(BaseModel):
    title: str
    body: str
    scheduled_for: datetime | None = None


class PostRead(BaseModel):
    id: int
    project_id: int
    title: str
    body: str
    status: str
    scheduled_for: datetime | None
    facebook_post_id: str | None
    publish_attempts: int
    last_error: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StrategyResponse(BaseModel):
    project_id: int
    monthly_objective: str
    pillars: list[str]
    weekly_plan: list[dict[str, str]]


class MarketAnalysisResponse(BaseModel):
    project_id: int
    competitor_signals: list[str]
    winning_patterns: list[str]
    opportunity_gaps: list[str]


class AudienceAnalysisResponse(BaseModel):
    project_id: int
    segments: list[dict[str, str]]
    content_preferences: list[str]
    best_posting_slots: list[str]
    messaging_style: str


class AutopilotRunRequest(BaseModel):
    days: int = Field(default=7, ge=1, le=30)
    posts_per_day: int = Field(default=1, ge=1, le=4)
    start_at: datetime | None = None


class AutopilotRunResponse(BaseModel):
    project_id: int
    strategy: StrategyResponse
    market_analysis: MarketAnalysisResponse
    audience_analysis: AudienceAnalysisResponse
    scheduled_posts_count: int
    scheduled_post_ids: list[int]


class KpiSummaryResponse(BaseModel):
    project_id: int
    total_posts: int
    published_posts: int
    scheduled_posts: int
    total_impressions: int
    total_engaged_users: int
