<div class="space-y-8">
    @if (session()->has('message'))
        <div class="p-4 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-800 dark:bg-emerald-950 dark:border-emerald-800 dark:text-emerald-300 text-sm font-medium">
            {{ session('message') }}
        </div>
    @endif

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="text-sm font-medium text-slate-500">Total Live Tasks</div>
            <div class="mt-2 text-3xl font-bold text-slate-900 dark:text-slate-100">{{ $totalCount }}</div>
            <div class="mt-1 text-xs text-orange-600">Real-time Morphing</div>
        </div>
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="text-sm font-medium text-slate-500">Completed</div>
            <div class="mt-2 text-3xl font-bold text-emerald-600 dark:text-emerald-400">{{ $completedCount }}</div>
            <div class="mt-1 text-xs text-slate-400">Verified actions</div>
        </div>
        <div class="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="text-sm font-medium text-slate-500">Database Engine</div>
            <div class="mt-2 text-3xl font-bold text-slate-900 dark:text-slate-100">PostgreSQL 16</div>
            <div class="mt-1 text-xs text-slate-400">UUID Primary Keys</div>
        </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-1 p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm h-fit">
            <h2 class="text-lg font-bold text-slate-900 dark:text-slate-100 mb-4">Add Reactive Task</h2>
            <form wire:submit="save" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Title</label>
                    <input type="text" wire:model.blur="title" placeholder="e.g. Implement Volt single-file component" class="w-full px-4 py-2 border rounded-lg border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-orange-500" />
                    @error('title') <span class="text-xs text-red-500 mt-1 block">{{ $message }}</span> @enderror
                </div>
                <div>
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Description</label>
                    <textarea wire:model="description" rows="3" placeholder="Component details and acceptance criteria..." class="w-full px-4 py-2 border rounded-lg border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-orange-500"></textarea>
                </div>
                <div>
                    <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Priority</label>
                    <select wire:model="priority" class="w-full px-4 py-2 border rounded-lg border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100">
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                    </select>
                </div>
                <button type="submit" wire:loading.attr="disabled" class="w-full py-2.5 px-4 rounded-lg bg-orange-600 hover:bg-orange-700 text-white font-semibold shadow-sm transition">
                    <span wire:loading.remove>Save Task</span>
                    <span wire:loading>Saving...</span>
                </button>
            </form>
        </div>

        <div class="lg:col-span-2 p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <h2 class="text-lg font-bold text-slate-900 dark:text-slate-100 mb-4">Task Stream</h2>
            <div class="divide-y divide-slate-100 dark:divide-slate-800">
                @forelse ($tasks as $task)
                    <div wire:key="{{ $task->id }}" class="py-4 flex items-start justify-between space-x-4">
                        <div class="space-y-1">
                            <div class="flex items-center space-x-2">
                                <span class="font-semibold text-slate-900 dark:text-slate-100 {{ $task->is_completed ? 'line-through text-slate-400' : '' }}">{{ $task->title }}</span>
                                <span class="px-2 py-0.5 text-xs rounded-full font-medium bg-orange-100 text-orange-700 dark:bg-orange-950 dark:text-orange-300">{{ ucfirst($task->priority) }}</span>
                            </div>
                            @if ($task->description)
                                <p class="text-sm text-slate-600 dark:text-slate-400">{{ $task->description }}</p>
                            @endif
                            <p class="text-xs text-slate-400">Created: {{ $task->created_at->format('M d, Y H:i') }}</p>
                        </div>
                        <div class="flex items-center space-x-2">
                            <button wire:click="toggleComplete('{{ $task->id }}')" class="px-3 py-1.5 text-xs font-semibold rounded-lg border {{ $task->is_completed ? 'border-slate-300 text-slate-600' : 'border-emerald-300 text-emerald-700 bg-emerald-50 dark:bg-emerald-950 dark:border-emerald-800 dark:text-emerald-300' }}">
                                {{ $task->is_completed ? 'Mark Pending' : 'Complete' }}
                            </button>
                            <button wire:click="deleteTask('{{ $task->id }}')" wire:confirm="Are you sure you want to delete this task?" class="px-2 py-1.5 text-xs text-red-600 hover:bg-red-50 rounded-lg">
                                ✕
                            </button>
                        </div>
                    </div>
                @empty
                    <div class="text-center py-12 text-slate-400">
                        <p>No tasks created yet. Use the form on the left to add one.</p>
                    </div>
                @endforelse
            </div>
        </div>
    </div>
</div>
