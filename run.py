import argparse
from datetime import date
from pathlib import Path

from src.edtech_image_service import CourseImageRequest, educator_report, generate_course_image


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and store one course image.")
    parser.add_argument("--course", required=True)
    parser.add_argument("--learner", required=True)
    parser.add_argument("--lesson", required=True)
    parser.add_argument("--deadline", required=True, type=date.fromisoformat)
    parser.add_argument("--output", type=Path, default=Path("generated-images"))
    args = parser.parse_args()
    request = CourseImageRequest(
        course_id=args.course,
        learner_id=args.learner,
        lesson_title=args.lesson,
        deadline=args.deadline,
        today=date.today(),
    )
    result = generate_course_image(request, args.output)
    print(educator_report(result))


if __name__ == "__main__":
    main()
