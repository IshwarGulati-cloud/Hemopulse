from pydantic import BaseModel, Field, SecretStr


class SignupRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=320)
    password: SecretStr = Field(..., min_length=8, max_length=128)


class SignupResponse(BaseModel):
    user_id: str
    email: str
    email_confirmation_required: bool
    message: str
