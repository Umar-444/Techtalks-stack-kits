<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('articles', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('title');
            $table->text('content');
            $table->string('status')->default('draft');
            $table->timestamps();

            $table->index(['status', 'created_at']);
        });

        // FULLTEXT is a MySQL/Postgres feature. The test suite runs on SQLite,
        // which has no equivalent on a regular table, so this is applied only
        // where the driver supports it.
        if (in_array(Schema::getConnection()->getDriverName(), ['mysql', 'mariadb'], true)) {
            Schema::table('articles', function (Blueprint $table) {
                $table->fullText(['title', 'content']);
            });
        }
    }

    public function down(): void
    {
        Schema::dropIfExists('articles');
    }
};
