---
name: "api-security-and-policies"
description: "Techniques for eliminating BOLA/IDOR vulnerabilities, applying rate limits, and securing CORS."
version: "1.0.0"
---

# API Security & Policies Skill

## BOLA Policy Pattern
```php
namespace App\Policies;

use App\Models\User;
use App\Models\Project;

class ProjectPolicy
{
    public function view(User $user, Project $project): bool
    {
        return $user->id === $project->user_id;
    }

    public function update(User $user, Project $project): bool
    {
        return $user->id === $project->user_id;
    }

    public function delete(User $user, Project $project): bool
    {
        return $user->id === $project->user_id;
    }
}
```

## Controller Invocation
```php
public function update(UpdateProjectRequest $request, Project $project)
{
    $this->authorize('update', $project);
    $project->update($request->validated());
    return new ProjectResource($project);
}
```
