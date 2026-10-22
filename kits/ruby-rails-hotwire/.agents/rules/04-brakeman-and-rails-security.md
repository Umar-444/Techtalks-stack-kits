# Rails Security Invariants, Strong Parameters, and Brakeman

# Rails Security Invariants, Strong Parameters, and Brakeman

## 1. Zero-Brakeman-Warning Baseline
- Run `brakeman -q -z` in CI; any high or medium confidence security warning fails the build.
- Prevent SQL injection: Never interpolate variables into `.where("title = '#{title}'")`. Always use bind parameters `.where(title: title)` or `.where("title ILIKE ?", "%#{query}%")`.

## 2. Strict Strong Parameters
- Guard mass-assignment in all mutating actions:
  ```ruby
  def post_params
    params.require(:post).permit(:title, :body)
  end
  ```
- Never call `.permit!` on user input. Explicitly list every whitelisted attribute.

## 3. CSRF & Session Security
- Maintain `protect_from_forgery with: :exception` in `ApplicationController`.
- Cookie session stores must be configured with `secure: true`, `httponly: true`, and `same_site: :lax`.
- Never expose sensitive tokens, API secrets, or passwords in plain-text logs; maintain comprehensive `config.filter_parameters`.
