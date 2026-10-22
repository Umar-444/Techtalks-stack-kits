<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('tasks', function (Blueprint $table) {
            $table->uuid('id')->primary();
            $table->foreignUuid('user_id')->constrained('users')->cascadeOnDelete();
            $table->string('title');
            $table->text('description')->nullable();
            $table->string('priority')->default('medium');
            $table->boolean('is_completed')->default(false);
            $table->timestamps();

            $table->index(['user_id', 'is_completed', 'created_at']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('tasks');
    }
};
