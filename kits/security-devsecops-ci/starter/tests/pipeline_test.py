"""
Automated Unit Tests for DevSecOps CI Pipeline Configuration & Health Probe.
"""
import unittest
import os
import json
import yaml

class TestDevSecOpsPipeline(unittest.TestCase):
    def setUp(self):
        self.starter_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def test_workflow_syntax(self):
        wf = os.path.join(self.starter_dir, ".github/workflows/devsecops.yml")
        self.assertTrue(os.path.exists(wf), "devsecops.yml workflow must exist")
        with open(wf, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.assertIn("jobs", data, "Workflow must contain jobs section")
        self.assertIn("secret-scan", data["jobs"])
        self.assertIn("sast-scan", data["jobs"])
        self.assertIn("container-cve-scan", data["jobs"])

    def test_semgrep_configuration(self):
        sg = os.path.join(self.starter_dir, ".semgrep.yml")
        self.assertTrue(os.path.exists(sg), ".semgrep.yml must exist")
        with open(sg, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.assertIn("rules", data)
        self.assertGreaterEqual(len(data["rules"]), 1)

    def test_dockerfile_hardening(self):
        df = os.path.join(self.starter_dir, "Dockerfile")
        self.assertTrue(os.path.exists(df), "Dockerfile must exist")
        with open(df, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("USER", content, "Dockerfile must declare non-root USER")
        self.assertIn("alpine", content, "Dockerfile must use minimal Alpine base")

if __name__ == "__main__":
    unittest.main()
