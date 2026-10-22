<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use App\Models\EventLog;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class EventLogController
{
    public function index(): JsonResponse
    {
        $events = EventLog::query()->latest()->take(50)->get();

        // MongoDB Aggregation Pipeline for Category Summary
        $stats = EventLog::raw(function ($collection) {
            return $collection->aggregate([
                ['$group' => [
                    '_id' => '$category',
                    'count' => ['$sum' => 1],
                    'avg_latency' => ['$avg' => '$latency_ms']
                ]],
                ['$sort' => ['count' => -1]]
            ])->toArray();
        });

        return response()->json([
            'status' => 'ok',
            'total_events' => EventLog::count(),
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

        // Sanitize any NoSQL operator injection in metadata keys
        if (isset($validated['metadata'])) {
            foreach (array_keys($validated['metadata']) as $key) {
                if (str_starts_with((string)$key, '$')) {
                    return response()->json(['error' => 'Illegal operator in metadata keys'], 422);
                }
            }
        }

        $user = Auth::user();
        $event = EventLog::create([
            'user_id' => $user ? (string)$user->id : 'system',
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
}
