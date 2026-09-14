# Meesho Reseller Growth & Alert Intelligence Pipeline

A small end-to-end analytics and agent workflow for monitoring Meesho reseller category revenue, identifying significant month-on-month movements, creating stakeholder narratives, and holding alerts for human approval.

## Project Structure

```text
data/
├── generate_dataset.py
├── resellers.csv
├── orders.csv
└── meesho_reseller.db

part1_sql/
├── queries.sql
└── output/
    ├── monthly_category_revenue.csv
    ├── region_revenue.csv
    ├── top_resellers.csv
    ├── zero_order_resellers.csv
    ├── zero_order_count_demo.csv
    └── june_delivered_aov.csv

part2_engine/
├── growth_engine.py
├── test_growth_engine.py
└── fixtures/
    ├── corrupted_feed.csv
    └── monthly_category_revenue.csv

part3_narrative/
├── prompt_pack.md
├── narrative_report.md
└── masking.py

part4_agent/
├── agent_spec.md
└── mock_agent_runner.py