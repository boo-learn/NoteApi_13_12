from api import api, app, docs
from api.resources import note
from api.resources.user import UserResource, UsersListResource, UsersSearchResource
from api.resources.auth import TokenResource
from api.resources.tag import TagsResource, TagsListResource
from api.resources.file import UploadPictureResource
from config import Config

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE
api.add_resource(UsersListResource,
                 '/users')  # GET, POST
api.add_resource(UsersSearchResource,
                 '/users/search')  # GET
api.add_resource(UserResource,
                 '/users/<int:user_id>')  # GET, PUT, DELETE

api.add_resource(TokenResource,
                 '/auth/token')  # GET

api.add_resource(note.NotesListResource,
                 '/notes',  # GET, POST
                 )
api.add_resource(note.NoteResource,
                 '/notes/<int:note_id>',  # GET, PUT, DELETE
                 )

api.add_resource(TagsListResource,
                 '/tags')  # GET, POST
api.add_resource(TagsResource,
                 '/tags/<int:tag_id>')  # GET, PUT, DELETE

api.add_resource(note.NoteSetTagsResource,
                 '/notes/<int:note_id>/add_tags')  # PUT
api.add_resource(note.NoteFilerResource,
                 '/notes/public/filter')  # PUT


docs.register(UserResource)
docs.register(UsersListResource)
docs.register(note.NoteResource)
docs.register(note.NotesListResource)
docs.register(TagsResource)
docs.register(TagsListResource)
docs.register(note.NoteSetTagsResource)
docs.register(note.NoteFilerResource)
docs.register(note.NoteArchive)
docs.register(UploadPictureResource)
docs.register(UsersSearchResource)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
