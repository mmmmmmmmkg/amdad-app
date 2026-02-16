from app.models import Project
from app.services.intelligence import AudienceIntelligenceService, MarketIntelligenceService


def test_market_analysis_returns_expected_shape():
    project = Project(
        id=11,
        name="عيادة",
        business_type="خدمات طبية",
        region="السعودية",
        target_audience="العائلات",
        goals="زيادة الحجوزات",
    )
    service = MarketIntelligenceService()

    result = service.analyze_market(project)

    assert result["project_id"] == 11
    assert len(result["competitor_signals"]) >= 3
    assert len(result["winning_patterns"]) >= 3
    assert len(result["opportunity_gaps"]) >= 3


def test_audience_analysis_has_slots_and_segments():
    project = Project(
        id=12,
        name="متجر",
        business_type="إكسسوارات",
        region="مصر",
        target_audience="نساء 20-35",
        goals="زيادة الطلبات",
    )
    service = AudienceIntelligenceService()

    result = service.analyze_audience(project)

    assert result["project_id"] == 12
    assert len(result["segments"]) == 3
    assert len(result["best_posting_slots"]) == 3
