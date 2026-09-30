import pytest

from app.agent import REDEEMED_CODES, redeem_discount_code, root_agent


@pytest.fixture(autouse=True)
def reset_redeemed_codes():
    """Reset the REDEEMED_CODES set before each test to ensure test isolation."""
    REDEEMED_CODES.clear()
    yield
    REDEEMED_CODES.clear()


def test_redeem_discount_code_success():
    """Test successful redemption of a valid single-use discount code."""
    result = redeem_discount_code(code="WELCOME50", user_id="user_101")
    assert "Success" in result
    assert "WELCOME50" in result
    assert "50% off your purchase" in result
    assert "user_101" in result
    assert "WELCOME50" in REDEEMED_CODES


def test_redeem_discount_code_single_use_enforcement():
    """Test that a discount code can only be redeemed once (replay prevention)."""
    first_attempt = redeem_discount_code(code="SUMMER20", user_id="user_101")
    assert "Success" in first_attempt
    assert "SUMMER20" in REDEEMED_CODES

    # Second attempt with the same code must fail, even for another user ID
    second_attempt = redeem_discount_code(code="SUMMER20", user_id="user_202")
    assert "Error" in second_attempt
    assert "already been redeemed" in second_attempt


def test_redeem_discount_code_requires_registered_user_id():
    """Test that an empty or whitespace user_id is rejected."""
    result_empty = redeem_discount_code(code="WELCOME50", user_id="")
    assert "Error" in result_empty
    assert "registered user ID is required" in result_empty
    assert "WELCOME50" not in REDEEMED_CODES

    result_whitespace = redeem_discount_code(code="WELCOME50", user_id="   ")
    assert "Error" in result_whitespace
    assert "registered user ID is required" in result_whitespace
    assert "WELCOME50" not in REDEEMED_CODES


def test_redeem_discount_code_invalid_code():
    """Test that non-existent discount codes are rejected."""
    result = redeem_discount_code(code="FAKE50", user_id="user_101")
    assert "Error" in result
    assert "Invalid discount code" in result
    assert "FAKE50" not in REDEEMED_CODES


def test_redeem_discount_code_case_insensitivity_and_whitespace():
    """Test normalization of whitespace and lowercase discount codes."""
    result = redeem_discount_code(code="  welcome50  ", user_id="user_101")
    assert "Success" in result
    assert "WELCOME50" in REDEEMED_CODES


def test_root_agent_configuration():
    """Test root agent configuration and tool binding."""
    assert root_agent.name == "shopping_assistant"
    assert redeem_discount_code in root_agent.tools
    assert isinstance(root_agent.instruction, str)
    assert "AI shopping assistant" in root_agent.instruction
