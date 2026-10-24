FROM php:8.4-cli-alpine
RUN apk add --no-cache postgresql-dev libzip-dev git unzip curl && docker-php-ext-install pdo_pgsql zip \
    && addgroup -g 10001 appgroup && adduser -u 10001 -G appgroup -s /bin/sh -D appuser
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
WORKDIR /var/www/html
USER 10001:10001
EXPOSE 8000
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
