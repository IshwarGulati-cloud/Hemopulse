from fastapi import APIRouter, File, HTTPException, UploadFile, status
from app.schemas.predict import ScreeningInputSchema, ScreeningOutputSchema
from app.services.ml_service import ml_service

router = APIRouter()

@router.post("/eyelid", response_model=ScreeningOutputSchema, status_code=status.HTTP_200_OK)
async def predict_anemia_eyelid(payload: ScreeningInputSchema):
    try:
        result = ml_service.predict(payload)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference pipeline failed: {str(e)}")


@router.post("/eyelid/image", response_model=ScreeningOutputSchema)
async def predict_anemia_eyelid_image(photo: UploadFile = File(...)):
    if photo.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(status_code=415, detail="Upload a JPEG or PNG image.")
    try:
        return ml_service.predict_image(await photo.read())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Image inference failed.")
