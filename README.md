# Meesho Reseller Growth & Alert Intelligence Pipeline

An end-to-end analytics and agent workflow for monitoring Meesho reseller category revenue, identifying significant month-on-month movements, generating stakeholder-friendly narratives, and preparing controlled alerts for human approval.

## Objective

The objective of this project is to build a reliable revenue-monitoring workflow that combines SQL analysis, Python-based growth calculations, data validation, narrative generation, privacy-safe reporting, and a guarded alerting agent.

The workflow is designed to identify meaningful category-level revenue movements while preventing invalid data or unverified messages from reaching stakeholders.

## Key Features

- Category-level revenue analysis using SQL
- Monthly and regional revenue analysis
- Top-reseller and zero-order reseller analysis
- Month-on-month (MoM) growth calculation
- 8% revenue movement threshold for flagging
- Exact 8% boundary escalation
- Input-feed validation and corrupted-data detection
- Automated stakeholder narrative generation
- Privacy-safe reseller name masking
- Top-3 alert drafting limit to prevent notification flooding
- Human approval checkpoint before an alert is considered ready to send
- Structured JSON output from the monitoring agent

## Workflow

The project is divided into four parts:

### Part 1 — SQL Analytics

SQL queries are used to generate business metrics from the reseller and order data, including:

- Monthly category revenue
- Regional revenue
- Top resellers with total spend above INR 50,000
- Resellers with zero orders
- Zero-order count validation
- June delivered Average Order Value (AOV)

The results are stored as CSV outputs for use in later stages.

### Part 2 — Growth Engine

The Python growth engine:

- Calculates month-on-month revenue movement
- Flags movements above the 8% threshold
- Identifies the exact 8% boundary separately
- Validates incoming revenue feeds
- Detects missing categories
- Detects missing revenue values
- Detects non-numeric revenue values
- Detects negative revenue values

The module also includes automated tests covering normal growth, non-flagged growth, the exact 8% boundary, and corrupted-feed validation.

### Part 3 — Narrative & Privacy

This stage converts analytical results into stakeholder-friendly narratives.

The narratives separate:

- **Facts** — verified revenue values and calculated movements
- **Hypotheses** — possible explanations for the movement
- **Implications** — suggested areas for managerial review

Reseller identities are protected using privacy-safe aliases rather than exposing raw reseller names in external-facing narratives.

### Part 4 — Alert Intelligence Agent

The mock agent combines the outputs from the previous stages.

The agent:

1. Validates the incoming feed.
2. Performs a hard stop if validation fails.
3. Calculates MoM movement for each category.
4. Applies the 8% threshold.
5. Sorts flagged categories by absolute movement.
6. Drafts messages for a maximum of three flagged categories.
7. Suppresses additional flagged categories for manual review.
8. Separately escalates categories exactly at the 8% boundary.
9. Produces one structured JSON result.

The agent does not automatically send emails or messages. Every drafted message is held for human approval.

## Project Structure

```text
meesho-reseller-growth-alert-intelligence/
│
├── data/
│   ├── generate_dataset.py
│   ├── resellers.csv
│   ├── orders.csv
│   └── meesho_reseller.db
│
├── part1_sql/
│   ├── queries.sql
│   └── output/
│       ├── monthly_category_revenue.csv
│       ├── region_revenue.csv
│       ├── top_resellers.csv
│       ├── zero_order_resellers.csv
│       ├── zero_order_count_demo.csv
│       └── june_delivered_aov.csv
│
├── part2_engine/
│   ├── growth_engine.py
│   ├── test_growth_engine.py
│   └── fixtures/
│       ├── corrupted_feed.csv
│       └── monthly_category_revenue.csv
│
├── part3_narrative/
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   └── masking.py
│
├── part4_agent/
│   ├── agent_spec.md
│   └── mock_agent_runner.py
│
├── .gitignore
└── README.mds