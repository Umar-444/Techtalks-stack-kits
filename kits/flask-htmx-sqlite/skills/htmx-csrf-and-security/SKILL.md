---
name: htmx-csrf-and-security
description: Implementing CSRF protection, Content Security Policy (CSP), and secure headers for HTMX 2.0 AJAX requests in Flask.
---
# HTMX CSRF Protection and Web Security Skill

## 1. Flask-WTF CSRFProtect Setup
Install `Flask-WTF` and initialize in `app/__init__.py`:
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback-secret-for-dev")
    app.config["WTF_CSRF_TIME_LIMIT"] = 7200  # 2 hours
    csrf.init_app(app)
    return app
```

## 2. Global HTMX CSRF Header Injection
In `app/templates/base.html`, include the CSRF token in the document `<head>` and hook HTMX:
```html
<head>
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <script src="https://unpkg.com/htmx.org@2.0.3"></script>
    <script>
        document.body.addEventListener('htmx:configRequest', function(evt) {
            evt.detail.headers['X-CSRFToken'] = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        });
    </script>
</head>
```
Alternatively, configure HTMX declaratively on `<body>`:
```html
<body hx-headers='{"X-CSRFToken": "{{ csrf_token() }}"}'>
```

## 3. Handling 400 CSRF Errors with User-Friendly Feedback
Add an error handler to smoothly prompt the user if their token expired:
```python
from flask_wtf.csrf import CSRFError

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    if request.headers.get("HX-Request") == "true":
        return "<div class='toast error'>Session token expired. Please refresh the page.</div>", 400
    return render_template("errors/csrf.html", reason=e.description), 400
```
