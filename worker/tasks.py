
import requests
from celery_config import celery_app

@celery_app.task(name='parse_url_task')
def parse_url_task(url: str):
    response = requests.post(
        "http://parser:8000/parse",
        params={"url": url},
        timeout=60,
    )

    return response.json()