from api import auth, abort, g, Resource, reqparse
from api.models.tag import TagModel
from api.schemas.tag import TagSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields


@doc(tags=['Tags'])
class TagsResource(MethodResource):
    @marshal_with(TagSchema)
    @doc(summary="Get tag by id")
    def get(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if not tag:
            abort(404, error=f"User with id={tag_id} not found")
        return tag, 200


@doc(tags=['Tags'])
class TagsListResource(MethodResource):
    @doc(summary="Get all tags")
    @marshal_with(TagSchema(many=True))
    def get(self):
        tags = TagModel.query.all()
        return tags, 200

    @doc(summary="Create new tag")
    @use_kwargs({"name": fields.Str(required=True)})
    @marshal_with(TagSchema, code=201)
    def post(self, **kwargs):
        tag = TagModel(**kwargs)
        tag.save()
        return tag, 201
