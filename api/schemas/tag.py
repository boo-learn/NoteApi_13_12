# Сериализация ответа(response)
class TagSchema(ma.SQLAlchemyAutoSchema):
   class Meta:
       model = TagModel
       fields = ("name",)


# Десериализация запроса(request)
class TagRequestSchema(ma.SQLAlchemySchema):
   class Meta:
       model = TagModel

   name = ma.Str()
