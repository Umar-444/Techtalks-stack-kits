# Multi-stage production container for Laravel 11/12 + MySQL 8.4
FROM php:8.4-fpm-alpine AS base

WORKDIR /var/www/html

RUN apk add --no-cache \
    curl \
    git \
    libpng-dev \
    libxml2-dev \
    zip \
    unzip \
    oniguruma-dev \
    icu-dev \
    linux-headers

RUN docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd intl opcache

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

RUN addgroup -S appgroup -g 10001 && \
    adduser -S appuser -u 10001 -G appgroup

COPY composer.json composer.lock* ./
RUN composer install --no-dev --no-scripts --prefer-dist --no-autoloader || true

COPY . .
RUN chown -R appuser:appgroup /var/www/html

USER appuser

EXPOSE 9000
CMD ["php-fpm"]
