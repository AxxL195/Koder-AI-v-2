from config import GITHUB_WEBHOOK_KEY
import hmac
import hashlib

def verify_signature(body:str,signature:str) -> bool:
    expected_signature= hmac.new(
        GITHUB_WEBHOOK_KEY.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    expected_signature = f"sha256={expected_signature}"

    return hmac.compare_digest(expected_signature,signature)