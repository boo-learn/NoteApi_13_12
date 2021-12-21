from api import ma
from api.models.note import NoteModel
from api.schemas.user import UserSchema


#       schema        flask-restful
# object ------>  dict ----------> json

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel

    author = ma.Nested(UserSchema())
    _links = ma.Hyperlinks({
        'self': ma.URLFor('noteresource', values=dict(note_id="<id>")),
        'collection': ma.URLFor('noteslistresource')
    })


class NoteCreateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel
        fields = ["text", "private"]


class NoteEditSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel
    text = ma.auto_field(required=False)
    private = ma.auto_field(required=False)
