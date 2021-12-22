from api import abort


def get_or_404(model, id):
    object = model.query.get(id)
    if not object:
        abort(404, error=f"note {id} not found")
    return object
