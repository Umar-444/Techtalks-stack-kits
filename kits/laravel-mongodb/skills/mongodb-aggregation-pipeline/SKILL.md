---
name: mongodb-aggregation-pipeline
description: Construct multi-stage MongoDB aggregation pipelines ($match, $group, $sort) for high-velocity analytics.
---

# MongoDB Aggregation Pipeline Skill

## Purpose
Enables building performant server-side data processing pipelines directly inside MongoDB.

## Pipeline Architecture
```php
$stats = EventLog::raw(function ($collection) use ($userId) {
    return $collection->aggregate([
        ['$match' => ['user_id' => $userId]],
        ['$group' => [
            '_id' => '$category',
            'count' => ['$sum' => 1],
            'avg_latency' => ['$avg' => '$latency_ms']
        ]],
        ['$sort' => ['count' => -1]],
        ['$limit' => 10]
    ]);
});
```

## Standards
- Always filter with `$match` before grouping.
- Ensure indexed fields are utilized in initial pipeline stages.

## Done Means
Aggregation pipeline executes inside MongoDB engine in under 10ms and returns structured group metrics without in-memory PHP loops.
