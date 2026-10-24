# syntax=docker/dockerfile:1
# Laravel 12/13 + Filament + PostgreSQL 16 — hardened multi-stage image.
# Runs as UID 10001; see security/checks.json control OPS-02.

# ---------------------------------------------------------------------------
# Stage 1 — build PHP extensions and resolve Composer dependencies.
# ---------------------------------------------------------------------------
FROM php:8.4-cli-alpine AS vendor

RUN apk add --no-cache --virtual .build-deps \
        $PHPIZE_DEPS \
        postgresql-dev \
        libzip-dev \
        icu-dev \
        linux-headers \
    && docker-php-ext-install -j"$(nproc)" \
        pdo_pgsql \
        zip \
        intl \
        pcntl \
        bcmath \
        opcache \
    && pecl install redis \
    && docker-php-ext-enable redis

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /app

# Install dependencies against the lockfile alone so this layer is reused
# whenever application source changes but dependencies do not.
COPY composer.json composer.loc[k] ./
RUN composer install \
        --no-dev \
        --no-scripts \
        --no-autoloader \
        --prefer-dist \
        --no-interaction

COPY . .
RUN composer dump-autoload --optimize --classmap-authoritative

# ---------------------------------------------------------------------------
# Stage 2 — runtime. No compilers, no Composer, no build headers.
# ---------------------------------------------------------------------------
FROM php:8.4-cli-alpine AS runtime

RUN apk add --no-cache \
        postgresql-libs \
        libzip \
        icu-libs \
        curl \
    && addgroup -g 10001 appgroup \
    && adduser -u 10001 -G appgroup -s /bin/sh -D appuser

COPY --from=vendor /usr/local/lib/php/extensions/ /usr/local/lib/php/extensions/
COPY --from=vendor /usr/local/etc/php/conf.d/ /usr/local/etc/php/conf.d/

WORKDIR /var/www/html

COPY --from=vendor --chown=10001:10001 /app /var/www/html

# Laravel needs these two writable; everything else stays read-only.
RUN mkdir -p storage/framework/{cache,sessions,views} storage/logs bootstrap/cache \
    && chown -R 10001:10001 storage bootstrap/cache

USER 10001:10001

ENV APP_ENV=production \
    APP_DEBUG=false \
    LOG_CHANNEL=stderr

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
    CMD curl -fsS http://127.0.0.1:8000/up || exit 1

CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
