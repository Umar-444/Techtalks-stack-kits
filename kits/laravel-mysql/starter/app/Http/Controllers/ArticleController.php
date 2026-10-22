<?php

namespace App\Http\Controllers;

use App\Models\Article;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class ArticleController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $query = Article::with('user');

        if ($request->filled('q')) {
            $query->search($request->query('q'));
        } else {
            $query->published();
        }

        $articles = $query->orderByDesc('created_at')->paginate(20);

        return response()->json($articles);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'title' => 'required|string|min:3|max:255',
            'content' => 'required|string',
            'status' => 'nullable|in:draft,published',
        ]);

        $article = DB::transaction(function () use ($validated, $request) {
            return Article::create([
                'user_id' => $request->user()?->id ?? 1,
                'title' => $validated['title'],
                'content' => $validated['content'],
                'status' => $validated['status'] ?? 'published',
            ]);
        }, attempts: 5);

        return response()->json($article, 201);
    }

    public function show(Article $article): JsonResponse
    {
        $this->authorize('view', $article);
        return response()->json($article->load('user'));
    }

    public function destroy(Article $article): JsonResponse
    {
        $this->authorize('delete', $article);
        $article->delete();
        return response()->json(['status' => 'deleted']);
    }
}
