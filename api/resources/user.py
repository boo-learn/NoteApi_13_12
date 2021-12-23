from api import Resource, abort, reqparse, auth
from api.models.user import UserModel
from api.schemas.user import UserSchema, UserRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields

# language=YAML <-- оставил для примера
"""
Get User by id
---
tags:
    - Users
parameters:
     - in: path
       name: user_id
       type: integer
       required: true
       default: 1
responses:
   200:
       description: A single user item
       schema:
           id: User
           properties:
               id:
                   type: integer
                   description: user id
                   default: 1
               username:
                   type: string
                   description: The name of the user
                   default: Steven Wilson
               is_staff:
                   type: boolean
                   description: user is staff
                   default: false
               role:
                   type: string
                   description: user role
                   default: simple_user
"""


@doc(tags=['Users'])
class UserResource(MethodResource):
    @doc(summary="Get user by id", description="Returns single user")
    @doc(responses={404: {"description": 'User not found'}})
    @marshal_with(UserSchema, code=200)
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id={user_id} not found")
        return user, 200

    @auth.login_required(role="admin")
    @doc(summary="Edit user by id")
    @use_kwargs({"username": fields.Str(), "role": fields.Str()})
    @marshal_with(UserSchema)
    @doc(responses={401: {"description": "Not authorization"}})
    @doc(responses={404: {"description": 'User not found'}})
    @doc(security=[{"basicAuth": []}])
    def put(self, user_id, **kwargs):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id={user_id} not found")
        user.username = kwargs.get("username") or user.username
        user.role = kwargs.get("role") or user.role
        user.save()
        return user, 200

    @auth.login_required(role="admin")
    @doc(summary='Delete user by id')
    @doc(responses={401: {"description": "Not authorization"}})
    @doc(responses={404: {"description": "Not found"}})
    @marshal_with(UserSchema)
    @doc(security=[{"basicAuth": []}])
    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id:{user_id} not found")
        user.delete()
        return user, 200


@doc(description='Api for notes.', tags=['Users'])
class UsersListResource(MethodResource):
    @doc(summary="Get all Users")
    @marshal_with(UserSchema(many=True), code=200)
    def get(self):
        users = UserModel.query.all()
        return users, 200

    @doc(summary="Create new User")
    @marshal_with(UserSchema, code=201)
    @doc(responses={400: {"description": "User with username already exist"}})
    @use_kwargs(UserRequestSchema, location=('json'))
    def post(self, **kwargs):
        user = UserModel(**kwargs)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        return user, 201


@doc(description='Api for users.', tags=['Users'])
class UsersSearchResource(MethodResource):
    @doc(summary="Get list of all users by search")
    @use_kwargs({"username": fields.Str()}, location=('query'))
    @marshal_with(UserSchema(many=True), code=200)
    def get(self, **kwargs):
        users = []
        if kwargs.get("username"):
            users = UserModel.query.filter(UserModel.username.like(f'%{kwargs["username"]}%')).all()
        return users, 200

# endpoint: /users/search