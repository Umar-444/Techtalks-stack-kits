FROM php:8.3-fpm-alpine

RUN apk add --no-cache \
    mysql-client \
    libpng-dev \
    libjpeg-turbo-dev \
    freetype-dev \
    libzip-dev \
    zip \
    unzip \
    git \
    curl

RUN docker-php-ext-install pdo pdo_mysql bcmath zip

COPY --from=composer:2.7 /usr/bin/composer /usr/bin/composer

# Non-root unprivileged user (UID/GID 10001)
RUN addgroup -g 10001 appgroup && \
    adduser -u 10001 -G appgroup -s /bin/sh -D appuser

WORKDIR /var/www/html

COPY --chown=appuser:appgroup . .

USER 10001:10001

EXPOSE 9000
CMD ["php-fpm"]
