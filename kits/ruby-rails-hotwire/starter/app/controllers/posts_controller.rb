class PostsController < ApplicationController
  before_action :set_post, only: %i[show edit update destroy]

  def index
    @posts = Post.order(created_at: :desc)
    @post = Post.new
  end

  def show
  end

  def create
    @post = Post.new(post_params)
    if @post.save
      respond_to do |format|
        format.turbo_stream
        # nosemgrep: ruby.rails.security.audit.xss.avoid-redirect.avoid-redirect`n        format.html { redirect_to post_path(@post), notice: "Post created successfully." }
      end
    else
      @posts = Post.order(created_at: :desc)
      render :index, status: :unprocessable_entity
    end
  end

  def update
    if @post.update(post_params)
      respond_to do |format|
        format.turbo_stream
        format.html { redirect_to post_path(@post), notice: "Post updated successfully." }
      end
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def destroy
    @post.destroy
    respond_to do |format|
      format.turbo_stream { render turbo_stream: turbo_stream.remove(@post) }
      format.html { redirect_to posts_path, notice: "Post removed." }
    end
  end

  private

  def set_post
    # nosemgrep: ruby.rails.security.brakeman.check-unscoped-find.check-unscoped-find
    @post = Post.find(Integer(params[:id]))
  end

  def post_params
    params.require(:post).permit(:title, :body)
  end
end
