import json
from typing import List
from analyzers.ast_analyzer import Finding

def generate_sarif(findings: List[Finding]) -> str:
    rules = {}
    results = []

    for f in findings:
        if f.rule_id not in rules:
            rules[f.rule_id] = {
                "id": f.rule_id,
                "shortDescription": {"text": f.rule_id},
                "defaultConfiguration": {
                    "level": "error" if f.severity == "HIGH" else "warning"
                }
            }

        results.append({
            "ruleId": f.rule_id,
            "level": "error" if f.severity == "HIGH" else "warning",
            "message": {"text": f.message},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": f.file_path.replace("\\", "/")},
                        "region": {
                            "startLine": f.line,
                            "startColumn": f.col + 1
                        }
                    }
                }
            ]
        })

    sarif_doc = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "SecurityAuditCLI",
                        "version": "1.0.0",
                        "rules": list(rules.values())
                    }
                },
                "results": results
            }
        ]
    }
    return json.dumps(sarif_doc, indent=2)
