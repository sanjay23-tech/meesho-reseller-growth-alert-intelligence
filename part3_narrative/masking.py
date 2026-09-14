def alias_for(reseller_id: str) -> str:
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    return not any(name in text for name in reseller_names)


# Required positive and negative checks
assert alias_for("RS019") == "ALIAS-19"
assert alias_for("RS006") == "ALIAS-06"

reseller_names = [
    "Mumbai Reseller 1",
    "Mumbai Reseller 4",
    "Hyderabad Reseller 6",
    "Lucknow Reseller 6",
    "Jaipur Reseller 5",
]

final_narrative = """
West — ALIAS-19: total spend INR 75295.09.
West — ALIAS-22: total spend INR 73882.33.
South — ALIAS-12: total spend INR 69936.46.
North — ALIAS-06: total spend INR 64238.97.
North — ALIAS-05: total spend INR 61825.02.
"""

assert assert_no_raw_names_leak(final_narrative, reseller_names) is True

leaky_narrative = "Mumbai Reseller 1 had the highest spend."

assert assert_no_raw_names_leak(leaky_narrative, reseller_names) is False