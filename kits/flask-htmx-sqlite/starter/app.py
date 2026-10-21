from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string("<h1>Flask + HTMX Token-Light</h1>")

@app.route("/health")
def health():
    return {"status": "ok", "token_light": True}

if __name__ == "__main__":
    app.run(port=8080)
