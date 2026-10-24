import { cookies } from 'next/headers';

/**
 * The authenticated caller. `tenantId` and `userId` originate here and
 * nowhere else — never from a request body. See rules/source/04.
 */
export interface Session {
  userId: string;
  tenantId: string;
}

export class UnauthorizedError extends Error {
  constructor(message = 'Authentication required') {
    super(message);
    this.name = 'UnauthorizedError';
  }
}

/**
 * Resolve the session for the current request.
 *
 * Replace the cookie lookup with your real identity provider. What must not
 * change is the boundary: the caller's tenant is derived server-side, so a
 * crafted request body cannot reassign it.
 */
export async function getSession(): Promise<Session | null> {
  const store = await cookies();
  const userId = store.get('session_user')?.value;
  const tenantId = store.get('session_tenant')?.value;

  if (!userId || !tenantId) return null;
  return { userId, tenantId };
}

/** Same as getSession but throws, for use at the top of a Server Action. */
export async function requireSession(): Promise<Session> {
  const session = await getSession();
  if (!session) throw new UnauthorizedError();
  return session;
}
