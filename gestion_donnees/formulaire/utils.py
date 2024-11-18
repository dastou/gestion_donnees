from django.http import Http404
from neomodel import db

def neo4j_get_or_404(model, *args, **kwargs):
    try:
        return model.nodes.get(*args, **kwargs)
    except (model.DoesNotExist, db.DoesNotExist):
        raise Http404(f"{model.__name__} does not exist")