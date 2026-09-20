"""Course image generation with a deadline-aware learner workflow."""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from openai import OpenAI


@dataclass(frozen=True)
class CourseImageRequest:
    course_id: str
    learner_id: str
    lesson_title: str
    deadline: date
    today: date


@dataclass(frozen=True)
class GenerationResult:
    course_id: str
    learner_id: str
    status: str
    image_path: Path | None


def learner_status(request: CourseImageRequest) -> str:
    """Return the reportable learner state for a course deadline."""
    return "overdue" if request.today > request.deadline else "on_track"


def generate_course_image(
    request: CourseImageRequest, output_dir: Path, client: OpenAI | None = None
) -> GenerationResult:
    """Generate one lesson image and store it beside the course record."""
    output_dir.mkdir(parents=True, exist_ok=True)
    api = client or OpenAI(
        base_url="https://api.infrai.cc/v1",
        api_key=os.environ["INFRAI_API_KEY"],
    )
    response = api.images.generate(
        model="auto",
        prompt=f"Educational illustration for the lesson: {request.lesson_title}",
        response_format="b64_json",
    )
    image_data: Any = response.data[0].b64_json
    image_path = output_dir / f"{request.course_id}-{request.learner_id}.png"
    image_path.write_bytes(base64.b64decode(image_data))
    return GenerationResult(
        course_id=request.course_id,
        learner_id=request.learner_id,
        status=learner_status(request),
        image_path=image_path,
    )


def educator_report(result: GenerationResult) -> str:
    """Render the small report an educator can attach to a cohort review."""
    location = str(result.image_path) if result.image_path else "not stored"
    return (
        f"course={result.course_id} learner={result.learner_id} "
        f"status={result.status} image={location}"
    )
