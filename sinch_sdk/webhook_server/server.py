from flask import Flask, request, jsonify
from sinch_sdk import SinchClient
from sinch_sdk.utils import validate_webhook_signature
import os

app = Flask(__name__)

webhook_secret = os.environ.get('WEBHOOK_SECRET', 'mySecret')
client = SinchClient(api_key=os.environ.get('API_KEY', 'there-is-no-key'))

@app.route("/webhooks", methods=["POST"])
def handle_webhook():
    signature = request.headers.get("Authorization", "").split(" ")[1]
    payload = request.get_json()

    if not validate_webhook_signature(payload, signature, webhook_secret):
        return jsonify({"error": "Invalid signature"}), 401

    print(f"Message {payload.get('id')} status: {payload.get('status')}")
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(port=3010)