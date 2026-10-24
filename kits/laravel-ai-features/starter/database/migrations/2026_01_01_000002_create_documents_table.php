<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    public function up(): void
    {
        $pgsql = Schema::getConnection()->getDriverName() === 'pgsql';

        if ($pgsql) {
            // Enable pgvector extension
            DB::statement('CREATE EXTENSION IF NOT EXISTS vector;');
        }

        Schema::create('documents', function (Blueprint $table) use ($pgsql) {
            $table->id();
            $table->string('title');
            $table->text('content');
            $table->unsignedBigInteger('tenant_id')->default(1)->index();
            if (! $pgsql) {
                // No vector type outside PostgreSQL (e.g. SQLite in the test suite).
                $table->text('embedding')->nullable();
            }
            $table->timestamps();
        });

        if ($pgsql) {
            // Add vector column via direct DDL
            DB::statement('ALTER TABLE documents ADD COLUMN embedding vector(1536);');

            // Add HNSW cosine index
            DB::statement('CREATE INDEX documents_embedding_hnsw_idx ON documents USING hnsw (embedding vector_cosine_ops);');
        }
    }

    public function down(): void
    {
        Schema::dropIfExists('documents');
    }
};
