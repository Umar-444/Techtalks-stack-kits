FROM php:8.4-cli-alpine
RUN apk add --no-cache postgresql-dev libzip-dev git unzip curl && docker-php-ext-install pdo_pgsql zip
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
WORKDIR /var/www/html
EXPOSE 8000
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
