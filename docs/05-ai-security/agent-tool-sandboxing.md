# AI Agent Tool Sandboxing in Laravel

> Last reviewed: 2026-10. Applies to: PHP 8.4+, Laravel 11.x – 13.x.

## Quick Answer

AI agent tool sandboxing restricts what function calls an autonomous model can execute in your Laravel application. Because an LLM can be manipulated via prompt injection or model hallucination, agent actions must be strictly bounded: only explicitly allowlisted tools can be registered, all function arguments must pass standard Laravel validation rules, destructive operations require human-in-the-loop confirmation, and all actions must execute under the authenticated user's authorization policies.

## Threat Model

- **Attacker Profile**: Malicious end-users or adversaries injecting indirect prompt triggers into data processed by autonomous AI agents.
- **Attack Vectors**:
  - **Tool Hijacking / Excessive Agency**: An agent configured with a `sendRefund` or `runSql` tool is tricked by prompt injection into issuing unauthorized refunds or truncating tables.
  - **Argument Manipulation**: Injecting arbitrary email addresses into an email dispatch tool to turn your server into a spam/phishing relay.
  - **Privilege Escalation**: An agent taking actions with elevated system permissions rather than the permissions of the calling tenant.
- **Impact & Cost**: Financial loss, unauthorized database modifications, data destruction, and server compromise.

## Vulnerable Example

```php
<?php

declare(strict_types=1);

namespace App\Services\Ai;

use Illuminate\Support\Facades\DB;

class VulnerableAgentExecutor
{
    /**
     * [INSECURE]: Dynamically invoking arbitrary methods and running unchecked SQL.
     */
    public function executeAgentFunction(string $functionName, array $arguments): mixed
    {
        // Vulnerable: Blindly executing whatever function name the LLM outputs
        if (method_exists($this, $functionName)) {
            return $this->$functionName(...$arguments);
        }

        // Dangerous: Raw query execution tool given to model
        if ($functionName === 'execute_query') {
            return DB::statement($arguments['sql']);
        }

        return 'Unknown tool';
    }
}
```

## Secure Implementation

```php
<?php

declare(strict_types=1);

namespace App\Services\Ai\Tools;

use App\Models\User;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\Validator;
use InvalidArgumentException;
use RuntimeException;

interface AgentToolInterface
{
    public function name(): string;
    public function description(): string;
    public function schema(): array;
    public function execute(User $caller, array $arguments): array;
}

final class SendNotificationTool implements AgentToolInterface
{
    public function name(): string
    {
        return 'send_user_notification';
    }

    public function description(): string
    {
        return 'Sends a plain-text notification message to an authenticated team member.';
    }

    public function schema(): array
    {
        return [
            'type' => 'object',
            'properties' => [
                'recipient_id' => ['type' => 'integer'],
                'message' => ['type' => 'string'],
            ],
            'required' => ['recipient_id', 'message'],
        ];
    }

    public function execute(User $caller, array $arguments): array
    {
        // 1. Authorize: Verify caller has permission to perform this action
        if (!Gate::forUser($caller)->allows('send-team-notifications')) {
            throw new RuntimeException('Unauthorized: Caller lacks permission to invoke notification tool.');
        }

        // 2. Validate tool arguments strictly with Laravel Validator
        $validated = Validator::make($arguments, [
            'recipient_id' => ['required', 'integer', 'exists:users,id'],
            'message' => ['required', 'string', 'max:500'],
        ])->validate();

        // 3. Execute safely within tenant boundary
        $recipient = User::where('tenant_id', $caller->tenant_id)
            ->findOrFail($validated['recipient_id']);

        // Dispatch notification safely
        return [
            'status' => 'success',
            'message' => "Notification dispatched to user {$recipient->id}.",
        ];
    }
}

final class SecureAgentDispatcher
{
    /** @var array<string, AgentToolInterface> */
    private array $allowedTools = [];

    public function registerTool(AgentToolInterface $tool): void
    {
        $this->allowedTools[$tool->name()] = $tool;
    }

    /**
     * [SECURE]: Explicit allowlist dispatch, argument validation, and authorization check.
     */
    public function dispatchTool(User $user, string $toolName, array $rawArguments): array
    {
        if (!array_key_exists($toolName, $this->allowedTools)) {
            throw new InvalidArgumentException("Tool [{$toolName}] is not in the approved agent tool allowlist.");
        }

        $tool = $this->allowedTools[$toolName];

        // Critical safety: Destructive tools require human confirmation token
        if ($this->isDestructive($toolName)) {
            return [
                'status' => 'pending_confirmation',
                'action_token' => bin2hex(random_bytes(16)),
                'message' => 'Action requires human approval before execution.',
            ];
        }

        return $tool->execute($user, $rawArguments);
    }

    private function isDestructive(string $toolName): bool
    {
        return in_array($toolName, ['delete_record', 'process_refund', 'transfer_funds'], true);
    }
}
```

## Laravel-Specific Notes

- **Laravel Policies & Gates**: Always pass the calling `User` model into tool execution methods and invoke `Gate::forUser($user)->authorize(...)`. Never execute tools using a system daemon or elevated administrator role.
- **Queued Approval Workflow**: For destructive tools (refunds, deletions), store the proposed action in a `pending_ai_actions` database table and send a confirmation email or Slack notification to a human manager.
- **Audit Logging**: Write every tool invocation and argument payload to an append-only audit log table (`ai_tool_audit_logs`) with user ID, timestamp, and IP address.

## Checklist

- [ ] All agent functions are maintained in a strict, hard-coded allowlist.
- [ ] No tools allow arbitrary shell commands, raw SQL, or file system modifications.
- [ ] All function call arguments are validated using standard Laravel validation rules.
- [ ] Every tool invocation checks caller permissions via Laravel Gates/Policies.
- [ ] Destructive financial or deletion actions require human-in-the-loop approval.

## Further Reading

- [OWASP Top 10 for LLM Applications (LLM08: Excessive Agency)](https://genai.owasp.org/llm-top-10/)
- [Laravel Authorization & Policies Documentation](https://laravel.com/docs/13.x/authorization)
- [OpenAI Function Calling & Tool Definitions Guide](https://platform.openai.com/docs/guides/function-calling)
