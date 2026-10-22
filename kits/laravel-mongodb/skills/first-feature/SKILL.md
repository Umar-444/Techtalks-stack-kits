---
name: first-feature
description: Build the canonical first feature: EventLog Document Resource with embedded telemetry attributes, aggregation stats, and BOLA policy protection.
---

# First Feature Skill: EventLog Document Resource

## Objective
Construct a high-performance MongoDB Document module adhering to the 18-checkpoint standard:
1. Eloquent MongoDB Model extending `MongoDB\Laravel\Eloquent\Model`.
2. Embedded document telemetry payload (`embedsMany` or embedded JSON schema).
3. Laravel Gate/Policy enforcing BOLA authorization on document owners.
4. Aggregation pipeline builder calculating event metrics by category and severity.
5. Pest test verifying document persistence, aggregation accuracy, and access control.

## Implementation Steps
1. Define Model in `app/Models/EventLog.php`.
2. Create Policy in `app/Policies/EventLogPolicy.php` checking `$user->id === $event->user_id`.
3. Implement Controller in `app/Http/Controllers/EventLogController.php` with aggregation pipeline.
4. Register Routes in `routes/web.php`.
5. Run automated test suite verifying document persistence.

## Done Means
A user creates an event document with embedded payload attributes, data saves to MongoDB collection `event_logs`, aggregation endpoint returns computed group metrics, and unauthorized users cannot mutate logs.
