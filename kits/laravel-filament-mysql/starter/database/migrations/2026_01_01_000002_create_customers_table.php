<?php

declare(strict_types=1);

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('customers', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('email')->index();
            $table->string('company_name')->nullable();
            $table->string('status')->default('active')->index();
            $table->unsignedBigInteger('team_id')->default(1)->index();
            $table->timestamps();

            // Native MySQL 8.4 Full-Text Index (SQLite, used by the test suite,
            // has no equivalent).
            if (in_array(Schema::getConnection()->getDriverName(), ['mysql', 'mariadb', 'pgsql'], true)) {
                $table->fullText(['name', 'email', 'company_name'], 'customers_fulltext_idx');
            }
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('customers');
    }
};
