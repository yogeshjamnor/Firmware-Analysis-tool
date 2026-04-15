from pathlib import Path
import uuid

BASE = Path("workspace")


def create_job():
    job_id = str(uuid.uuid4())
    job_path = BASE / job_id
    job_path.mkdir(parents=True, exist_ok=True)
    return job_path