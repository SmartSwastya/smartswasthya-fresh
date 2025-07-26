# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
import jwt
import datetime
from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import get_db
from config import settings
from models.token_log import TokenLog
from handler import auto_logic, auto_route, auto_model

SECRET = settings.JWT_SECRET
blacklist = set()


@auto_logic
async def create_token_logic(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    user = body.get("user", "test_user")
    role = body.get("role", "guest")
    payload = {
        'user': user,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    db.add(TokenLog(username=user, role=role, token=token))
    db.commit()
    return JSONResponse(content={'token': token})


@auto_logic
async def verify_token_post_logic(request: Request):
    body = await request.json()
    token = body.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="Token missing")

    if token in blacklist:
        return JSONResponse(content={'error': '❌ Blacklisted token'}, status_code=403)
    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return JSONResponse(content={'valid': True, 'decoded': decoded})
    except jwt.ExpiredSignatureError:
        return JSONResponse(content={'valid': False, 'error': 'Token expired'}, status_code=401)
    except jwt.InvalidTokenError as e:
        return JSONResponse(content={'valid': False, 'error': str(e)}, status_code=401)


@auto_logic
async def verify_token_query_logic(request: Request):
    token = request.query_params.get("token")
    if not token:
        return JSONResponse(content={'success': False, 'message': 'Token missing'}, status_code=400)
    if token in blacklist:
        return JSONResponse(content={'success': False, 'message': 'Blacklisted'}, status_code=403)
    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return JSONResponse(content={'success': True, 'message': 'Valid', 'decoded': decoded})
    except Exception as e:
        return JSONResponse(content={'success': False, 'message': str(e)}, status_code=401)


@auto_logic
async def blacklist_token_logic(request: Request):
    body = await request.json()
    token = body.get("token")
    if not token:
        return JSONResponse(content={'success': False, 'message': 'Token missing'}, status_code=400)
    blacklist.add(token)
    return JSONResponse(content={'success': True, 'message': 'Token blacklisted'})


@auto_logic
async def expire_token_logic(request: Request):
    # Same logic as blacklist
    return await blacklist_token_logic(request)


@auto_model
@auto_route
@auto_logic
def get_all_tokens_logic(db: Session = Depends(get_db)):
    logs = db.query(TokenLog).all()
    data = [{
        'user': log.username,
        'role': log.role,
        'token': log.token,
        'status': log.status
    } for log in logs]
    return JSONResponse(content={'success': True, 'tokens': data})


@auto_model
@auto_route
@auto_logic
def list_tokens_logic(request: Request, db: Session = Depends(get_db)):
    search = request.query_params.get("search", "").lower()
    query = db.query(TokenLog)
    if search:
        from sqlalchemy import or_
        query = query.filter(
            or_(
                TokenLog.username.ilike(f"%{search}%"),
                TokenLog.role.ilike(f"%{search}%"),
                TokenLog.token.ilike(f"%{search}%")
            )
        )
    tokens = query.order_by(TokenLog.created_at.desc()).all()
    return JSONResponse(content=[{
        'user': t.username,
        'role': t.role,
        'token': t.token,
        'status': t.status,
        'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for t in tokens])
