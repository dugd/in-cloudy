from fastapi import APIRouter
import datetime

router = APIRouter(prefix="/common", tags=["common"])


@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok", "message": "Service is running"}


@router.get("/time")
def get_time():
    return {"server_time": datetime.datetime.now().isoformat()}


@router.get("/error")
def trigger_error():
    division_by_zero = 1 / 0
    return {"division_by_zero": division_by_zero}

__all__ = ["router"]
