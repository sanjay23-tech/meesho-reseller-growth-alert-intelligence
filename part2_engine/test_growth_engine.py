from growth_engine import mom_growth, is_flagged, validate_feed


# Test 1: April → May Ethnic Wear
def test_ethnic_wear_growth():
    # Given
    previous = 104520.77
    current = 185107.61

    # When
    growth = mom_growth(previous, current)
    result = is_flagged(growth)

    # Then
    assert growth == 77.1
    assert result == "flagged"


# Test 2: May → June Beauty & Personal Care
def test_beauty_growth():
    # Given
    previous = 35542.11
    current = 37559.07

    # When
    growth = mom_growth(previous, current)
    result = is_flagged(growth)

    # Then
    assert growth == 5.67
    assert result == "not_flagged"


# Test 3: Exactly 8% boundary
def test_exact_boundary():
    # Given
    previous = 100000
    current = 108000

    # When
    growth = mom_growth(previous, current)
    result = is_flagged(growth)

    # Then
    assert growth == 8.0
    assert result == "escalate_exact_boundary"


# Test 4: Corrupted feed validation
def test_corrupted_feed():
    # Given
    feed_path = "part2_engine/fixtures/corrupted_feed.csv"

    # When
    valid, errors = validate_feed(feed_path)

    # Then
    assert valid is False
    assert errors == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]