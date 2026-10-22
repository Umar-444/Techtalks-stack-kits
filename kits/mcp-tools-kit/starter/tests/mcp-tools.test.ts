import { describe, it, expect } from 'vitest';
import { handleSystemInfo, handleCalculator, handleReadSecureFile } from '../src/tools/index';

describe('MCP Tools Unit Tests', () => {
  it('should return system info telemetry cleanly', () => {
    const info = handleSystemInfo();
    expect(info).toHaveProperty('platform');
    expect(info).toHaveProperty('architecture');
    expect(info.cpuCount).toBeGreaterThan(0);
  });

  it('should perform safe arithmetic without eval()', () => {
    expect(handleCalculator(10, 5, 'add')).toBe(15);
    expect(handleCalculator(10, 5, 'subtract')).toBe(5);
    expect(handleCalculator(10, 5, 'multiply')).toBe(50);
    expect(handleCalculator(10, 5, 'divide')).toBe(2);
  });

  it('should throw error on division by zero', () => {
    expect(() => handleCalculator(10, 0, 'divide')).toThrowError('DIVISION_BY_ZERO');
  });
});
