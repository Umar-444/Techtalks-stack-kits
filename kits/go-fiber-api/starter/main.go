package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/fiber/v2/middleware/recover"
)

type Record struct {
	ID        int64     `json:"id"`
	Key       string    `json:"key"`
	Value     string    `json:"value"`
	CreatedAt time.Time `json:"created_at"`
}

func setupApp() *fiber.App {
	app := fiber.New(fiber.Config{
		AppName:      "Go Fiber High-Throughput API",
		ServerHeader: "Fiber",
		BodyLimit:    4 * 1024 * 1024,
	})

	app.Use(recover.New())
	app.Use(logger.New())

	// Strict CORS whitelist from environment
	rawOrigins := os.Getenv("ALLOWED_ORIGINS")
	if rawOrigins == "" {
		rawOrigins = "http://localhost:3000,http://localhost:8080"
	}
	app.Use(cors.New(cors.Config{
		AllowOrigins:     rawOrigins,
		AllowCredentials: true,
		AllowHeaders:     "Origin, Content-Type, Accept, Authorization",
		AllowMethods:     "GET, POST, HEAD, PUT, DELETE, PATCH, OPTIONS",
	}))

	app.Get("/health", func(c *fiber.Ctx) error {
		return c.Status(fiber.StatusOK).JSON(fiber.Map{
			"status":    "ok",
			"framework": "fiber",
			"engine":    "fasthttp",
			"version":   "1.0.0",
		})
	})

	api := app.Group("/api/v1")
	{
		api.Get("/bench", func(c *fiber.Ctx) error {
			return c.Status(fiber.StatusOK).JSON(fiber.Map{
				"throughput": "ultra-high",
				"allocations": "zero",
				"timestamp":  time.Now().UnixNano(),
			})
		})

		api.Get("/records", func(c *fiber.Ctx) error {
			records := []Record{
				{ID: 1, Key: "cluster-status", Value: "active", CreatedAt: time.Now().UTC()},
				{ID: 2, Key: "node-capacity", Value: "99.8%", CreatedAt: time.Now().UTC()},
			}
			return c.Status(fiber.StatusOK).JSON(fiber.Map{
				"data":  records,
				"count": len(records),
			})
		})

		api.Post("/records", func(c *fiber.Ctx) error {
			var input struct {
				Key   string `json:"key"`
				Value string `json:"value"`
			}
			if err := c.BodyParser(&input); err != nil {
				return c.Status(fiber.StatusUnprocessableEntity).JSON(fiber.Map{
					"error": "malformed json body",
				})
			}
			if strings.TrimSpace(input.Key) == "" {
				return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
					"error": "key is required",
				})
			}

			// Buffer safety: copy strings when passing beyond handler lifecycle
			keyCopy := strings.Clone(input.Key)
			valCopy := strings.Clone(input.Value)

			rec := Record{
				ID:        time.Now().Unix(),
				Key:       keyCopy,
				Value:     valCopy,
				CreatedAt: time.Now().UTC(),
			}
			return c.Status(fiber.StatusCreated).JSON(fiber.Map{"data": rec})
		})
	}

	return app
}

func main() {
	app := setupApp()

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	go func() {
		log.Printf("Fiber server listening on :%s", port)
		// nosemgrep: go.lang.security.audit.net.use-tls.use-tls
		if err := app.Listen(":" + port); err != nil {
			log.Printf("server error: %v", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Gracefully terminating Fiber application...")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := app.ShutdownWithContext(ctx); err != nil {
		log.Fatalf("Fiber shutdown error: %v", err)
	}
	log.Println("Server exiting successfully")
}
