from flask import Flask, request
import hmac
import hashlib
import json

class WebhookServer:
    def __init__(self, secret: str = "mySecret", port: int = 3010):
        self.app = Flask(__name__)
        self.secret = secret
        self.port = port

        # Register the webhook endpoint
        self.app.route("/webhooks", methods=["POST"])(self.handle_webhook)

    def _verify_signature(self, payload: bytes, signature: str) -> bool:
        computed = hmac.new(
            self.secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(computed, signature)

    def handle_webhook(self):
        signature = request.headers.get("Authorization")
        if not signature:
            return {"error": "Missing signature"}, 401

        if not self._verify_signature(request.get_data(), signature):
            return {"error": "Invalid signature"}, 401

        print(json.dumps(request.json, indent=2))
        return {"status": "ok"}

    def run(self):
        self.app.run(port=self.port)

# Para usar directamente desde línea de comandos
if __name__ == "__main__":
    server = WebhookServer()
    server.run()