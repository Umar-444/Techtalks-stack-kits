require "test_helper"

class PostsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @post = posts(:one) rescue Post.create!(title: "Setup Post", body: "Initial body")
  end

  test "should get index" do
    get posts_url
    assert_response :success
  end

  test "should get healthz probe" do
    get "/healthz"
    assert_response :success
    json = JSON.parse(response.body)
    assert_equal "ok", json["status"]
    assert_equal "ruby-rails-hotwire", json["app"]
  end

  test "should create post via turbo stream" do
    assert_difference("Post.count") do
      post posts_url, params: { post: { title: "New Title", body: "New Body" } }, as: :turbo_stream
    end
    assert_response :success
  end
end
