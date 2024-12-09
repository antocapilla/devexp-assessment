import pytest
from sinch_sdk import SinchClient

@pytest.fixture
def client():
    return SinchClient(
        api_key="there-is-no-key",
        base_url="http://localhost:3000"
    )