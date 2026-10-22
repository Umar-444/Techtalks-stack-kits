const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  const user = await prisma.user.upsert({
    where: { email: 'admin@techtalks.dev' },
    update: {},
    create: {
      email: 'admin@techtalks.dev',
      name: 'System Admin',
      role: 'admin',
      tenantId: 'tenant-001',
    },
  });

  const project1 = await prisma.project.create({
    data: {
      title: 'Infrastructure Modernization',
      description: 'Migrating legacy services to Next.js 15 and PostgreSQL 16.',
      tenantId: 'tenant-001',
      userId: user.id,
      tasks: {
        create: [
          { title: 'Provision PostgreSQL container', status: 'done', tenantId: 'tenant-001' },
          { title: 'Configure Prisma schema migrations', status: 'in_progress', tenantId: 'tenant-001' },
        ],
      },
    },
  });

  console.log(`Seeding completed: Created user ${user.id} and project ${project1.id}`);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
