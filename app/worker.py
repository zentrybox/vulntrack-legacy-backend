from app.core.celery_app import celery_app

# Import tasks to ensure they are registered
import app.core.tasks

if __name__ == "__main__":
    celery_app.worker_main()
