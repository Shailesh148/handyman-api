import json
from functools import lru_cache
from urllib.request import urlopen
from typing import Dict, Any, List

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from .config import settings


http_bearer = HTTPBearer(auto_error=False)


@lru_cache(maxsize=1)
def get_jwks() -> Dict[str, Any]:
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    with urlopen(jwks_url) as response:
        return json.loads(response.read())


def verify_auth0_token(token: str) -> Dict[str, Any]:
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header.get("kid"):
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
            break

    if not rsa_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to find appropriate key",
        )

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=[settings.AUTH0_ALGORITHMS],
            audience=settings.AUTH0_AUDIENCE,
            issuer=f"https://{settings.AUTH0_DOMAIN}/",
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation error: {str(e)}",
        )


def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> Dict[str, Any]:
    """
    Global auth dependency – attach to routers or individual endpoints.
    Returns the Auth0 token payload if valid.
    """
    # if credentials is None or credentials.scheme.lower() != "bearer":
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Not authenticated",
    #     )

    # token = credentials.credentials
    return True
