package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
)

type User struct {
	ID        int64     `json:"id"`
	Email     string    `json:"email"`
	Name      string    `json:"name"`
	Role      string    `json:"role"`
	CreatedAt time.Time `json:"created_at"`
}

func CORSMiddleware() gin.HandlerFunc {
	rawOrigins := os.Getenv("ALLOWED_ORIGINS")
	if rawOrigins == "" {
		rawOrigins = "http://localhost:3000,http://localhost:8080"
	}
	allowedOrigins := strings.Split(rawOrigins, ",")
	allowedMap := make(map[string]bool)
	for _, o := range allowedOrigins {
		trimmed := strings.TrimSpace(o)
		if trimmed != "" {
			allowedMap[trimmed] = true
		}
	}

	return func(c *gin.Context) {
		origin := c.Request.Header.Get("Origin")
		if allowedMap[origin] {
			c.Writer.Header().Set("Access-Control-Allow-Origin", origin)
			c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
			c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
			c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, DELETE")
		}

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(http.StatusNoContent)
			return
		}

		c.Next()
	}
}

func setupRouter() *gin.Engine {
	gin.SetMode(gin.ReleaseMode)
	r := gin.New()

	r.Use(gin.Recovery())
	r.Use(CORSMiddleware())

	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":    "ok",
			"framework": "gin",
			"database":  "postgresql",
			"cache":     "redis",
			"version":   "1.0.0",
		})
	})

	api := r.Group("/api/v1")
	{
		api.GET("/users", func(c *gin.Context) {
			mockUsers := []User{
				{ID: 1, Email: "lead@techtalks.dev", Name: "Staff Engineer", Role: "admin", CreatedAt: time.Now().UTC()},
				{ID: 2, Email: "agent@techtalks.dev", Name: "AI Agent", Role: "engineer", CreatedAt: time.Now().UTC()},
			}
			c.JSON(http.StatusOK, gin.H{
				"data":  mockUsers,
				"count": len(mockUsers),
			})
		})

		api.POST("/users", func(c *gin.Context) {
			var input struct {
				Email string `json:"email" binding:"required,email"`
				Name  string `json:"name" binding:"required,min=2"`
			}
			if err := c.ShouldBindJSON(&input); err != nil {
				c.JSON(http.StatusUnprocessableEntity, gin.H{"error": err.Error()})
				return
			}
			newUser := User{
				ID:        time.Now().Unix(),
				Email:     input.Email,
				Name:      input.Name,
				Role:      "user",
				CreatedAt: time.Now().UTC(),
			}
			c.JSON(http.StatusCreated, gin.H{"data": newUser})
		})
	}

	return r
}

func main() {
	r := setupRouter()

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	srv := &http.Server{
		Addr:         ":" + port,
		Handler:      r,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	go func() {
		log.Printf("Go Gin server running on :%s", port)
		// nosemgrep: go.lang.security.audit.net.use-tls.use-tls
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen error: %s\n", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down server gracefully...")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server forced shutdown:", err)
	}
	log.Println("Server exiting successfully")
}
