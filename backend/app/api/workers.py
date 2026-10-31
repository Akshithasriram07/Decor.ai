from uuid import uuid4
from fastapi import APIRouter
from app.api.deps import DB, CurrentUser
from app.models import WorkerApplication
from app.schemas.worker import WorkerApplicationRequest
router=APIRouter(prefix="/api/worker-applications",tags=["Worker Applications"])
@router.post("")
def apply(payload:WorkerApplicationRequest,user:CurrentUser,db:DB):
    item=WorkerApplication(id=str(uuid4()),user_id=user.id,**payload.model_dump())
    db.add(item); db.commit()
    return {"message":"Your local worker application has been submitted.","status":"pending"}
