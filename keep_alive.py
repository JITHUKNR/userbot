from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "ബോട്ട് വിജയകരമായി റൺ ചെയ്യുന്നുണ്ട്..."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
