# app/routers/users.py
from typing import Annotated
from fastapi import Path, HTTPException, Query, APIRouter, Depends, status
from datetime import datetime
from app.models.users import UserModel
from app.schemas.users import UserCreateRequest, UserUpdateRequest, UserSearchParams, Token
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.auth_jwt import get_current_user, create_access_token
# 유저 라우터 생성
user_router = APIRouter(
    prefix="/users",
    tags=["user"]
)

#--------------------일반 유저 CRUD--------------------

# 유저 생성: POST /users
@user_router.post('')
async def create_user(data: UserCreateRequest):
    user = UserModel.create(**data.model_dump())
    return user.id

# 모든 유저 조회: GET /users
@user_router.get('')
async def get_all_users():
    result = UserModel.all()
    if not result:
        raise HTTPException(status_code=404)
    return result

# 유저 검색: GET /users/search
@user_router.get('/search')
async def search_users(query_params: Annotated[UserSearchParams, Query()]):
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
    filtered_users = UserModel.filter(**valid_query)
    if not filtered_users:
        raise HTTPException(status_code=404)
    return 	filtered_users

# 틀정 유저 조회: GET /users/{user_id}
@user_router.get('/{user_id}')
async def get_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return user

# 유저 정보 수정: PATCH /users/{user_id}
@user_router.patch('/{user_id}')
async def update_user(data: UserUpdateRequest, user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    user.update(**data.model_dump())
    return user

# 유저 삭제: DELETE /users/{user_id}
@user_router.delete('/{user_id}')
async def delete_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    user.delete()
    return {'detail': f'User: {user_id}, Successfully Deleted.'}

# ---------------------로그인 및 JWT 관련------------------------

# 유저 로그인 및 JWT 토근 발급: POST /users/login
@user_router.post('/login', response_model=Token)
async def login_user(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
	user = UserModel.authenticate(data.username, data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	access_token = create_access_token(data={"user_id": user.id})
	user.update(last_login=datetime.now())
	return Token(access_token=access_token, token_type="bearer")

# 현재 로그인된 유저 정보 조회: GET /users/me
@user_router.get('/me')
async def get_user(user: Annotated[UserModel, Depends(get_current_user)]):
	return user

# 현재 로그인된 유저 정보 수정: PATCH /users/me
@user_router.patch('/me')
async def update_user(
	user: Annotated[UserModel, Depends(get_current_user)],
	data: UserUpdateRequest,
):
	if user is None:
		raise HTTPException(status_code=404)
	user.update(**data.model_dump())
	return user

# 현재 로그인된 유저 정보 삭제: DELETE /users/me
@user_router.delete('/me')
async def delete_user(user: Annotated[UserModel, Depends(get_current_user)]):
	user.delete()
	return {'detail': 'Successfully Deleted.'}