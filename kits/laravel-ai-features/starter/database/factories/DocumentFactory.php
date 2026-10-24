<?php

declare(strict_types=1);

namespace Database\Factories;

use App\Models\Document;
use Illuminate\Database\Eloquent\Factories\Factory;

class DocumentFactory extends Factory
{
    protected $model = Document::class;

    public function definition(): array
    {
        return [
            'title' => fake()->sentence(3),
            'content' => fake()->paragraph(),
            'tenant_id' => 1,
        ];
    }
}
