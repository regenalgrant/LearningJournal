"""presenting view to the user in a human readable format."""
from pyramid.view import view_config

ENTRIES = [
    {"title": "Blog - Day 10", "creation_date": "Aug 19, 2016", "id": 10, "body": "Sample body text."},
    {"title": "Blog - Day 11", "creation_date": "Aug 22, 2016", "id": 11, "body": "Sample body text."},
    {"title": "Blog - Day 12", "creation_date": "Aug 23, 2016", "id": 12, "body": "Sample body text."},
]

@view_config(route_name="home", renderer="templates/list.jinja2")
def list_view(request):
    return {"entries": ENTRIES}

@view_config(route_name="detail", renderer="templates/detail.jinja2")
def detail_view(request):
    return {"title": "entry title",
            "creation_date": "Jan",
            "body": "this my body"}

@view_config(route_name="create", renderer="templates/create.jinja2")
def create_view(request):
    return "create view"

@view_config(route_name="update", renderer="templates/update.jinja2")
def update_view(request):
    return "update_view"
