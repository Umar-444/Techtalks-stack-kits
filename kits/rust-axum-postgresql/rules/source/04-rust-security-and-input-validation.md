---
id: 04-rust-security-and-input-validation
title: Memory Safety, Deserialization Limits, and Supply Chain Auditing
globs: "starter/**/*.rs,starter/Cargo.toml"
alwaysApply: true
---

# Memory Safety, Deserialization Limits, and Supply Chain Auditing

## 1. Zero Unsafe Code
- The codebase enforces `#![deny(unsafe_code)]`. Memory safety is guaranteed by Rust's ownership and borrow checker.

## 2. Request Deserialization Bounds
- Protect against memory exhaustion denial-of-service by imposing payload size limits:
  `app.layer(DefaultBodyLimit::max(2 * 1024 * 1024))` (2MB maximum request body).
- Validate input structs with custom validation functions or the `validator` crate.

## 3. Continuous Supply Chain Auditing
- Run `cargo audit` in CI to detect vulnerabilities in third-party dependencies (`Cargo.lock`).
- Maintain `cargo deny` checks to enforce permissive software licenses and avoid duplicate crates.
