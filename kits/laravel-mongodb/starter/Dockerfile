FROM php:8.4-cli-alpine

# Install system build dependencies and MongoDB PECL extension
RUN apk add --no-cache     $PHPIZE_DEPS     openssl-dev     git     unzip     curl     && pecl install mongodb     && pecl install redis     && docker-php-ext-enable mongodb redis

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

EXPOSE 8000
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=8000"]
