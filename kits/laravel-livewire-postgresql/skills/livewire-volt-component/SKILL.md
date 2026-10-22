---
name: livewire-volt-component
description: Author high-velocity Volt single-file components with state, computed properties, and validation.
---

# Livewire Volt Component Skill

## Purpose
Enables creating declarative single-file reactive components where PHP logic and Blade template live seamlessly in one file.

## Example Pattern
```php
<?php

use function Livewire\Volt\{state, rules};
use App\Models\Task;

state(['title' => '', 'priority' => 'medium']);
rules(['title' => 'required|min:3|max:100']);

$save = function () {
    $this->validate();
    Task::create([
        'user_id' => auth()->id(),
        'title' => $this->title,
        'priority' => $this->priority,
    ]);
    $this->title = '';
};

?>

<div>
    <form wire:submit="save">
        <input type="text" wire:model="title" class="border rounded p-2" />
        <button type="submit" class="bg-orange-600 text-white px-4 py-2 rounded">Save</button>
    </form>
</div>
```

## Done Means
Volt single-file component compiles, binds reactive state without full page refreshes, and validates inputs strictly before database writes.
