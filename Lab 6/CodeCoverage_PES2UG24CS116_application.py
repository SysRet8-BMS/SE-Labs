import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


# Statement/code coverage: execute every statement at least once.
def test_reward_points_unknown_material():
    with pytest.raises(ValueError):
        reward_points("glass", 10, False)


def test_reward_points_negative_weight():
    with pytest.raises(ValueError):
        reward_points("paper", -1, False)


def test_reward_points_paper_without_bonus():
    assert reward_points("paper", 10, False) == 30


def test_reward_points_plastic_with_bonus():
    assert reward_points("plastic", 10, True) == 48


def test_reward_points_metal_standard_rate():
    assert reward_points("metal", 10, False) == 96


def test_reward_points_non_metal_high_rate():
    assert reward_points("paper", 26, False) == 210


def test_reward_points_metal_high_rate():
    assert reward_points("metal", 23, False) == 378


def test_collection_hazardous_accepted():
    assert collection_accepted(5, 10, True) is True


def test_collection_hazardous_rejected():
    assert collection_accepted(6, 1, True) is False


def test_collection_non_hazardous_accepted():
    assert collection_accepted(20, 2, False) is True


def test_collection_non_hazardous_rejected_by_weight():
    assert collection_accepted(51, 1, False) is False


def test_collection_non_hazardous_rejected_by_bag_count():
    assert collection_accepted(20, 4, False) is False


def test_slot_status_open():
    assert slot_status(20, True, False) == "open"


def test_slot_status_late():
    assert slot_status(19, True, False) == "late"


def test_slot_status_missed():
    assert slot_status(4, True, False) == "missed"


def test_slot_status_holiday():
    assert slot_status(35, True, True) == "open"
