# Meesho Reseller Growth & Alert Intelligence Agent Specification

## 1. Goal

Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every drafted message before it is considered sent.

## 2. Tools

The agent uses the following project functions:

- `validate_feed` from Part 2 to validate the monthly revenue feed.
- `mom_growth` from Part 2 to calculate month-on-month revenue movement.
- `is_flagged` from Part 2 to classify the movement using the 8% threshold.
- Part 3 prompt-pack template-fill logic to draft a stakeholder message for flagged categories.

The agent does not use any external API, network service, Gmail, SMTP, or automatic message-sending integration.

## 3. Memory / State

Between runs, the agent needs the previous month's revenue for each category.

This previous-month category revenue is required to calculate the next month's month-on-month growth.

The current run also keeps the calculated category results, including:
- category
- previous revenue
- current revenue
- mom_pct
- flagged status
- drafted status
- drafted message, when applicable

## 4. Planner

The agent follows these ordered subtasks:

1. Load the monthly revenue feed and run `validate_feed`.
2. If the feed is invalid, Hard Stop and report the validation errors.
3. If the feed is valid, compute `mom_growth` for every category against the previous month.
4. Run `is_flagged` on every category.
5. Sort flagged categories by absolute `mom_pct` in descending order.
6. Draft a message using Part 3's prompt template for at most the top 3 flagged categories by magnitude.
7. Log any remaining flagged categories beyond the top 3 as `suppressed, review manually` without drafting a message.
7b. Separately log any category whose `is_flagged` result is `escalate_exact_boundary` into `escalated_categories`, without drafting a message.
8. Emit one structured JSON object for the run.

The top-3 drafting cap prevents notification flooding by avoiding unlimited message drafting for flagged categories.

## 5. Feedback Loop

Every drafted message is held for human approval.

The mock runner only drafts and holds messages. It does not send them automatically.

Human approval is therefore the checkpoint between drafting a message and considering it ready to be sent.

## 6. Guardrails

### Input Guardrail

`validate_feed` must pass before any month-on-month calculation or drafting takes place.

If validation fails, the agent must Hard Stop and surface all validation errors.

### Action Guardrail

The agent must never automatically send a message.

It can only draft a message and hold it for human approval.

No Gmail, SMTP, or other message-sending integration is used.

### Output Guardrail

Every number in a drafted message must trace back to a verified Part 1 or Part 2 value.

The agent must not invent additional figures.

## 7. Success and Error Stopping Conditions

### Success

The run succeeds when:
- the feed passes validation,
- month-on-month calculations are completed,
- flagged categories are correctly identified,
- at most 3 messages are drafted,
- remaining flagged categories are suppressed when necessary,
- exact-boundary categories are separately escalated,
- and every number in a drafted message is traceable to Part 1 or Part 2.

If no category crosses the threshold, the run can also succeed with zero drafted messages.

### Error

If `validate_feed` returns `False`, the agent performs a Hard Stop.

The validation errors are surfaced in the output.

No MoM calculation, flagging, drafting, or suppression is attempted on invalid data.

## 8. Agent-Level Given-When-Then Specifications

### Specification 1 — May Ethnic Wear

**Given** April to May Ethnic Wear revenue moves from 104520.77 to 185107.61,

**When** `mom_growth` and `is_flagged` are run by the agent,

**Then** `mom_growth` returns 77.1 and `is_flagged` returns `"flagged"`.

The agent should therefore include Ethnic Wear among the flagged categories and draft it when it is within the top 3 by magnitude.

### Specification 2 — June Beauty & Personal Care

**Given** May to June Beauty & Personal Care revenue moves from 35542.11 to 37559.07,

**When** the agent evaluates the category,

**Then** `mom_growth` returns 5.67 and `is_flagged` returns `"not_flagged"`.

The category must not appear in either `flagged_categories` or `suppressed_categories`.

### Specification 3 — Exact 8% Boundary

**Given** previous revenue is 100000 and current revenue is 108000,

**When** the agent evaluates the category,

**Then** `mom_growth` returns exactly 8.0 and `is_flagged` returns `"escalate_exact_boundary"`.

The category must be placed in `escalated_categories`, not treated as either flagged or not flagged.

### Specification 4 — Corrupted Feed

**Given** the corrupted feed fixture contains a negative revenue row, a missing category, and a missing revenue value,

**When** the agent runs `validate_feed`,

**Then** validation returns `False` with exactly these three errors in order:

1. `line 3: negative revenue (-4200.0) for category=Western Wear`
2. `line 4: missing category (month=July)`
3. `line 6: missing revenue (category=Home & Kitchen)`

The agent must Hard Stop, with no MoM calculation attempted.

## 9. Structured Output

Every run produces one JSON object with exactly these top-level keys:

- `run_month`
- `validation_status`
- `validation_errors`
- `flagged_categories`
- `suppressed_categories`
- `escalated_categories`
- `action_taken`

`validation_status` is either `"valid"` or `"invalid"`.

`validation_errors` is a list and is empty on successful validation.

Each object in `flagged_categories` contains:

- `category`
- `mom_pct`
- `previous_revenue`
- `current_revenue`
- `drafted`
- `message` when a message is drafted

`suppressed_categories` contains category names that were flagged but exceeded the top-3 drafting cap.

`escalated_categories` contains categories whose result was `"escalate_exact_boundary"`.

`action_taken` is either:

- `"drafted_and_held_for_approval"`
- `"hard_stop"`

## 10. Privacy

Any external-facing reseller narrative must use the privacy-safe alias from Part 3 rather than a raw reseller name.

The agent must not expose raw reseller names in drafted external-facing summaries.