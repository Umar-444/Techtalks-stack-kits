# Multi-stage production Dockerfile for Ruby on Rails 8 Hotwire
FROM ruby:3.3.6-alpine AS base

WORKDIR /rails

RUN apk add --no-cache \
    build-base \
    gcompat \
    git \
    postgresql-dev \
    sqlite-dev \
    tzdata \
    yaml-dev \
    zlib-dev

ENV RAILS_ENV=production \
    BUNDLE_DEPLOYMENT=1 \
    BUNDLE_PATH=/usr/local/bundle \
    BUNDLE_WITHOUT="development:test"

FROM base AS build

COPY Gemfile Gemfile.lock* ./
RUN bundle install && \
    rm -rf ~/.bundle/ "${BUNDLE_PATH}"/ruby/*/cache "${BUNDLE_PATH}"/ruby/*/bundler/gems/*/.git

COPY . .

RUN bundle exec bootsnap precompile --gemfile app/ lib/ || true

FROM base AS final

COPY --from=build "${BUNDLE_PATH}" "${BUNDLE_PATH}"
COPY --from=build /rails /rails

RUN addgroup --system --gid 1000 rails && \
    adduser --system --uid 1000 --ingroup rails rails && \
    chown -R rails:rails db log storage tmp

USER rails:rails

EXPOSE 3000
CMD ["bin/rails", "server", "-b", "0.0.0.0", "-p", "3000"]
