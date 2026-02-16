from app.services.autopilot import AutopilotService


def test_resolve_angle_rotates_over_pillars():
    pillars = ["A", "B", "C"]

    angle_0 = AutopilotService._resolve_angle(0, 0, pillars)
    angle_1 = AutopilotService._resolve_angle(0, 1, pillars)
    angle_2 = AutopilotService._resolve_angle(1, 1, pillars)

    assert angle_0 == "A"
    assert angle_1 == "B"
    assert angle_2 == "C"
