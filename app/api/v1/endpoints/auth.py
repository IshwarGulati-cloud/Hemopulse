from fastapi import APIRouter, HTTPException, status

from app.core.database import get_supabase_client
from app.schemas.auth import SignupRequest, SignupResponse

router = APIRouter()


@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(payload: SignupRequest) -> SignupResponse:
    try:
        client = get_supabase_client()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Account signup is not configured.",
        ) from None

    try:
        result = client.auth.sign_up(
            {
                "email": payload.email.strip(),
                "password": payload.password.get_secret_value(),
            }
        )
    except Exception:
        # Avoid returning provider details, which may contain account or configuration data.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signup could not be completed. Check the email, password, and Supabase Auth settings.",
        ) from None

    if result.user is None or result.user.email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signup could not be completed. Check the email and Supabase Auth settings.",
        )

    return SignupResponse(
        user_id=str(result.user.id),
        email=result.user.email,
        email_confirmation_required=result.session is None,
        message=(
            "Signup successful. Check your email to confirm the account."
            if result.session is None
            else "Signup successful."
        ),
    )
