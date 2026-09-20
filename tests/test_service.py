from datetime import date

from src.edtech_image_service import CourseImageRequest, learner_status


def test_deadline_decision_marks_late_learner_overdue() -> None:
    request = CourseImageRequest(
        course_id="anatomy-101",
        learner_id="learner-7",
        lesson_title="Heart valves",
        deadline=date(2026, 9, 8),
        today=date(2026, 9, 9),
    )

    assert learner_status(request) == "overdue"
