
import requests
from fastapi import HTTPException

USER_SERVICE_URL = "http://127.0.0.1:8002"


def get_user_by_id(user_id: int):
    url = f"{USER_SERVICE_URL}/users/{user_id}"

    try:
        response = requests.get(url, timeout=5)
        return response

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="User Service timeout"
        )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="User Service is unavailable"
        )
