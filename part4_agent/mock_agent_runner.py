import csv
import json
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from part2_engine.growth_engine import validate_feed, mom_growth, is_flagged



MONTH_ORDER = ["April", "May", "June", "July"]


def load_feed(csv_path: str) -> list[dict]:
    """Load a CSV revenue feed."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def previous_month(month: str) -> str:
    """Return the previous month used by the agent."""
    index = MONTH_ORDER.index(month)
    if index == 0:
        raise ValueError("April does not have a previous month in this project.")
    return MONTH_ORDER[index - 1]


def revenue_by_category(rows: list[dict], month: str) -> dict[str, float]:
    """Create category -> revenue mapping for one month."""
    result = {}

    for row in rows:
        if row.get("month") == month:
            result[row["category"]] = round(float(row["revenue"]), 2)

    return result


def fill_prompt_template(
    category: str,
    previous_revenue: float,
    current_revenue: float,
    mom_pct: float,
    month: str,
    prev_month: str,
) -> str:
    """
    Part 3 prompt-pack template-fill logic.

    Every number in the drafted message comes from the supplied
    Part 1 / Part 2 values.
    """
    return (
        f"Context: {category} revenue is being compared for "
        f"{month} vs. {prev_month}. "
        f"Insight: Fact — {category} revenue moved from "
        f"INR {previous_revenue} in {prev_month} to "
        f"INR {current_revenue} in {month}, representing an exact "
        f"month-on-month movement of {mom_pct}%. "
        f"Implication: Hypothesis — the movement may reflect a change "
        f"in demand or reseller activity. The regional manager should "
        f"review recent category performance and reseller activity "
        f"before deciding on corrective action."
    )


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    """Run the guarded Meesho monitoring agent."""

    prev_month = previous_month(month)

    # ---------------------------------------------------------
    # 1. Load the current feed and validate it first.
    # ---------------------------------------------------------
    current_rows = load_feed(current_month_csv)

    valid, errors = validate_feed(current_month_csv)

    # ---------------------------------------------------------
    # 2. Hard Stop if validation fails.
    # ---------------------------------------------------------
    if not valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

    # Load previous feed only after current validation succeeds.
    previous_rows = load_feed(previous_month_csv)

    previous_revenue = revenue_by_category(previous_rows, prev_month)
    current_revenue = revenue_by_category(current_rows, month)

    # ---------------------------------------------------------
    # 3 & 4. Calculate MoM and classify every category.
    # ---------------------------------------------------------
    flagged = []
    escalated = []

    for category in current_revenue:
        if category not in previous_revenue:
            continue

        previous_value = previous_revenue[category]
        current_value = current_revenue[category]

        growth = mom_growth(previous_value, current_value)
        flag_status = is_flagged(growth)

        if flag_status == "flagged":
            flagged.append(
                {
                    "category": category,
                    "mom_pct": growth,
                    "previous_revenue": previous_value,
                    "current_revenue": current_value,
                }
            )

        elif flag_status == "escalate_exact_boundary":
            escalated.append(category)

    # ---------------------------------------------------------
    # 5. Sort flagged categories by absolute MoM magnitude.
    # ---------------------------------------------------------
    flagged.sort(key=lambda item: abs(item["mom_pct"]), reverse=True)

    # ---------------------------------------------------------
    # 6. Draft messages for only the top 3.
    # ---------------------------------------------------------
    top_three = flagged[:3]

    for item in top_three:
        item["drafted"] = True
        item["message"] = fill_prompt_template(
            category=item["category"],
            previous_revenue=item["previous_revenue"],
            current_revenue=item["current_revenue"],
            mom_pct=item["mom_pct"],
            month=month,
            prev_month=prev_month,
        )

    # ---------------------------------------------------------
    # 7. Suppress remaining flagged categories.
    # ---------------------------------------------------------
    suppressed = [
        item["category"]
        for item in flagged[3:]
    ]

    # Make the flagged output contain only the required fields.
    flagged_output = top_three

    # ---------------------------------------------------------
    # 7b. Exact-boundary categories are separately escalated.
    # ---------------------------------------------------------
    escalated.sort()

    # ---------------------------------------------------------
    # 8. Emit structured JSON.
    # ---------------------------------------------------------
    action = (
        "drafted_and_held_for_approval"
        if flagged_output
        else "drafted_and_held_for_approval"
    )

    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_output,
        "suppressed_categories": suppressed,
        "escalated_categories": escalated,
        "action_taken": action,
    }


def print_result(result: dict) -> None:
    """Print exactly one structured JSON object."""
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python part4_agent/mock_agent_runner.py "
            "<month> <previous_month_csv> <current_month_csv>"
        )
        sys.exit(1)

    run_month = sys.argv[1]
    previous_csv = sys.argv[2]
    current_csv = sys.argv[3]

    result = run(
        run_month,
        previous_csv,
        current_csv,
    )

    print_result(result)