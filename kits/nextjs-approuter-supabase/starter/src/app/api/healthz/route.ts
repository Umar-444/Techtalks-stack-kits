import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'ok',
    app: 'nextjs-approuter-supabase',
    version: '1.0.0',
    framework: 'Next.js 15 App Router',
    runtime: 'nodejs',
  });
}
