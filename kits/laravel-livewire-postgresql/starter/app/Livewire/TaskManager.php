<?php

declare(strict_types=1);

namespace App\Livewire;

use App\Models\Task;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Validation\ValidationException;
use Livewire\Attributes\Layout;
use Livewire\Attributes\Validate;
use Livewire\Component;

#[Layout('layouts.app')]
class TaskManager extends Component
{
    /** Mutating actions allowed per user per minute (LW-05). */
    private const ACTIONS_PER_MINUTE = 30;

    // Only these three values are client-writable public state (LW-03).
    // Ownership (user_id) and record ids are never public properties.
    #[Validate('required|min:3|max:150')]
    public string $title = '';

    #[Validate('nullable|max:500')]
    public string $description = '';

    #[Validate('required|in:low,medium,high')]
    public string $priority = 'medium';

    public function save(): void
    {
        $this->validate();

        $user = Auth::user();
        if (! $user) {
            session()->flash('error', 'Please log in to add tasks.');
            return;
        }

        $this->throttle();

        Task::create([
            'user_id' => $user->id,
            'title' => $this->title,
            'description' => $this->description,
            'priority' => $this->priority,
            'is_completed' => false,
        ]);

        $this->reset(['title', 'description']);
        session()->flash('message', 'Task created successfully.');
    }

    public function toggleComplete(string $id): void
    {
        $task = Task::findOrFail($id);
        Gate::authorize('update', $task);
        $this->throttle();

        $task->is_completed = ! $task->is_completed;
        $task->save();
    }

    public function deleteTask(string $id): void
    {
        $task = Task::findOrFail($id);
        Gate::authorize('delete', $task);
        $this->throttle();

        $task->delete();
        session()->flash('message', 'Task deleted.');
    }

    public function render()
    {
        // Only the signed-in user's own tasks are ever loaded (LW-02).
        $tasks = Task::query()->where('user_id', Auth::id())->latest()->get();

        return view('livewire.task-manager', [
            'tasks' => $tasks,
            'totalCount' => $tasks->count(),
            'completedCount' => $tasks->where('is_completed', true)->count(),
        ]);
    }

    private function throttle(): void
    {
        $key = 'task-actions:' . Auth::id();

        if (! RateLimiter::attempt($key, self::ACTIONS_PER_MINUTE, static fn () => true, 60)) {
            throw ValidationException::withMessages(['rate' => 'Too many actions. Please slow down.']);
        }
    }
}
