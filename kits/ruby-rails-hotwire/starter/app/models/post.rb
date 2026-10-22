class Post < ApplicationRecord
  validates :title, presence: true, length: { minimum: 3, maximum: 200 }
  validates :body, presence: true

  after_create_commit  -> { broadcast_prepend_to "posts", target: "posts_list", partial: "posts/post" }
  after_update_commit  -> { broadcast_replace_to "posts" }
  after_destroy_commit -> { broadcast_remove_to "posts" }
end
