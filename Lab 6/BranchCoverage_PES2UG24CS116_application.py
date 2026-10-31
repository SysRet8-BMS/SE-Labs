import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


# Branch coverage: exercise both outcomes of each decision.


@pytest.mark.parametrize(
    ("material", "weight", "bonus", "expected"),
    [
        ("unknown", 10, False, None),  # invalid material branch
        ("paper", -1, False, None),    # invalid weight branch
        ("paper", 5, False, 0),        # extra <= 0
        ("paper", 6, False, 6),        # extra > 0
        ("paper", 4, True, 0),         # bonus lowers paper minimum
        ("paper", 5, True, 6),
        ("plastic", 2, True, 0),       # bonus lowers plastic minimum
        ("plastic", 3, True, 6),
        ("metal", 3, True, 12),        # bonus does not lower metal minimum
        ("metal", 22, False, 240),     # extra == 20: standard rate
        ("metal", 23, False, 378),     # extra > 20: metal rate adjustment
        ("paper", 25, False, 120),     # extra == 20: standard rate
        ("paper", 26, False, 210),     # extra > 20: non-metal rate adjustment
    ],
)
def test_reward_points_branches(material, weight, bonus, expected):
    if material == "unknown" or weight < 0:
        with pytest.raises(ValueError):
            reward_points(material, weight, bonus)
    else:
        assert reward_points(material, weight, bonus) == expected


@pytest.mark.parametrize(
    ("weight", "bags", "hazardous", "expected"),
    [
        (5, 4, True, True),       # hazardous and weight <= 5
        (6, 1, True, False),      # hazardous and weight > 5
        (50, 3, False, True),     # non-hazardous, weight <= 50, bags <= 3
        (51, 1, False, False),    # non-hazardous, weight > 50
        (20, 4, False, False),    # weight accepted, bags > 3
    ],
)
def test_collection_accepted_branches(weight, bags, hazardous, expected):
    assert collection_accepted(weight, bags, hazardous) is expected


@pytest.mark.parametrize(
    ("minutes", "morning", "holiday", "expected"),
    [
        (20, True, False, "open"),
        (19, True, False, "late"),
        (4, True, False, "missed"),
        (10, False, False, "open"),
        (9, False, False, "late"),
        (35, True, True, "open"),
        (34, True, True, "late"),
        (19, False, True, "late"),
        (9, False, True, "missed"),
    ],
)
def test_slot_status_branches(minutes, morning, holiday, expected):
    assert slot_status(minutes, morning, holiday) == expected
