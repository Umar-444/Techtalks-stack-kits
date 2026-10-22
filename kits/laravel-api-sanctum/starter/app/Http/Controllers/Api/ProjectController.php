<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\Project\StoreProjectRequest;
use App\Http\Requests\Project\UpdateProjectRequest;
use App\Http\Resources\ProjectResource;
use App\Models\Project;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;
use Spatie\QueryBuilder\AllowedFilter;
use Spatie\QueryBuilder\QueryBuilder;

class ProjectController extends Controller
{
    public function index(Request $request): AnonymousResourceCollection
    {
        // Tenant Scoping & Query Builder Whitelisting
        $projects = QueryBuilder::for(Project::where('user_id', $request->user()->id))
            ->allowedFilters([
                'status',
                'title',
                AllowedFilter::exact('priority'),
                AllowedFilter::scope('search'),
            ])
            ->allowedSorts(['created_at', 'title', 'priority'])
            ->allowedIncludes(['user'])
            ->defaultSort('-created_at')
            ->paginate($request->integer('per_page', 15));

        return ProjectResource::collection($projects);
    }

    public function store(StoreProjectRequest $request): JsonResponse
    {
        $this->authorize('create', Project::class);

        $project = $request->user()->projects()->create($request->validated());

        return (new ProjectResource($project))
            ->response()
            ->setStatusCode(201);
    }

    public function show(Project $project): ProjectResource
    {
        $this->authorize('view', $project);

        return new ProjectResource($project->loadMissing('user'));
    }

    public function update(UpdateProjectRequest $request, Project $project): ProjectResource
    {
        $this->authorize('update', $project);

        $project->update($request->validated());

        return new ProjectResource($project);
    }

    public function destroy(Project $project): JsonResponse
    {
        $this->authorize('delete', $project);

        $project->delete();

        return response()->json(null, 204);
    }
}
