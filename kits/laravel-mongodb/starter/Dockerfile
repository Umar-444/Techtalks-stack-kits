FROM php:8.4-cli-alpine
RUN apk add --no-cache $PHPIZE_DEPS openssl-dev git unzip && pecl install mongodb && docker-php-ext-enable mongodb
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
WORKDIR /var/www/html
EXPOSE 8000
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
