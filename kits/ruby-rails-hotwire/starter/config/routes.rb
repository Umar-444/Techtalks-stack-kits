Rails.application.routes.draw do
  root "posts#index"
  resources :posts
  
  # Health check probe returning 200 OK JSON
  get "/healthz", to: proc { [200, { "Content-Type" => "application/json" }, ['{"status":"ok","app":"ruby-rails-hotwire","version":"1.0.0"}']] }
  get "up" => "rails/health#show", as: :rails_health_check
end
