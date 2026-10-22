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
    private challenges: Map<string, { challenge: string; expiresAt: number }> = new Map();

    async saveChallenge(key: string, challenge: string, ttlSeconds: number = 120): Promise<void> {
        this.challenges.set(key, {
            challenge,
            expiresAt: Date.now() + ttlSeconds * 1000,
        });
    }

    async getChallenge(key: string): Promise<string | null> {
        const item = this.challenges.get(key);
        if (!item) return null;
        if (Date.now() > item.expiresAt) {
            this.challenges.delete(key);
            return null;
        }
        // One-time use: consume immediately
        this.challenges.delete(key);
        return item.challenge;
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
