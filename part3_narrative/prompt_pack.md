# Reliable AI Narrative Prompt Pack

## Trigger

Use this prompt when a category's `is_flagged` result is `"flagged"` because its month-on-month revenue movement exceeds the 8% threshold.

## Input list

The prompt requires these values:

- `{category}` — the category name
- `{previous_revenue}` — revenue in the previous month
- `{current_revenue}` — revenue in the current month
- `{mom_pct}` — month-on-month revenue percentage
- `{month}` — current month
- `{prev_month}` — previous month

## Prompt

Write a concise stakeholder update for a regional manager using the following structure:

**Context:** State what category is being measured and clearly name the comparison period as `{month}` vs. `{prev_month}`.

**Insight:** State the supplied revenue values `{previous_revenue}` and `{current_revenue}` and the supplied month-on-month movement `{mom_pct}`. Treat these numbers as facts. Do not introduce or calculate any additional numbers.

**Implication:** Give one specific and actionable next step for the regional manager. If suggesting a possible cause, label it explicitly as a hypothesis because the supplied data does not prove the cause.

Use only the supplied placeholder values. Never state a number that is not one of the supplied placeholders. Keep the message focused on the business decision and avoid technical or unnecessary detail.

## Checklist

Before the update is used, verify:

1. Every number in the draft exactly matches a supplied placeholder value.
2. The category name and comparison months are correct.
3. The Insight section labels supplied numerical information as fact.
4. Any proposed cause is clearly labeled as a hypothesis rather than a proven fact.
5. The recommendation is specific and actionable, not vague.
6. The message is written for a regional manager rather than a data engineer.
7. No raw reseller name or other unnecessary internal identifier is exposed.