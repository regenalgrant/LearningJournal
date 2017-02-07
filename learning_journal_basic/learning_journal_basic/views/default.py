"""Setting up views."""
from pyramid.view import view_config
from ..models import MyEntry
from pyramid.httpexceptions import HTTPNotFound


@view_config(route_name="home", renderer="../templates/list.jinja2")
def list_view(request):
    """Creating list views."""
    query = request.dbsession.query(MyEntry).order_by(
        MyEntry.creation_date.desc()
    )
    entries = query.all()
    return {"entries": entries}


@view_config(route_name="detail", renderer="../templates/detail.jinja2")
def detail_view(request):
    """Creating detail view."""
    entry_id = int(request.matchdict["id"])
    entry = request.dbsession.query(MyEntry).get(entry_id)
    if entry is None:
        raise HTTPNotFound
    return {"entry": entry}


@view_config(route_name="create", renderer="../templates/create.jinja2")
def create_view(request):
    """Making a create view."""
    if request.method == "POST":
        return {}
    return {}


@view_config(route_name="update", renderer="../templates/update.jinja2")
def update_view(request):
    """Creating an Update view."""
    entry_id = int(request.matchdict["id"])
    entry = request.dbsession.query(MyEntry).get(entry_id)
    if entry is None:
        raise HTTPNotFound
    if request.method == "POST":
            entry.title = request.POST["title"]
            entry.blog_entry = request.POST["blog_entry"]
            entry = MyEntry(
                title=entry.title,
                blog_entry=entry.blog_entry,
                creation_date=entry.creation_date
            )
    return {"entry": entry}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_basic_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
