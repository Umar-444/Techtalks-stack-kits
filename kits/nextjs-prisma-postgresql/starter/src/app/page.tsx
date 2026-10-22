import { prisma } from '@/lib/prisma';

export default async function HomePage() {
  const projects = await prisma.project.findMany({
    orderBy: { createdAt: 'desc' },
    take: 10,
  });

  return (
    <main className="min-h-screen p-8 bg-slate-950 text-slate-100 font-sans">
      <div className="max-w-4xl mx-auto space-y-6">
        <header className="border-b border-slate-800 pb-4">
          <h1 className="text-2xl font-bold tracking-tight">Project Management Platform</h1>
          <p className="text-slate-400 text-sm">Next.js 15 App Router + Prisma ORM + PostgreSQL 16</p>
        </header>

        <section className="grid gap-4 md:grid-cols-2">
          {projects.map((p) => (
            <div key={p.id} className="p-4 bg-slate-900 border border-slate-800 rounded-lg">
              <h2 className="text-lg font-semibold">{p.title}</h2>
              <p className="text-slate-400 text-sm mt-1">{p.description}</p>
              <div className="mt-4 flex justify-between items-center text-xs text-slate-500">
                <span>Status: {p.status}</span>
                <span>Tenant: {p.tenantId}</span>
              </div>
            </div>
          ))}
        </section>
      </div>
    </main>
  );
}
