from api import Resource, abort, reqparse, auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


class UserResource(Resource):
    def get(self, user_id):
        # language=YAML
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
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id={user_id} not found")
        return user_schema.dump(user), 200

    @auth.login_required(role="admin")
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        user_data = parser.parse_args()
        user = UserModel.query.get(user_id)
        user.username = user_data["username"]
        user.save()
        return user_schema.dump(user), 200

    @auth.login_required
    def delete(self, user_id):
        raise NotImplemented  # не реализовано!


class UsersListResource(Resource):
    def get(self):
        # language=YAML
        """
        Get all Users
        ---
        tags:
           - Users
        """

        users = UserModel.query.all()
        return users_schema.dump(users), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("role")
        user_data = parser.parse_args()
        user = UserModel(**user_data)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        return user_schema.dump(user), 201
