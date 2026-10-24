"""Security controls declared in security/checks.json, verified.

The functional suite uses Django's default test client, which bypasses CSRF so
routes can be called directly. These tests build a client with
`enforce_csrf_checks=True`, because a suite that disables a protection cannot
also prove it works.
"""

import io
import json
import os
import re
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.contrib.auth.password_validation import validate_password
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from app.models import Item

STARTER = Path(__file__).resolve().parent.parent


# --- SEC-04: CSRF enforcement (A06:2025, CWE-352) -------------------------

class CsrfProtectionTest(TestCase):
    def setUp(self):
        self.strict = Client(enforce_csrf_checks=True)

    def test_post_without_csrf_token_is_rejected(self):
        res = self.strict.post(reverse('app:item_create'), {'title': 'No token'})
        self.assertEqual(res.status_code, 403, 'CSRF middleware did not reject a tokenless POST')

    def test_toggle_without_csrf_token_is_rejected(self):
        item = Item.objects.create(title='Guarded')
        res = self.strict.post(reverse('app:item_toggle', args=[item.pk]))
        self.assertEqual(res.status_code, 403)

    def test_csrf_middleware_is_installed(self):
        self.assertIn('django.middleware.csrf.CsrfViewMiddleware', settings.MIDDLEWARE)


# --- SEC-05: parameterized ORM access (A05:2025, CWE-89) ------------------

class SqlInjectionTest(TestCase):
    def test_quote_breaking_filter_is_treated_as_a_literal(self):
        Item.objects.create(title='Legitimate record')
        hits = Item.objects.filter(title__icontains="' OR 1=1 --")
        self.assertEqual(hits.count(), 0, 'filter value was interpreted rather than bound')

    def test_injection_payload_cannot_drop_the_table(self):
        Item.objects.create(title='Survivor')
        list(Item.objects.filter(title__icontains="'; DROP TABLE app_item; --"))
        self.assertEqual(Item.objects.count(), 1, 'table was damaged by an injection payload')

    def test_orm_emits_bound_parameters(self):
        query = str(Item.objects.filter(title="x' OR '1'='1").query)
        self.assertNotIn('DROP', query.upper())


# --- SEC-07: template autoescaping (A05:2025, CWE-79) ---------------------

class XssProtectionTest(TestCase):
    def test_stored_script_payload_is_escaped_on_render(self):
        Item.objects.create(title="<script>alert('xss')</script>")
        body = self.client.get(reverse('app:item_list')).content
        self.assertNotIn(b"<script>alert(", body, 'stored XSS rendered unescaped')
        self.assertIn(b'&lt;script&gt;', body, 'payload was not HTML-escaped')

    def test_autoescape_is_not_disabled(self):
        options = settings.TEMPLATES[0].get('OPTIONS', {})
        self.assertNotEqual(options.get('autoescape'), False)


# --- SEC-08 / SEC-09: response and cookie hardening (A02, A07:2025) -------

class ResponseHardeningTest(TestCase):
    def test_x_frame_options_denies_framing(self):
        res = self.client.get(reverse('app:item_list'))
        self.assertEqual(res.headers.get('X-Frame-Options'), 'DENY')

    def test_content_type_nosniff_is_sent(self):
        res = self.client.get(reverse('app:item_list'))
        self.assertEqual(res.headers.get('X-Content-Type-Options'), 'nosniff')

    def test_referrer_policy_is_set(self):
        res = self.client.get(reverse('app:item_list'))
        self.assertEqual(res.headers.get('Referrer-Policy'), 'strict-origin-when-cross-origin')

    def test_session_cookie_flags(self):
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)
        self.assertEqual(settings.SESSION_COOKIE_SAMESITE, 'Lax')

    def test_security_middleware_is_first(self):
        self.assertEqual(settings.MIDDLEWARE[0], 'django.middleware.security.SecurityMiddleware')


# --- SEC-03: deploy audit is clean in production config (A02:2025) --------

class DeployAuditTest(TestCase):
    @override_settings(
        DEBUG=False,
        ALLOWED_HOSTS=['example.com'],
        SECRET_KEY='production-grade-secret-key-of-at-least-fifty-characters-abc',
        SECURE_SSL_REDIRECT=True,
        SESSION_COOKIE_SECURE=True,
        CSRF_COOKIE_SECURE=True,
        SECURE_HSTS_SECONDS=31536000,
        SECURE_HSTS_INCLUDE_SUBDOMAINS=True,
        SECURE_HSTS_PRELOAD=True,
    )
    def test_check_deploy_reports_no_issues(self):
        buffer = io.StringIO()
        call_command('check', '--deploy', stdout=buffer, stderr=buffer)
        self.assertIn('no issues', buffer.getvalue())

    def test_wildcard_allowed_hosts_is_refused_in_production(self):
        """A wildcard host with DEBUG off must raise, not warn."""
        source = (STARTER / 'config' / 'settings.py').read_text(encoding='utf-8')
        self.assertIn('ImproperlyConfigured', source)
        self.assertIn('Host header poisoning', source)


# --- SEC-06: manifest static storage (A08:2025, CWE-345) ------------------

class StaticStorageTest(TestCase):
    def test_production_uses_manifest_hashed_storage(self):
        source = (STARTER / 'config' / 'settings.py').read_text(encoding='utf-8')
        self.assertIn('CompressedManifestStaticFilesStorage', source)

    def test_whitenoise_middleware_follows_security_middleware(self):
        mw = settings.MIDDLEWARE
        self.assertIn('whitenoise.middleware.WhiteNoiseMiddleware', mw)
        self.assertLess(
            mw.index('django.middleware.security.SecurityMiddleware'),
            mw.index('whitenoise.middleware.WhiteNoiseMiddleware'),
        )


# --- SEC-10: composite indexes (A06:2025, CWE-1049) -----------------------

class IndexTest(TestCase):
    def test_composite_index_on_completion_and_recency(self):
        combos = [tuple(i.fields) for i in Item._meta.indexes]
        self.assertIn(('is_completed', '-created_at'), combos)

    def test_priority_is_indexed(self):
        combos = [tuple(i.fields) for i in Item._meta.indexes]
        self.assertIn(('priority',), combos)


# --- SEC-11: password policy (A07:2025, CWE-521) --------------------------

class PasswordPolicyTest(TestCase):
    def test_all_four_validators_are_configured(self):
        names = {v['NAME'].rsplit('.', 1)[-1] for v in settings.AUTH_PASSWORD_VALIDATORS}
        self.assertEqual(names, {
            'UserAttributeSimilarityValidator', 'MinimumLengthValidator',
            'CommonPasswordValidator', 'NumericPasswordValidator',
        })

    def test_common_password_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_password('password')

    def test_all_numeric_password_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_password('84736451')

    def test_strong_password_is_accepted(self):
        validate_password('c8rrect-h0rse-b4ttery-stapl3')


# --- SEC-01 / SEC-12: secrets and dependency pinning (A04, A03:2025) ------

class SupplyChainTest(TestCase):
    def test_env_example_holds_no_real_secret(self):
        content = (STARTER / '.env.example').read_text(encoding='utf-8')
        self.assertFalse(content.startswith('﻿'), '.env.example starts with a UTF-8 BOM')
        for line in content.splitlines():
            if line.startswith('SECRET_KEY='):
                value = line.split('=', 1)[1].lower()
                self.assertTrue(
                    any(token in value for token in ('change', 'your', 'insecure', 'dev')),
                    'SECRET_KEY in .env.example looks like a real secret',
                )

    def test_no_hardcoded_credentials_in_source(self):
        patterns = [
            re.compile(r'AKIA[0-9A-Z]{16}'),
            re.compile(r'\bsk-[A-Za-z0-9_-]{20,}'),
            re.compile(r'BEGIN RSA PRIVATE KEY'),  # pragma: allowlist secret
        ]
        for path in STARTER.rglob('*.py'):
            if '__pycache__' in str(path) or path.name == 'test_security.py':
                continue
            text = path.read_text(encoding='utf-8', errors='ignore')
            for pattern in patterns:
                self.assertIsNone(pattern.search(text), f'credential-shaped literal in {path.name}')

    def test_every_dependency_is_version_pinned(self):
        for line in (STARTER / 'requirements.txt').read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                self.assertRegex(line, r'[><=~]=', f'unpinned dependency: {line}')
