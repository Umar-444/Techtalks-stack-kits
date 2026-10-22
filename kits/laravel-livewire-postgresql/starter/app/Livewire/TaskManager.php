<?php

declare(strict_types=1);

namespace App\Livewire;

use App\Models\Task;
use Illuminate\Support\Facades\Auth;
use Livewire\Component;
use Livewire\Attributes\Validate;

class TaskManager extends Component
{
    #[Validate('required|min:3|max:150')]
    public string $title = '';

    #[Validate('nullable|max:500')]
    public string $description = '';

    public string $priority = 'medium';

    public function save(): void
    {
        $this->validate();

        $user = Auth::user();
        if (!$user) {
            session()->flash('error', 'Please log in to add tasks.');
            return;
        }

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
        $task->is_completed = !$task->is_completed;
        $task->save();
    }

    public function deleteTask(string $id): void
    {
        $task = Task::findOrFail($id);
        $task->delete();
        session()->flash('message', 'Task deleted.');
    }

    public function render()
    {
        $tasks = Task::query()->latest()->get();
        return view('livewire.task-manager', [
            'tasks' => $tasks,
            'totalCount' => $tasks->count(),
            'completedCount' => $tasks->where('is_completed', true)->count(),
        ]);
    }
}
