from api import db
from api.models.user import UserModel


class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    text = db.Column(db.String(255), unique=False, nullable=False)
    private = db.Column(db.Boolean(), default=True, nullable=False)

    @classmethod
    def get_all_for_user(cls, author):
        return cls.query.filter((NoteModel.author.has(id=author.id)) | (NoteModel.private == False))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
