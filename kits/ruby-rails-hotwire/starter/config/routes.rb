Rails.application.routes.draw do
  root "posts#index"
  resources :posts
  get "up" => "rails/health#show", as: :rails_health_check
end
