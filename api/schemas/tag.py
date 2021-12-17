from api import ma
from api.models.tag import TagModel


# Сериализация ответа(response)
class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TagModel
        fields = ("id", "name",)


# Десериализация запроса(request)
class TagRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel

    name = ma.Str()
