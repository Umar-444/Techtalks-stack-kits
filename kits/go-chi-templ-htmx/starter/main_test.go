package main

import (
    "net/http"
    "net/http/httptest"
    "strings"
    "testing"
)

func TestHealthEndpoint(t *testing.T) {
    router := setupRouter()
    req := httptest.NewRequest("GET", "/health", nil)
    rec := httptest.NewRecorder()

    router.ServeHTTP(rec, req)

    if rec.Code != http.StatusOK {
        t.Fatalf("expected status 200, got %d", rec.Code)
    }

    body := rec.Body.String()
    if !strings.Contains(body, `"status":"ok"`) {
        t.Errorf("expected status ok in body, got: %s", body)
    }
    if !strings.Contains(body, `"token_light":true`) {
        t.Errorf("expected token_light true, got: %s", body)
    }
}

func TestRootEndpoint(t *testing.T) {
    router := setupRouter()
    req := httptest.NewRequest("GET", "/", nil)
    rec := httptest.NewRecorder()

    router.ServeHTTP(rec, req)

    if rec.Code != http.StatusOK {
        t.Fatalf("expected status 200, got %d", rec.Code)
    }

    body := rec.Body.String()
    if !strings.Contains(body, "Go + Chi + templ + HTMX") {
        t.Errorf("expected title in body, got: %s", body)
    }
}
