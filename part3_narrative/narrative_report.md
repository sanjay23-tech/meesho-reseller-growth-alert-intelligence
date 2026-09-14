# Reliable AI Narrative Report

## 1. Worked Narrative — May Ethnic Wear

### Context

This measures Ethnic Wear revenue from April to May 2026.

### Insight

**Fact:** Ethnic Wear revenue increased from INR 104520.77 in April to INR 185107.61 in May, representing an exact month-on-month increase of **+77.1%**.

### Implication

**Hypothesis:** The strong increase may indicate higher demand or improved reseller activity for Ethnic Wear. The regional manager should check which resellers or regions contributed most to the increase and confirm whether inventory and supply can support continued demand.

### Self-score

- **Specificity — Pass:** The narrative uses the correct category, months, revenue values, and exact +77.1% movement.
- **Audience fit — Pass:** The narrative is written for a regional manager rather than a data engineer.
- **Completeness — Pass:** It includes context, a factual insight, and an actionable implication.
- **Actionability — Pass:** It recommends checking reseller/region contributions and inventory readiness.

---

## 2. Worked Narrative — June Ethnic Wear

### Context

This measures Ethnic Wear revenue from May to June 2026.

### Insight

**Fact:** Ethnic Wear revenue decreased from INR 185107.61 in May to INR 76371.53 in June, representing an exact month-on-month decrease of **-58.74%**.

### Implication

**Hypothesis:** The sharp decline may indicate weaker demand or reduced reseller activity. The regional manager should check which regions and resellers experienced the largest decline and review inventory availability and recent sales activity before deciding on corrective action.

### Self-score

- **Specificity — Pass:** The narrative uses the correct category, months, revenue values, and exact -58.74% movement.
- **Audience fit — Pass:** The narrative is written for a regional manager rather than a data engineer.
- **Completeness — Pass:** It includes context, a factual insight, and an actionable implication.
- **Actionability — Pass:** It recommends checking regional/reseller performance and inventory availability.

---

## 3. Chart-choice Justification

### 3.1 Which month had the highest total revenue?

**Recommended chart: Column chart.**

This is a univariate comparison of total revenue across three months. A simple column chart makes the highest month immediately visible within 10 seconds. The y-axis should start at zero, and no legend is needed because there is only one series.

The totals are April = INR 419417.43, May = INR 444594.25, and June = INR 398055.24. Therefore, May had the highest total revenue.

### 3.2 What percentage share does Ethnic Wear represent of April's total revenue?

**Recommended chart: Donut chart.**

This is a part-to-whole question, showing Ethnic Wear's share of April total revenue. A simple donut chart can communicate the share clearly within 10 seconds. Only the required categories should be shown, and unnecessary visual decoration should be avoided.

Ethnic Wear revenue was INR 104520.77 out of April's total revenue of INR 419417.43, representing **24.92%**.

### 3.3 How do the four regions compare on total revenue?

**Recommended chart: Column chart.**

This is a bivariate comparison of region and total revenue. A column chart allows the four regions to be compared directly and makes the ranking clear within 10 seconds. The y-axis should start at zero, and no legend is needed because there is only one revenue series.

The Part 1 regional totals are North = INR 337125.46, West = INR 333106.33, South = INR 316736.68, and East = INR 275098.45.

---

## 4. Top-Reseller Narrative with Privacy Masking

The top-reseller analysis from Part 1 identified five resellers whose total spend exceeded INR 50000 and ranked them by total spend.

- **West — ALIAS-19:** total spend INR 75295.09.
- **West — ALIAS-22:** total spend INR 73882.33.
- **South — ALIAS-12:** total spend INR 69936.46.
- **North — ALIAS-06:** total spend INR 64238.97.
- **North — ALIAS-05:** total spend INR 61825.02.

**Implication:** **Hypothesis:** These high-spend reseller accounts may represent important contributors to overall revenue. A regional manager should review their recent category mix and activity to understand what is driving their spend and whether similar patterns can be encouraged elsewhere.

No raw reseller names are exposed in this external-facing narrative. Only the reseller region and privacy-safe alias are used.

### Masking check

The final narrative above contains no raw reseller names.

Expected checks:

- `alias_for("RS019")` → `ALIAS-19`
- `assert_no_raw_names_leak(final_narrative, reseller_names)` → `True`
- `assert_no_raw_names_leak(version_containing_Mumbai_Reseller_1, reseller_names)` → `False`