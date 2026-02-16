from app.models import Project


class StrategyPlanner:
    def generate_strategy(self, project: Project) -> dict:
        objective = f"رفع نتائج {project.name} في سوق {project.region} خلال 30 يوم"
        pillars = [
            "محتوى تعليمي يجاوب أسئلة العملاء",
            "محتوى ثقة (قصص نجاح/آراء عملاء)",
            "محتوى عروض مباشر للتحويل",
        ]
        weekly_plan = [
            {"week": "1", "focus": "تعريف بالعلامة + بناء الثقة"},
            {"week": "2", "focus": "حل مشاكل الجمهور بمحتوى تعليمي"},
            {"week": "3", "focus": "دفع التحويل بعروض قوية"},
            {"week": "4", "focus": "إعادة استهداف المحتوى الأعلى تفاعلاً"},
        ]
        return {
            "project_id": project.id,
            "monthly_objective": objective,
            "pillars": pillars,
            "weekly_plan": weekly_plan,
        }
