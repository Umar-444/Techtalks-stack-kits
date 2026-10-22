import { createClient } from '@/lib/supabase/server';
import { createItem, toggleItem } from './actions';

export default async function DashboardPage() {
  const supabase = await createClient();
  
  // Fetch user-scoped items protected by RLS
  const { data: items } = await supabase
    .from('items')
    .select('*')
    .order('created_at', { ascending: false });

  const totalCount = items?.length || 0;
  const completedCount = items?.filter((i: any) => i.is_completed).length || 0;

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="text-sm font-medium text-slate-500">Total Items</div>
          <div className="mt-2 text-3xl font-bold text-slate-900 dark:text-slate-100">{totalCount}</div>
          <div className="mt-1 text-xs text-blue-600">Row Level Security Enforced</div>
        </div>
        <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="text-sm font-medium text-slate-500">Completed</div>
          <div className="mt-2 text-3xl font-bold text-emerald-600 dark:text-emerald-400">{completedCount}</div>
          <div className="mt-1 text-xs text-slate-400">Mutated via Server Actions</div>
        </div>
        <div className="p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="text-sm font-medium text-slate-500">Framework</div>
          <div className="mt-2 text-3xl font-bold text-slate-900 dark:text-slate-100">Next.js 15</div>
          <div className="mt-1 text-xs text-slate-400">React 19 Server Components</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1 p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm h-fit">
          <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 mb-4">Add Task (Server Action)</h2>
          <form action={createItem} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Title</label>
              <input
                type="text"
                name="title"
                required
                placeholder="e.g. Implement Supabase RLS Policy"
                className="w-full px-4 py-2 border rounded-lg border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Description</label>
              <textarea
                name="description"
                rows={3}
                placeholder="Action validation rules and criteria..."
                className="w-full px-4 py-2 border rounded-lg border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button
              type="submit"
              className="w-full py-2.5 px-4 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-sm transition"
            >
              Save Item
            </button>
          </form>
        </div>

        <div className="lg:col-span-2 p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
          <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 mb-4">Items Stream</h2>
          <div className="divide-y divide-slate-100 dark:divide-slate-800">
            {items && items.length > 0 ? (
              items.map((item: any) => (
                <div key={item.id} className="py-4 flex items-start justify-between space-x-4">
                  <div className="space-y-1">
                    <span className={`font-semibold ${item.is_completed ? 'line-through text-slate-400' : 'text-slate-900 dark:text-slate-100'}`}>
                      {item.title}
                    </span>
                    {item.description && <p className="text-sm text-slate-600 dark:text-slate-400">{item.description}</p>}
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-12 text-slate-400">
                <p>No items in database. Use the form to insert one.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
