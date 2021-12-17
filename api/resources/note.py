from api import auth, abort, g, Resource, reqparse
from api.models.note import NoteModel
from api.models.tag import TagModel
from flask_apispec import marshal_with, use_kwargs, doc
from sqlalchemy.orm.exc import NoResultFound
from api.schemas.note import NoteSchema, NoteCreateSchema, NoteEditSchema
from flask_apispec.views import MethodResource
from webargs import fields


@doc(tags=['Notes'])
class NoteResource(MethodResource):
    @auth.login_required
    @doc(summary="Get note by id", security=[{"basicAuth": []}])
    @doc(responses={404: {"description": "Not found"}})
    @marshal_with(NoteSchema)
    def get(self, note_id):
        author = g.user
        try:
            note = NoteModel.get_all_for_user(author).filter_by(id=note_id).one()
            return note, 200
        except NoResultFound:
            abort(404, error=(f"Note with id={note_id} not found"))

    @auth.login_required
    @doc(summary="Edit note by id", security=[{"basicAuth": []}])
    @doc(responses={404: {"description": "Not found"}})
    @doc(responses={403: {"description": "Forbidden"}})
    @use_kwargs(NoteEditSchema)
    @marshal_with(NoteSchema)
    def put(self, note_id, **kwargs):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")

        note.text = kwargs.get("text") or note.text
        note.private = kwargs.get("private") or note.private
        note.save()
        return note, 200

    @auth.login_required
    @doc(summary='Delete note by id', security=[{"basicAuth": []}])
    @doc(responses={401: {"description": "Not authorization"}})
    @doc(responses={404: {"description": "Not found"}})
    @marshal_with(NoteSchema, code=200)
    def delete(self, note_id):
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id:{note_id} not found")
        # FIXME: удаление только своих(авторизованного пользователя) заметок
        note.delete()
        return note, 200


@doc(tags=['Notes'])
class NotesListResource(MethodResource):
    @auth.login_required
    @doc(summary="Get notes list", security=[{"basicAuth": []}])
    @marshal_with(NoteSchema(many=True), code=200)
    def get(self):
        # FIXME: получение только своих(авторизованного пользователя) заметок
        notes = NoteModel.query.all()
        return notes, 200

    @auth.login_required
    @doc(summary="Create note", security=[{"basicAuth": []}])
    @marshal_with(NoteSchema, code=201)
    @use_kwargs(NoteCreateSchema)
    def post(self, **kwargs):
        author = g.user
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201


@doc(tags=['Notes'])
class NoteSetTagsResource(MethodResource):
    @doc(summary="Set tags to Note")
    @use_kwargs({"tags": fields.List(fields.Int())}, location=('json'))
    @marshal_with(NoteSchema)
    def put(self, note_id, **kwargs):
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)
            note.tags.append(tag)
        note.save()
        return note, 200
