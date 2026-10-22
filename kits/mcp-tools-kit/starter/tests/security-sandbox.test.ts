import { describe, it, expect } from 'vitest';
import { handleReadSecureFile } from '../src/tools/index';

describe('Security Sandboxing Tests', () => {
  it('should reject path traversal attempts outside sandbox root', () => {
    expect(() => {
      handleReadSecureFile('../../../etc/passwd', process.cwd());
    }).toThrowError('SECURITY_ERROR: Access denied. Path outside sandbox boundary.');
  });
});
