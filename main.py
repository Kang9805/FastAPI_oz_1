# main.py
from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Query
from app.models.movies import MovieModel
from app.models.users import UserModel
from app.schemas.movies import MovieResponse, CreateMovieRequest, MovieSearchParams, MovieUpdateRequest
from app.schemas.users import UserCreateRequest, UserUpdateRequest, UserSearchParams


app = FastAPI()

UserModel.create_dummy() # API 테스트를 위한 더미를 생성하는 메서드 입니다.
UserModel.create_dummy()
MovieModel.create_dummy()



# 유저 생성 API
@app.post('/users')
async def create_user(data: UserCreateRequest):
    user = UserModel.create(**data.model_dump())
    return user.id

# 모든 유저 정보를 가져오는 API
@app.get('/users')
async def get_all_users():
    result = UserModel.all()
    if not result:
        raise HTTPException(status_code=404)
    return result

# 유저 정보를 가져오는 API
@app.get('/users/{user_id}')
async def get_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return user

# 유저 정보를 부분 수정하는 API
@app.patch('/users/{user_id}')
async def update_user(data: UserUpdateRequest, user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    user.update(**data.model_dump())
    return user

# 유저 삭제 API
@app.delete('/users/{user_id}')
async def delete_user(user_id: int = Path(gt=0)):
    user = UserModel.get(id=user_id)
    if user is None:
        raise HTTPException(status_code=404)
    user.delete()

    return {'detail': f'User: {user_id}, Successfully Deleted'}

# 유저 검색 API
@app.get('/users/search')
async def search_users(query_params: Annotated[UserSearchParams, Query()]):
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}
    filtered_users = UserModel.filter(**valid_query)
    if not filtered_users:
        raise HTTPException(status_code=404)
    return 	filtered_users




# 영화 등록 API
@app.post('/movies', response_model=MovieResponse, status_code=201)
async def create_movie(data: CreateMovieRequest):
    movie = MovieModel.create(**data.model_dump())
    return movie

# 전체 영화 검색 및 리스트 조회 API
@app.get('/movies', response_model=list[MovieResponse], status_code=200)
async def get_movie(query_params: Annotated[MovieSearchParams, Query()]):
    valid_query = {key: value for key, value in query_params.model_dump().items() if value is not None}

    if valid_query:
        return MovieModel.filter(**valid_query)
    return MovieModel.all()

# 특정 영화 상세 조회 API
@app.get('/movies/{movie_id}', response_model=MovieResponse, status_code=200)
async def get_movie(movie_id: int = Path(gt=0)):
    movie = MovieModel.get(id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404)
    return movie

# 특정 영화 정보 수정 API
@app.patch('/movies/{movie_id}', response_model=MovieResponse, status_code=200)
async def edit_movie(data: MovieUpdateRequest, movie_id: int = Path(gt=0)):
	movie = MovieModel.get(id=movie_id)
	if movie is None:
		raise HTTPException(status_code=404)
	movie.update(**data.model_dump())
	return movie

# 특정 영화 정보 삭제 API
@app.delete('/movies/{movie_id}', status_code=204)
async def delete_movie(movie_id: int = Path(gt=0)):
	movie = MovieModel.get(id=movie_id)
	if movie is None:
		raise HTTPException(status_code=404)
	movie.delete()
	return


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
