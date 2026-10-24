export interface StoredPasskey {
    id: string; // Base64URL string
    publicKey: Uint8Array;
    userId: string;
    userName: string;
    counter: number;
    deviceType: string;
    backedUp: boolean;
    transports?: string[];
    createdAt: Date;
}

export class MemoryAuthStore {
    private passkeys: Map<string, StoredPasskey> = new Map();
    private challenges: Map<
        string,
        { challenge: string; expiresAt: number; meta?: Record<string, string> }
    > = new Map();
    private sessions: Map<string, { userId: string; expiresAt: number }> = new Map();

    async saveChallenge(
        key: string,
        challenge: string,
        ttlSeconds: number = 120,
        meta?: Record<string, string>,
    ): Promise<void> {
        this.challenges.set(key, {
            challenge,
            meta,
            expiresAt: Date.now() + ttlSeconds * 1000,
        });
    }

    /** Returns the challenge and its metadata and deletes it: one-time use, even when expired. */
    async consumeChallenge(
        key: string,
    ): Promise<{ challenge: string; meta?: Record<string, string> } | null> {
        const item = this.challenges.get(key);
        if (!item) return null;
        // One-time use: consume immediately
        this.challenges.delete(key);
        if (Date.now() > item.expiresAt) return null;
        return { challenge: item.challenge, meta: item.meta };
    }

    async getChallenge(key: string): Promise<string | null> {
        return (await this.consumeChallenge(key))?.challenge ?? null;
    }

    async createSession(sessionId: string, userId: string, ttlSeconds: number = 86400 * 7): Promise<void> {
        this.sessions.set(sessionId, { userId, expiresAt: Date.now() + ttlSeconds * 1000 });
    }

    async getSessionUser(sessionId: string | undefined): Promise<string | null> {
        if (!sessionId) return null;
        const s = this.sessions.get(sessionId);
        if (!s) return null;
        if (Date.now() > s.expiresAt) {
            this.sessions.delete(sessionId);
            return null;
        }
        return s.userId;
    }

    async deleteSession(sessionId: string): Promise<void> {
        this.sessions.delete(sessionId);
    }

    async savePasskey(passkey: StoredPasskey): Promise<void> {
        this.passkeys.set(passkey.id, passkey);
    }

    async getPasskeyById(id: string): Promise<StoredPasskey | null> {
        return this.passkeys.get(id) || null;
    }

    async getUserPasskeys(userId: string): Promise<StoredPasskey[]> {
        return Array.from(this.passkeys.values()).filter(p => p.userId === userId);
    }

    async updatePasskeyCounter(id: string, newCounter: number): Promise<void> {
        const passkey = this.passkeys.get(id);
        if (passkey) {
            passkey.counter = newCounter;
        }
    }
}

export const authStore = new MemoryAuthStore();
