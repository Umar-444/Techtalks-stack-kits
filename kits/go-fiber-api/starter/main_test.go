package main

import (
	"bytes"
	"encoding/json"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
)

func TestHealthEndpoint(t *testing.T) {
	app := setupApp()

	req := httptest.NewRequest("GET", "/health", nil)
	resp, err := app.Test(req, 2000)
	if err != nil {
		t.Fatalf("unexpected error during request: %v", err)
	}

	if resp.StatusCode != 200 {
		t.Fatalf("expected status 200, got %d", resp.StatusCode)
	}

	buf := new(bytes.Buffer)
	_, _ = buf.ReadFrom(resp.Body)
	body := buf.String()

	if !strings.Contains(body, `"status":"ok"`) {
		t.Errorf("expected status ok in body, got: %s", body)
	}
	if !strings.Contains(body, `"framework":"fiber"`) {
		t.Errorf("expected framework fiber, got: %s", body)
	}
}

func TestCORSPolicy(t *testing.T) {
	_ = os.Setenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080")
	app := setupApp()

	req := httptest.NewRequest("OPTIONS", "/api/v1/bench", nil)
	req.Header.Set("Origin", "http://localhost:3000")
	req.Header.Set("Access-Control-Request-Method", "GET")

	resp, err := app.Test(req, 2000)
	if err != nil {
		t.Fatalf("unexpected error during request: %v", err)
	}

	if resp.StatusCode != 204 {
		t.Fatalf("expected status 204 for OPTIONS preflight, got %d", resp.StatusCode)
	}
	if resp.Header.Get("Access-Control-Allow-Origin") != "http://localhost:3000" {
		t.Errorf("expected CORS origin header set, got %s", resp.Header.Get("Access-Control-Allow-Origin"))
	}
}

func TestBenchAndRecordsEndpoints(t *testing.T) {
	app := setupApp()

	// 1. Benchmark route
	req := httptest.NewRequest("GET", "/api/v1/bench", nil)
	resp, _ := app.Test(req, 2000)
	if resp.StatusCode != 200 {
		t.Fatalf("expected status 200 on bench, got %d", resp.StatusCode)
	}

	// 2. Post record
	payload := map[string]string{
		"key":   "telemetry-sensor",
		"value": "24.5C",
	}
	bodyBytes, _ := json.Marshal(payload)
	postReq := httptest.NewRequest("POST", "/api/v1/records", bytes.NewBuffer(bodyBytes))
	postReq.Header.Set("Content-Type", "application/json")
	postResp, _ := app.Test(postReq, 2000)

	if postResp.StatusCode != 201 {
		t.Fatalf("expected status 201 on record create, got %d", postResp.StatusCode)
	}
}
