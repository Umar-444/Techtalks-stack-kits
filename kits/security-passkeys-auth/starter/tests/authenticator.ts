/**
 * Minimal software WebAuthn authenticator (ES256, "none" attestation) built on
 * node:crypto. It produces genuine signatures, so the real
 * @simplewebauthn/server verification code runs in the tests; nothing about
 * the verifier is mocked.
 */
import crypto from 'node:crypto';

const b64u = (b: Buffer) => b.toString('base64url');
const sha256 = (b: Buffer | string) => crypto.createHash('sha256').update(b).digest();

function cborBytes(b: Buffer): Buffer {
  const n = b.length;
  const head = n < 24 ? Buffer.from([0x40 | n]) : n < 256 ? Buffer.from([0x58, n]) : Buffer.from([0x59, n >> 8, n & 0xff]);
  return Buffer.concat([head, b]);
}
const cborText = (s: string) => Buffer.concat([Buffer.from([0x60 | s.length]), Buffer.from(s)]);

export class SoftAuthenticator {
  readonly credentialId = crypto.randomBytes(32);
  counter = 0;
  private privateKey: crypto.KeyObject;
  private x: Buffer;
  private y: Buffer;

  constructor() {
    const { privateKey, publicKey } = crypto.generateKeyPairSync('ec', { namedCurve: 'P-256' });
    this.privateKey = privateKey;
    const jwk = publicKey.export({ format: 'jwk' }) as { x: string; y: string };
    this.x = Buffer.from(jwk.x, 'base64url');
    this.y = Buffer.from(jwk.y, 'base64url');
  }

  get id() {
    return b64u(this.credentialId);
  }

  private coseKey(): Buffer {
    return Buffer.concat([
      Buffer.from([0xa5, 0x01, 0x02, 0x03, 0x26, 0x20, 0x01]),
      Buffer.from([0x21]), cborBytes(this.x),
      Buffer.from([0x22]), cborBytes(this.y),
    ]);
  }

  private clientData(type: string, challenge: string, origin: string) {
    return Buffer.from(JSON.stringify({ type, challenge, origin, crossOrigin: false }));
  }

  register(opts: { challenge: string; origin: string; rpId: string; userVerified?: boolean }) {
    const flags = 0x01 | (opts.userVerified === false ? 0 : 0x04) | 0x40;
    const counter = Buffer.alloc(4);
    counter.writeUInt32BE(this.counter);
    const credLen = Buffer.alloc(2);
    credLen.writeUInt16BE(this.credentialId.length);
    const authData = Buffer.concat([
      sha256(opts.rpId), Buffer.from([flags]), counter, Buffer.alloc(16), credLen, this.credentialId, this.coseKey(),
    ]);
    const attestationObject = Buffer.concat([
      Buffer.from([0xa3]),
      cborText('fmt'), cborText('none'),
      cborText('attStmt'), Buffer.from([0xa0]),
      cborText('authData'), cborBytes(authData),
    ]);
    return {
      id: this.id,
      rawId: this.id,
      type: 'public-key',
      clientExtensionResults: {},
      response: {
        clientDataJSON: b64u(this.clientData('webauthn.create', opts.challenge, opts.origin)),
        attestationObject: b64u(attestationObject),
        transports: ['internal'],
      },
    };
  }

  /** Signs an assertion. Pass `counter` to override the auto-incremented value. */
  assert(opts: { challenge: string; origin: string; rpId: string; counter?: number; userVerified?: boolean }) {
    this.counter = opts.counter ?? this.counter + 1;
    const flags = 0x01 | (opts.userVerified === false ? 0 : 0x04);
    const counter = Buffer.alloc(4);
    counter.writeUInt32BE(this.counter);
    const authData = Buffer.concat([sha256(opts.rpId), Buffer.from([flags]), counter]);
    const clientDataJSON = this.clientData('webauthn.get', opts.challenge, opts.origin);
    const signature = crypto.sign('sha256', Buffer.concat([authData, sha256(clientDataJSON)]), this.privateKey);
    return {
      id: this.id,
      rawId: this.id,
      type: 'public-key',
      clientExtensionResults: {},
      response: {
        authenticatorData: b64u(authData),
        clientDataJSON: b64u(clientDataJSON),
        signature: b64u(signature),
      },
    };
  }
}
