from api import ma
from api.models.user import UserModel


#       schema        flask-restful
# object ------>  dict ----------> json


# Сериализация ответа(response)
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        fields = ('id', 'username', "is_staff", "role")

    # id = ma.auto_field()
    # username = ma.auto_field()
    # is_staff = ma.auto_field()
    # role = ma.auto_field()


# Десериализация запроса(request)
# json --> dict (**kwargs)
class UserRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    username = ma.Str(required=True)
    password = ma.Str(required=True)
    role = ma.Str()
