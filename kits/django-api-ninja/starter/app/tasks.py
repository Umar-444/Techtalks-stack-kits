from config.celery import app as celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_project_notification(self, project_id: int):
    """Dispatched from create_project via transaction.on_commit.

    Takes a primary key rather than a serialized model: the broker only ever
    carries JSON scalars, so a compromised Redis cannot deliver a pickled
    object graph back into the worker.
    """
    from app.models import Project

    try:
        project = Project.objects.filter(pk=project_id).first()
        if project is None:
            return {"status": "skipped", "reason": "project no longer exists"}
        return {"status": "sent", "project_id": project.id}
    except Exception as exc:
        raise self.retry(exc=exc)
