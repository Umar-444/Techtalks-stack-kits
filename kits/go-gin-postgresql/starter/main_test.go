package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
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
	if !strings.Contains(body, `"framework":"gin"`) {
		t.Errorf("expected framework gin, got: %s", body)
	}
}

func TestCORSPolicy(t *testing.T) {
	_ = os.Setenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080")
	router := setupRouter()

	req := httptest.NewRequest("OPTIONS", "/api/v1/users", nil)
	req.Header.Set("Origin", "http://localhost:3000")
	rec := httptest.NewRecorder()

	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusNoContent {
		t.Fatalf("expected status 204 for OPTIONS, got %d", rec.Code)
	}
	if rec.Header().Get("Access-Control-Allow-Origin") != "http://localhost:3000" {
		t.Errorf("expected CORS origin header set, got %s", rec.Header().Get("Access-Control-Allow-Origin"))
	}
}

func TestUsersEndpoint(t *testing.T) {
	router := setupRouter()

	// 1. List users
	req := httptest.NewRequest("GET", "/api/v1/users", nil)
	rec := httptest.NewRecorder()
	router.ServeHTTP(rec, req)

	if rec.Code != http.StatusOK {
		t.Fatalf("expected status 200, got %d", rec.Code)
	}

	// 2. Create user valid
	payload := map[string]string{
		"email": "engineer@techtalks.dev",
		"name":  "Staff SRE",
	}
	bodyBytes, _ := json.Marshal(payload)
	postReq := httptest.NewRequest("POST", "/api/v1/users", bytes.NewBuffer(bodyBytes))
	postReq.Header.Set("Content-Type", "application/json")
	postRec := httptest.NewRecorder()
	router.ServeHTTP(postRec, postReq)

	if postRec.Code != http.StatusCreated {
		t.Fatalf("expected status 201 for user creation, got %d", postRec.Code)
	}
}
