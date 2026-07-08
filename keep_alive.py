from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running 24/7!"

def run():
    # Render നൽകുന്ന പോർട്ട് (Port) തനിയെ കണ്ടുപിടിക്കാൻ
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
