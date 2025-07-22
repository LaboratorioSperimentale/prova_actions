# webhook_listener.py
from flask import Flask, request, abort
import hmac
import hashlib
import subprocess
import os

app = Flask(__name__)

# Set your GitHub webhook secret here
GITHUB_SECRET = b'your_webhook_secret'

def verify_signature(payload, signature):
    mac = hmac.new(GITHUB_SECRET, msg=payload, digestmod=hashlib.sha256)
    expected = 'sha256=' + mac.hexdigest()
    return hmac.compare_digest(expected, signature)

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if signature is None or not verify_signature(request.data, signature):
        abort(403)

    # Optional: check the event type
    event = request.headers.get('X-GitHub-Event')
    if event != 'push':
        return 'Ignoring non-push event', 200

    # Run the update script
    subprocess.Popen(['python3', 'update.py'])

    return 'Update triggered', 200

if __name__ == '__main__':
    app.run(port=5000, debug=False)
