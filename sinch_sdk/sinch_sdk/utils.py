import hmac
import hashlib
from typing import Any, Dict

def validate_webhook_signature(payload: Dict[str, Any], signature: str, secret: str) -> bool:
    """Validate webhook signature using HMAC-SHA256."""
    computed = hmac.new(
        secret.encode(),
        str(payload).encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed, signature)