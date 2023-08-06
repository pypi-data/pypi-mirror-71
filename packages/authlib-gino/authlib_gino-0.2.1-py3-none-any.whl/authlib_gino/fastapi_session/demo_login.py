import time

from fastapi import Depends
from starlette.requests import Request

from .api import auth, login_context
from .models import Identity
from .models import db
from ..fastapi_session.models import User


async def demo_login(request: Request, context=Depends(login_context)):
    # request should contain all parameters in AUTHORIZATION_ENDPOINT
    user = await (
        User.query.select_from(Identity.outerjoin(User))
        .where(Identity.sub == "demo")
        .where(Identity.idp == "demo")
        .gino.first()
    )
    if user is None:
        user = await db.first(
            db.text(
                """\
WITH new_user AS (
    INSERT INTO users (id, created_at, profile) VALUES (:uid, :now, :up) RETURNING *
), new_id AS (
    INSERT INTO identities (sub, idp, user_id, created_at, profile)
    SELECT :sub, :idp, id, :now, :ip FROM new_user RETURNING id
) SELECT * FROM new_user
"""
            )
            .gino.model(User)
            .query,
            dict(
                uid="usr:demo",
                up='{"name": "demo"}',
                sub="demo",
                idp="demo",
                ip="{}",
                now=int(time.time()),
            ),
        )
    return await auth.create_authorization_response(request, user, context)
