<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use App\Models\EventLog;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class EventLogController
{
    public function index(Request $request): JsonResponse
    {
        // Every query is scoped to the signed-in user's own events (AUTH-02).
        $owner = (string) $request->user()->getAuthIdentifier();

        $events = EventLog::query()->where('user_id', $owner)->latest()->take(50)->get();

        // MongoDB Aggregation Pipeline for Category Summary. The $match stage
        // comes first so the pipeline only ever sees the caller's documents.
        $stats = EventLog::raw(function ($collection) use ($owner) {
            return $collection->aggregate([
                ['$match' => ['user_id' => $owner]],
                ['$group' => [
                    '_id' => '$category',
                    'count' => ['$sum' => 1],
                    'avg_latency' => ['$avg' => '$latency_ms'],
                ]],
                ['$sort' => ['count' => -1]],
            ])->toArray();
        });

        return response()->json([
            'status' => 'ok',
            'total_events' => EventLog::query()->where('user_id', $owner)->count(),
            'category_stats' => $stats,
            'recent_events' => $events,
        ]);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'category' => 'required|string|max:50',
            'action' => 'required|string|max:100',
            'severity' => 'required|in:low,medium,high,critical',
            'latency_ms' => 'nullable|integer|min:0',
            'metadata' => 'nullable|array',
        ]);

        // Reject NoSQL operator injection anywhere in the metadata tree
        // (NOSQL-01), not just in its top-level keys.
        if (isset($validated['metadata']) && self::hasOperatorKey($validated['metadata'])) {
            return response()->json(['error' => 'Illegal operator in metadata keys'], 422);
        }

        $event = EventLog::create([
            'user_id' => (string) $request->user()->getAuthIdentifier(),
            'category' => $validated['category'],
            'action' => $validated['action'],
            'severity' => $validated['severity'],
            'latency_ms' => $validated['latency_ms'] ?? 0,
            'metadata' => $validated['metadata'] ?? [],
        ]);

        return response()->json([
            'status' => 'created',
            'event' => $event,
        ], 201);
    }

    /** True when any key at any depth starts with "$" or contains ".". */
    private static function hasOperatorKey(array $data): bool
    {
        foreach ($data as $key => $value) {
            $key = (string) $key;

            if (str_starts_with($key, '$') || str_contains($key, '.')) {
                return true;
            }

            if (is_array($value) && self::hasOperatorKey($value)) {
                return true;
            }
        }

        return false;
    }
}
