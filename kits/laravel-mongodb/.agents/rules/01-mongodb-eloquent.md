# MongoDB Eloquent Conventions

# MongoDB Eloquent Conventions

1. **Model Inheritance:**
   - All MongoDB models must extend `MongoDB\Laravel\Eloquent\Model`.
   - Explicitly specify the collection name: `protected $collection = 'users';`.

2. **Embedded Relations:**
   - Use `embedsOne()` and `embedsMany()` for strictly co-located document data.
   - Define embedded models with strict attribute casting.
