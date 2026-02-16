from app.models import Project
from app.services.planner import StrategyPlanner


def test_generate_strategy_contains_project_id():
    project = Project(
        id=7,
        name="متجر ألف",
        business_type="ملابس",
        region="مصر",
        target_audience="شباب 18-30",
        goals="زيادة المبيعات",
    )
    planner = StrategyPlanner()

    strategy = planner.generate_strategy(project)

    assert strategy["project_id"] == 7
    assert len(strategy["pillars"]) == 3
    assert len(strategy["weekly_plan"]) == 4
