require "test_helper"

class PostTest < ActiveSupport::TestCase
  test "validates title presence" do
    post = Post.new(body: "Content without title")
    assert_not post.valid?
    assert_includes post.errors[:title], "can't be blank"
  end

  test "validates body presence" do
    post = Post.new(title: "Valid Title")
    assert_not post.valid?
    assert_includes post.errors[:body], "can't be blank"
  end

  test "creates valid post" do
    post = Post.new(title: "Test Title", body: "Test Body")
    assert post.valid?
    assert post.save
  end
end
