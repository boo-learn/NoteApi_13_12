from api import db
from api.models.user import UserModel
from api.models.tag import TagModel
from sqlalchemy.sql import expression

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('note_model_id', db.Integer, db.ForeignKey('note_model.id'), primary_key=True)
                )


class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    text = db.Column(db.String(255), unique=False, nullable=False)
    private = db.Column(db.Boolean(), default=True, nullable=False)
    tags = db.relationship(TagModel, secondary=tags, lazy='subquery', backref=db.backref('notes', lazy=True))
    archive = db.Column(db.Boolean(), default=False, server_default=expression.false(), nullable=False)

    @classmethod
    def get_all_for_user(cls, author):
        return cls.query.filter((NoteModel.author.has(id=author.id)) | (NoteModel.private == False))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
