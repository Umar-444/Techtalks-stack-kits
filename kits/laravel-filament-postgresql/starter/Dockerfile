FROM php:8.4-cli-alpine AS base

# Install system dependencies and PostgreSQL PDO drivers
RUN apk add --no-cache \
    postgresql-dev \
    libzip-dev \
    icu-dev \
    git \
    unzip \
    curl \
    linux-headers \
    $PHPIZE_DEPS \
    && docker-php-ext-install pdo_pgsql zip intl pcntl bcmath opcache \
    && pecl install redis \
    && docker-php-ext-enable redis

# Install Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

EXPOSE 8000
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
