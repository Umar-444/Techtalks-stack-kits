"""OWASP Top 10:2025 taxonomy and control classification.

The 2025 edition is the current final release; the 2021 edition is superseded.
Two categories are new (A03 Software Supply Chain Failures, A10 Mishandling of
Exceptional Conditions) and SSRF was absorbed into A01 Broken Access Control.

This module is the single source of truth for OWASP identifiers used across
kit security manifests, the coverage matrix, and CI validation.
"""

from __future__ import annotations

import re
from typing import NamedTuple

EDITION = "2025"
_BASE_URL = "https://owasp.org/Top10/2025"


class Category(NamedTuple):
    id: str
    rank: int
    name: str
    slug: str
    summary: str

    @property
    def url(self) -> str:
        return f"{_BASE_URL}/{self.slug}/"


CATEGORIES: tuple[Category, ...] = (
    Category(
        "A01:2025", 1, "Broken Access Control", "A01_2025-Broken_Access_Control",
        "Authorization gaps including IDOR/BOLA, tenant leakage, privilege "
        "escalation, and server-side request forgery (absorbed from A10:2021).",
    ),
    Category(
        "A02:2025", 2, "Security Misconfiguration", "A02_2025-Security_Misconfiguration",
        "Insecure defaults, permissive CORS, debug surfaces in production, "
        "over-privileged containers, and missing hardening headers.",
    ),
    Category(
        "A03:2025", 3, "Software Supply Chain Failures", "A03_2025-Software_Supply_Chain_Failures",
        "Compromise of dependencies, build systems, package registries, and "
        "distribution infrastructure. Expanded from A06:2021 components.",
    ),
    Category(
        "A04:2025", 4, "Cryptographic Failures", "A04_2025-Cryptographic_Failures",
        "Weak or missing encryption in transit and at rest, poor key handling, "
        "and inadequate password hashing.",
    ),
    Category(
        "A05:2025", 5, "Injection", "A05_2025-Injection",
        "SQL, NoSQL, command, template, and LDAP injection, plus cross-site "
        "scripting arising from untrusted input reaching an interpreter.",
    ),
    Category(
        "A06:2025", 6, "Insecure Design", "A06_2025-Insecure_Design",
        "Missing or ineffective control design: absent threat modelling, "
        "unbounded resource consumption, and missing rate limits.",
    ),
    Category(
        "A07:2025", 7, "Authentication Failures", "A07_2025-Authentication_Failures",
        "Credential stuffing exposure, weak session lifecycle, missing MFA. "
        "Renamed from Identification and Authentication Failures.",
    ),
    Category(
        "A08:2025", 8, "Software or Data Integrity Failures", "A08_2025-Software_or_Data_Integrity_Failures",
        "Unverified updates, insecure deserialization, and CI/CD pipelines "
        "that accept unsigned or unpinned artifacts.",
    ),
    Category(
        "A09:2025", 9, "Security Logging & Alerting Failures", "A09_2025-Security_Logging_and_Alerting_Failures",
        "Insufficient audit trails, unmonitored security events, and logs that "
        "leak secrets or personal data. Renamed to emphasise alerting.",
    ),
    Category(
        "A10:2025", 10, "Mishandling of Exceptional Conditions", "A10_2025-Mishandling_of_Exceptional_Conditions",
        "Improper error handling, fail-open logic, verbose stack traces, and "
        "unhandled edge cases that degrade into insecure states.",
    ),
)

BY_ID: dict[str, Category] = {c.id: c for c in CATEGORIES}

#: Mapping from the superseded 2021 edition to current 2025 identifiers.
MIGRATION_2021_TO_2025: dict[str, str] = {
    "A01:2021": "A01:2025",  # Broken Access Control
    "A02:2021": "A04:2025",  # Cryptographic Failures
    "A03:2021": "A05:2025",  # Injection
    "A04:2021": "A06:2025",  # Insecure Design
    "A05:2021": "A02:2025",  # Security Misconfiguration
    "A06:2021": "A03:2025",  # Vulnerable Components -> Supply Chain
    "A07:2021": "A07:2025",  # Auth Failures
    "A08:2021": "A08:2025",  # Integrity Failures
    "A09:2021": "A09:2025",  # Logging Failures
    "A10:2021": "A01:2025",  # SSRF absorbed into Broken Access Control
}


def normalize_id(raw: str) -> str | None:
    """Coerce a loose OWASP reference ('A01', 'a01:2021', 'A1') to a 2025 id."""
    if not raw:
        return None
    text = raw.strip().upper().replace(" ", "")
    match = re.match(r"^A0?(\d{1,2})(?::(\d{4}))?", text)
    if not match:
        return None
    num, year = int(match.group(1)), match.group(2)
    if not 1 <= num <= 10:
        return None
    candidate = f"A{num:02d}:{year or EDITION}"
    if year == "2021":
        return MIGRATION_2021_TO_2025.get(candidate)
    return candidate if candidate in BY_ID else None


# Ordered classification rules. The first pattern that matches a control's text
# wins, so narrower security concepts are listed before broader ones. Each entry
# is (compiled pattern, owasp id, default severity, cwe identifiers).
_RULES: tuple[tuple[re.Pattern[str], str, str, tuple[str, ...]], ...] = tuple(
    (re.compile(pattern, re.I), owasp, severity, cwes)
    for pattern, owasp, severity, cwes in (
        # --- Memory & type safety ----------------------------------------------
        # Listed first: phrases like "unsafe code policy" would otherwise be
        # caught by the broader authorization patterns below.
        (r"unsafe code|deny\(unsafe|memory safety|\bnull safety\b|bounds check",
         "A05:2025", "critical", ("CWE-119",)),

        # --- A07 Authentication -------------------------------------------------
        (r"argon2|bcrypt|scrypt|pbkdf2|password hash|work factor|hashing cost",
         "A07:2025", "critical", ("CWE-916",)),
        (r"passkey|webauthn|fido2|\bmfa\b|two.factor|\b2fa\b|totp",
         "A07:2025", "high", ("CWE-308",)),
        (r"session (regenerat|fixation|rotat)|session lifecycle|logout invalidat",
         "A07:2025", "high", ("CWE-384",)),
        (r"session cookie|cookie flag|samesite|httponly|secure cookie",
         "A07:2025", "high", ("CWE-1004",)),
        (r"credential stuffing|brute.force|login throttl|lockout",
         "A07:2025", "high", ("CWE-307",)),
        (r"password (polic|validation|strength|complexity|rotation)",
         "A07:2025", "high", ("CWE-521",)),
        (r"replay|single.use challenge|challenge consumption|\brp id\b|origin verification",
         "A07:2025", "high", ("CWE-294",)),
        (r"\bjwt\b|bearer token|token expir|refresh token|sanctum|token abilit",
         "A07:2025", "high", ("CWE-287",)),
        (r"authenticat", "A07:2025", "high", ("CWE-287",)),

        # --- A01 Access control -------------------------------------------------
        (r"\bbola\b|\bidor\b|object level auth|broken object",
         "A01:2025", "critical", ("CWE-639",)),
        (r"tenant (isolat|scop)|multi.?tenan|row level security|\brls\b|cross.tenant",
         "A01:2025", "critical", ("CWE-639",)),
        (r"\bssrf\b|server.side request forgery|outbound (url|request|access)|"
         r"metadata service|169\.254|link.local|\brfc ?1918\b|loopback|private network",
         "A01:2025", "high", ("CWE-918",)),
        (r"feature.gated|server code .*(client|leak)|bundle (leak|partition)",
         "A01:2025", "high", ("CWE-200",)),
        # Only authorization-flavoured uses of "policy" belong here; bare
        # "policy" is resolved late, after CSP/CORS/network policies have had
        # their chance to match.
        # \bprivileg deliberately excludes "unprivileged", which is container
        # hardening (A02), not an authorization control.
        (r"authoriz|\bacl\b|\brbac\b|permission|\bprivileg|"
         r"(model|resource|access|tenant|eloquent|filament|authorization)\s+polic(y|ies)|"
         r"\bgate::|authorization gate",
         "A01:2025", "critical", ("CWE-285",)),
        (r"path traversal|directory traversal|\.\./",
         "A01:2025", "high", ("CWE-22",)),
        (r"mass assignment|over.?posting|\bfillable\b|\bguarded\b|strong param",
         "A01:2025", "high", ("CWE-915",)),

        # --- A05 Injection ------------------------------------------------------
        (r"sql injection|parameteriz|prepared statement|bound parameter|raw (sql|quer)",
         "A05:2025", "critical", ("CWE-89",)),
        (r"nosql injection|mongo.*inject|operator inject|\$where",
         "A05:2025", "critical", ("CWE-943",)),
        (r"command injection|shell (exec|inject)|os command",
         "A05:2025", "critical", ("CWE-78",)),
        (r"\bxss\b|cross.site scripting|output escap|html escap|sanitiz.*(html|output)",
         "A05:2025", "high", ("CWE-79",)),
        (r"template injection|\bssti\b", "A05:2025", "high", ("CWE-1336",)),
        (r"prompt injection|jailbreak|system prompt leak|boundary nonce",
         "A05:2025", "critical", ("CWE-1427",)),
        (r"inject", "A05:2025", "high", ("CWE-74",)),

        # --- A04 Cryptography ---------------------------------------------------
        (r"plaintext credential|hardcoded (secret|credential|key)|secret scan|gitleaks",
         "A04:2025", "critical", ("CWE-798",)),
        (r"encryption at rest|field.level encryp|envelope encryp|\bkms\b",
         "A04:2025", "high", ("CWE-311",)),
        (r"\btls\b|\bhttps\b|\bhsts\b|certificate|ssl",
         "A04:2025", "high", ("CWE-319",)),
        (r"key rotation|key management|api key (storage|handling)",
         "A04:2025", "high", ("CWE-320",)),
        (r"encrypt|cryptograph|cipher", "A04:2025", "high", ("CWE-311",)),

        # --- A02 Misconfiguration ----------------------------------------------
        (r"rootless|non.?root|\buser 10001\b|unprivileged (user|container)|drop capabilit",
         "A02:2025", "high", ("CWE-250",)),
        (r"security header|content.security.policy|\bcsp\b|x-frame-options|frame.ancestors",
         "A02:2025", "medium", ("CWE-693",)),
        (r"\bcors\b|cross.origin", "A02:2025", "high", ("CWE-942",)),
        (r"debug (mode|surface)|app_debug|stack trace.*(disabl|product)|verbose error",
         "A02:2025", "high", ("CWE-489",)),
        (r"read.only (root|filesystem)|seccomp|apparmor|no.new.privileges",
         "A02:2025", "medium", ("CWE-250",)),
        (r"allowed_hosts|trusted (host|prox)|wildcard host",
         "A02:2025", "medium", ("CWE-16",)),
        (r"strict (sql )?mode|sql_mode|strict_trans_tables",
         "A02:2025", "medium", ("CWE-16",)),
        (r"misconfigur|hardening|secure default|\.env|environment variable",
         "A02:2025", "medium", ("CWE-16",)),

        # --- A03 Supply chain ---------------------------------------------------
        (r"lock ?file|pinned (dependenc|version|digest)|pin.*image|checksum verif",
         "A03:2025", "high", ("CWE-1357",)),
        (r"dependabot|renovate|dependency (audit|scan|review)|composer audit|npm audit|cargo.audit|pip.audit",
         "A03:2025", "high", ("CWE-1104",)),
        (r"\bsbom\b|provenance|sigstore|cosign|artifact sign",
         "A03:2025", "high", ("CWE-1357",)),
        (r"supply chain|typosquat|registry", "A03:2025", "high", ("CWE-1357",)),

        # --- A06 Insecure design ------------------------------------------------
        (r"rate limit|throttl|quota|cost (cap|ceiling|guard)|spend limit|token budget",
         "A06:2025", "high", ("CWE-770",)),
        (r"pagination (bound|clamp|limit)|max (page|result|payload)|request size limit|body limit",
         "A06:2025", "medium", ("CWE-770",)),
        (r"timeout|slowloris|connection (pool|starvation)|circuit breaker",
         "A06:2025", "medium", ("CWE-400",)),
        (r"sandbox|isolation boundary|egress (control|allowlist)|network polic",
         "A06:2025", "high", ("CWE-653",)),
        (r"threat model|secure design|defense in depth",
         "A06:2025", "medium", ("CWE-1053",)),
        (r"\bpii\b|redact|data minimi|personal data|anonymi",
         "A06:2025", "high", ("CWE-359",)),
        (r"\bcsrf\b|cross.site request forgery|state.changing request",
         "A06:2025", "high", ("CWE-352",)),
        (r"file upload|mime (type|sniff)|upload (validat|restrict)",
         "A06:2025", "high", ("CWE-434",)),

        # --- A08 Integrity ------------------------------------------------------
        (r"deserializ|pickle|unmarshal|yaml\.load",
         "A08:2025", "critical", ("CWE-502",)),
        (r"migration (revers|backward|zero.downtime)|schema drift",
         "A08:2025", "medium", ("CWE-1059",)),
        (r"webhook signature|payload signature|\bhmac\b|integrity check",
         "A08:2025", "high", ("CWE-345",)),
        (r"backdoor|rules (tamper|integrity)|agent rule scan",
         "A08:2025", "critical", ("CWE-506",)),
        (r"integrity", "A08:2025", "high", ("CWE-345",)),

        # --- A09 Logging --------------------------------------------------------
        (r"audit (log|trail)|activity log|immutable log",
         "A09:2025", "high", ("CWE-778",)),
        (r"log (redact|scrub|sanitiz)|secret.*log|sensitive data.*log|"
         r"sensitive parameter filtering|filter_parameters",
         "A09:2025", "high", ("CWE-532",)),
        (r"alert|monitor|observab|structured log|correlation id|trace id",
         "A09:2025", "medium", ("CWE-778",)),
        (r"logging", "A09:2025", "medium", ("CWE-778",)),

        # --- A10 Exceptional conditions ----------------------------------------
        (r"error (boundary|handling|envelope)|unified .*error|fail.(closed|open)|panic handl",
         "A10:2025", "medium", ("CWE-755",)),
        (r"health.?check|health (probe)|healthz|liveness|readiness|graceful (shutdown|degrad)",
         "A10:2025", "low", ("CWE-755",)),
        (r"exception|unwrap|error disclosure",
         "A10:2025", "medium", ("CWE-209",)),

        # --- Stack-specific controls -------------------------------------------
        # Resource exhaustion and runaway execution (A06).
        (r"recursi(on|ve)|cycl(e|ic) limit|max (iteration|depth|step)|loop bound",
         "A06:2025", "high", ("CWE-674",)),
        (r"payload size|body size limit|max request|size cap|capping",
         "A06:2025", "medium", ("CWE-770",)),
        (r"\bttl\b|expir(y|ation) (key|invariant)|cache isolation|broker config",
         "A06:2025", "medium", ("CWE-613",)),
        (r"\bwal\b mode|non.blocking concurrency|supervisor isolation|process isolation",
         "A06:2025", "medium", ("CWE-662",)),
        (r"compos(ite|ed) index|compound index|b.?tree index|collscan|index .*(guard|performance)",
         "A06:2025", "low", ("CWE-1049",)),
        (r"race|buffer copy|pointer race|data race",
         "A06:2025", "high", ("CWE-362",)),
        (r"airgap|zero.outbound|network isolation|internal network",
         "A06:2025", "high", ("CWE-653",)),
        (r"hallucinat|groundedness|faithfulness|relevancy (score|guardrail)",
         "A06:2025", "high", ("CWE-1426",)),
        (r"token.light|efficiency (tier|verification)",
         "A06:2025", "low", ("CWE-1050",)),

        # Serialization, migration and state integrity (A08).
        (r"serializ", "A08:2025", "high", ("CWE-502",)),
        (r"atomic (transaction|database)|transaction(al)? (integrity|boundar)|"
         r"transaction wrapping|wrapped in .{0,12}transaction|compound write",
         "A08:2025", "medium", ("CWE-662",)),
        (r"cascade on delete|foreign key|orphan(ed)? (record|row|database)|constraint migration",
         "A08:2025", "medium", ("CWE-1059",)),
        (r"consistency check|index consistency|dedup|content hash|manifest .*hash|static hash",
         "A08:2025", "medium", ("CWE-345",)),
        (r"type verification|schema conformance|json.rpc",
         "A08:2025", "medium", ("CWE-1287",)),

        # Error paths and failure handling (A10).
        (r"panic recover|deadlock|poison message|retry (safety|loop)|error code sanitiz",
         "A10:2025", "medium", ("CWE-755",)),

        # Configuration hardening (A02).
        (r"security middleware|deploy (security )?audit|security audit|check --deploy",
         "A02:2025", "high", ("CWE-16",)),
        (r"charset|collation|utf8mb4|character set",
         "A02:2025", "low", ("CWE-16",)),
        (r"non.executable stack|\bnx\b/\bdep\b|\baslr\b|stack canar|relro|pie\b",
         "A02:2025", "medium", ("CWE-693",)),

        # Credentials and keys (A04).
        (r"plaintext|secret key from environment|zero .*(secret|credential)",
         "A04:2025", "critical", ("CWE-798",)),

        # Identity (A07).
        (r"\bpkce\b|session (refresh|verification)|oauth flow",
         "A07:2025", "high", ("CWE-287",)),

        # Access control (A01).
        (r"changeset (param|filter)|uuid primary key|non.enumerable id",
         "A01:2025", "high", ("CWE-915",)),

        # Injection sinks (A05).
        (r"\beval\b|\bexec\b|dynamic execution|execution sink|safe math|query evaluation",
         "A05:2025", "critical", ("CWE-95",)),
        (r"sanitiz", "A05:2025", "high", ("CWE-20",)),

        # Supply chain (A03).
        (r"\bcves?\b|vulnerability (audit|scan)|hex\.audit|safety check",
         "A03:2025", "high", ("CWE-1104",)),
        (r"pre.commit|pre.flight|security gat(e|ing)|non.zero status|ci (gate|block)|"
         r"simulation script",
         "A03:2025", "high", ("CWE-1357",)),

        # Reporting and alerting pipelines (A09).
        (r"\bsarif\b|code scanning|security report|finding (export|upload)",
         "A09:2025", "medium", ("CWE-778",)),

        # Query efficiency guards that double as DoS protection (A06).
        (r"strict loading|n\+1|eager load",
         "A06:2025", "low", ("CWE-1049",)),

        # Build output hygiene (A02).
        (r"wasm.?opt|strip(ping)? debug|debug metadata|source ?map",
         "A02:2025", "medium", ("CWE-489",)),

        # --- Broad fallbacks ----------------------------------------------------
        (r"validat|schema (enforc|bound)|input bound|strict (type|coercion)|zod|pydantic",
         "A05:2025", "high", ("CWE-20",)),
        (r"semgrep|static .{0,16}analysis|\bsast\b|lint.*security|sobelow|bandit|brakeman",
         "A03:2025", "medium", ("CWE-1357",)),
        (r"egress|allowlist|whitelist",
         "A06:2025", "high", ("CWE-653",)),
        (r"isolation|guardrail",
         "A06:2025", "medium", ("CWE-653",)),
        # Resolved last so more specific policy kinds (CSP, CORS, network,
        # retention) are claimed by their own categories first.
        (r"polic(y|ies)", "A01:2025", "high", ("CWE-285",)),
    )
)


class Classification(NamedTuple):
    owasp: list[str]
    severity: str
    cwe: list[str]
    confident: bool


def classify(*fields: str) -> Classification:
    """Infer OWASP category, severity and CWE from a control's descriptive text.

    Returns ``confident=False`` when no rule matched, so callers can surface the
    control for manual review instead of silently mis-tagging it.
    """
    text = " ".join(f for f in fields if f)
    for pattern, owasp, severity, cwes in _RULES:
        if pattern.search(text):
            return Classification([owasp], severity, list(cwes), True)
    return Classification([], "medium", [], False)


def coverage(owasp_ids: list[str]) -> dict[str, bool]:
    """Map every 2025 category to whether the supplied ids cover it."""
    present = set(owasp_ids)
    return {c.id: c.id in present for c in CATEGORIES}
