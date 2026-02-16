from app.models import Project


class MarketIntelligenceService:
    """Lightweight intelligence module focused on practical planning inputs.

    This intentionally avoids fragile scraping dependencies and derives
    actionable signals from project context.
    """

    def analyze_market(self, project: Project) -> dict:
        competitors = [
            f"{project.business_type} محلي في {project.region}",
            f"علامات رقمية تقدم {project.business_type} بعروض قوية",
            "متاجر تعتمد فيديو قصير + CTA مباشر",
        ]
        winning_patterns = [
            "محتوى قبل/بعد يوضح النتيجة",
            "عروض محددة بزمن واضح",
            "قصص وتجارب عملاء حقيقية",
        ]
        gaps = [
            "ضعف الاستمرارية في المحتوى التعليمي",
            "قلة الرسائل الموجهة لكل شريحة جمهور",
            "عدم استغلال إعادة النشر للمحتوى الأعلى أداء",
        ]
        return {
            "project_id": project.id,
            "competitor_signals": competitors,
            "winning_patterns": winning_patterns,
            "opportunity_gaps": gaps,
        }


class AudienceIntelligenceService:
    def analyze_audience(self, project: Project) -> dict:
        best_posting_slots = ["11:00", "17:00", "21:00"]
        content_preferences = ["تعليمي مختصر", "شهادات عملاء", "عرض مباشر مع CTA"]
        messaging_style = "لهجة عربية واضحة، نبرة ودّية، تركيز على نتيجة عملية"

        return {
            "project_id": project.id,
            "segments": [
                {"name": "مهتم جديد", "need": "فهم القيمة بسرعة", "format": "بوست تعليمي"},
                {"name": "متردد", "need": "ثقة", "format": "قصة عميل"},
                {"name": "جاهز للشراء", "need": "عرض واضح", "format": "بوست عرض"},
            ],
            "content_preferences": content_preferences,
            "best_posting_slots": best_posting_slots,
            "messaging_style": messaging_style,
        }
