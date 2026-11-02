from typing import Literal, Optional

from pydantic import BaseModel, Field

class ScreeningInputSchema(BaseModel):
    red_ratio: float = Field(..., ge=0.0, le=100.0, description="Percentage of Red pixels extracted from eyelid ROI")
    green_ratio: float = Field(..., ge=0.0, le=100.0, description="Percentage of Green pixels extracted from eyelid ROI")
    blue_ratio: float = Field(..., ge=0.0, le=100.0, description="Percentage of Blue pixels extracted from eyelid ROI")
    patient_age: Optional[int] = Field(None, ge=0, le=120)
    patient_gender: Optional[str] = Field(None, pattern="^(Male|Female|Other)$")

class ScreeningOutputSchema(BaseModel):
    anemic_status: str
    risk_level: Literal["Normal", "Mild", "Moderate", "Severe"]
    confidence_score: float
    recommended_action: str
    demo_only: bool
