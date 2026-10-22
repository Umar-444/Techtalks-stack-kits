"""
Lightweight Mock Target Microservice for DevSecOps CI Verification.
Provides an authentic /healthz endpoint and zero-dependency routing.
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class SecurityTargetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz" or self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            payload = {
                "status": "ok",
                "app": "security-devsecops-ci",
                "version": "1.0.0",
                "pipeline": "GitHub Actions + Gitleaks + Semgrep + Trivy",
                "slsa_level": "SLSA Build Level 3"
            }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run(port=8080):
    server = HTTPServer(("0.0.0.0", port), SecurityTargetHandler)
    print(f"DevSecOps test target running on port {port}...")
    server.serve_forever()

if __name__ == "__main__":
    run()
