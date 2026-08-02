from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .models import Principal

IAP_CERTS_URL = "https://www.gstatic.com/iap/verify/public_key"
IAP_ISSUER = "https://cloud.google.com/iap"


class IdentityError(ValueError):
    """The request has no valid trusted identity."""


@dataclass(frozen=True)
class IapJwtVerifier:
    expected_audience: str
    decoder: Callable[[str, str], Mapping[str, Any]] | None = None

    def verify(self, encoded_jwt: str | None) -> Principal:
        if not encoded_jwt:
            raise IdentityError("missing IAP signed assertion")
        try:
            claims = (
                self.decoder(encoded_jwt, self.expected_audience)
                if self.decoder
                else self._decode_with_google_auth(encoded_jwt)
            )
        except Exception as exc:
            raise IdentityError("IAP signed assertion validation failed") from exc
        if claims.get("iss") != IAP_ISSUER:
            raise IdentityError("unexpected IAP token issuer")
        subject = claims.get("sub")
        email = claims.get("email")
        if not isinstance(subject, str) or not subject:
            raise IdentityError("IAP token has no stable subject")
        if not isinstance(email, str) or not email:
            raise IdentityError("IAP token has no email")
        google_claim = claims.get("google", {})
        raw_levels = (
            google_claim.get("access_levels", [])
            if isinstance(google_claim, dict)
            else []
        )
        levels = frozenset(str(item) for item in raw_levels)
        return Principal(subject=subject, email=email, access_levels=levels)

    def _decode_with_google_auth(self, encoded_jwt: str) -> Mapping[str, Any]:
        from google.auth.transport import requests
        from google.oauth2 import id_token

        return id_token.verify_token(
            encoded_jwt,
            requests.Request(),
            audience=self.expected_audience,
            certs_url=IAP_CERTS_URL,
        )

