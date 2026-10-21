-- name: GetUser :one
SELECT id, email, full_name, created_at FROM users
WHERE id = $1 LIMIT 1;

-- name: ListUsers :many
SELECT id, email, full_name, created_at FROM users
ORDER BY created_at DESC LIMIT 50;

-- name: CreateUser :one
INSERT INTO users (email, full_name)
VALUES ($1, $2)
RETURNING id, email, full_name, created_at;
