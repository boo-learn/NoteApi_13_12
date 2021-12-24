from api import db


class MixinMethods:
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self.archive = True
        self.save()
