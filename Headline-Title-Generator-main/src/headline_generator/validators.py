from difflib import SequenceMatcher
import re
from typing import Any


class ValidationError(ValueError):
    """Raised when generated title and headline records are invalid."""


def validate_headline_records(records: list[Any]) -> list[dict[str, Any]]:
    if not isinstance(records, list):
        raise ValidationError("The AI response must contain a JSON list.")
    if len(records) != 10:
        raise ValidationError(
            f"Expected exactly 10 title and headline pairs, but received {len(records)}."
        )

    validated: list[dict[str, Any]] = []
    seen_titles: set[str] = set()
    seen_headlines: set[str] = set()
    required_fields = {"title", "headline", "clarity_score"}

    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValidationError(
                f"Title and headline record {index} is not a valid object."
            )
        if set(record) != required_fields:
            missing = required_fields - set(record)
            extra = set(record) - required_fields
            details = []
            if missing:
                details.append(f"missing {', '.join(sorted(missing))}")
            if extra:
                details.append(f"unexpected {', '.join(sorted(extra))}")
            raise ValidationError(
                f"Record {index} must contain only title, headline, and "
                f"clarity_score ({'; '.join(details)})."
            )

        title = record.get("title")
        headline = record.get("headline")
        score = record.get("clarity_score")

        if not isinstance(title, str) or not title.strip():
            raise ValidationError(
                f"Title for record {index} is empty or missing."
            )
        if not isinstance(headline, str) or not headline.strip():
            raise ValidationError(
                f"Headline record {index} has an empty or missing headline."
            )

        normalized_title = re.sub(r"[^\w]+", " ", title.strip().casefold()).strip()
        normalized_headline = re.sub(
            r"[^\w]+", " ", headline.strip().casefold()
        ).strip()
        if normalized_title in seen_titles:
            raise ValidationError("Duplicate article titles were found.")
        if normalized_headline in seen_headlines:
            raise ValidationError("Duplicate headlines were found.")
        if (
            normalized_title == normalized_headline
            or SequenceMatcher(None, normalized_title, normalized_headline).ratio()
            >= 0.9
        ):
            raise ValidationError(
                f"The title and headline in record {index} are too similar. "
                "Each pair must be meaningfully different."
            )
        seen_titles.add(normalized_title)
        seen_headlines.add(normalized_headline)

        if isinstance(score, bool) or not isinstance(score, int):
            raise ValidationError(
                f"Clarity score for headline {index} must be an integer from 1 to 10."
            )
        if not 1 <= score <= 10:
            raise ValidationError(
                f"Clarity score for headline {index} must be between 1 and 10."
            )

        validated.append(
            {
                "title": title.strip(),
                "headline": headline.strip(),
                "clarity_score": score,
            }
        )

    return validated


def sort_headlines(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        records,
        key=lambda record: record["clarity_score"],
        reverse=True,
    )
