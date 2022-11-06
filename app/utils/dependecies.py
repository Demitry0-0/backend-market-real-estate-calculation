from app.utils import users as users_utils
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user = await users_utils.get_user_by_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )
    except Exception:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Bad token"
        )
    return user
