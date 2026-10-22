---
name: first-feature
description: Guide for scaffolding a real-time reactive Hotwire feature using Turbo Frames, Turbo Streams, and Stimulus.
---

# First Feature Skill: Real-Time Post Publishing

## Overview
Scaffold a complete real-time publishing workflow in Rails 8 using Hotwire Turbo 8 and Stimulus.

## Step-by-Step Implementation

### 1. Generate Model and Migration
```bash
bin/rails generate model Post title:string body:text
bin/rails db:migrate
```

### 2. Configure Model Validations & Broadcasting
In `app/models/post.rb`:
```ruby
class Post < ApplicationRecord
  validates :title, presence: true, length: { minimum: 3, maximum: 150 }
  validates :body, presence: true

  after_create_commit  -> { broadcast_prepend_to "posts", target: "posts_list", partial: "posts/post" }
  after_update_commit  -> { broadcast_replace_to "posts" }
  after_destroy_commit -> { broadcast_remove_to "posts" }
end
```

### 3. Create Resourceful Controller with Turbo Stream Responder
In `app/controllers/posts_controller.rb`:
```ruby
class PostsController < ApplicationController
  def index
    @posts = Post.order(created_at: :desc)
    @post = Post.new
  end

  def create
    @post = Post.new(post_params)
    if @post.save
      respond_to do |format|
        format.turbo_stream
        format.html { redirect_to posts_path, notice: "Post created successfully." }
      end
    else
      render :index, status: :unprocessable_entity
    end
  end

  private

  def post_params
    params.require(:post).permit(:title, :body)
  end
end
```

### 4. Build Reactive Views
In `app/views/posts/index.html.erb`:
```erb
<%= turbo_stream_from "posts" %>

<div class="max-w-xl mx-auto py-8">
  <h1 class="text-2xl font-bold mb-4">Articles &amp; Posts</h1>
  
  <%= turbo_frame_tag "new_post_frame" do %>
    <%= render "posts/form", post: @post %>
  <% end %>

  <div id="posts_list" class="mt-6 space-y-4">
    <%= render @posts %>
  </div>
</div>
```
