package main

import (
    "log"
    "github.com/gofiber/fiber/v3"
)

func main() {
    app := fiber.New()
    app.Get("/health", func(c fiber.Ctx) error {
        return c.JSON(fiber.Map{"status": "ok", "engine": "fasthttp"})
    })
    log.Fatal(app.Listen(":8080"))
}
