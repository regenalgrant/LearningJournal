import pytest
import transaction
import os
import faker
import random
from pyramid import testing
from .models import (
    MyEntry,
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from .models.meta import Base
from datetime import datetime
from pyramid.httpexceptions import HTTPNotFound

TITLE = ["learning journal 1", "learning journal 2", "learning journal 3"]

FAKE = faker.Faker()

ENTRIES = [MyEntry(
    title=random.choice(TITLE),
    blog_entry=FAKE.text(100),
    creation_date=datetime.utcnow()
    )
        for i in range(3)]

DB_SETTINGS = "sqlite:///:memory:" #setting DB (gloBAL VARIBLE)

@pytest.fixture(scope="session")
def setup_test_env():
    os.environ[ #telling where the database_url test is
        "DATABASE_URL"
        ] = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def sqlengine(request):
    config = testing.setUp(settings={
        "sqlalchemy.url": DB_SETTINGS
        # "sqlite:///:memory:"
    })
    config.include(".models")
    config.include(".routes")
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    def teardown():
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine

@pytest.fixture(scope="function")
def new_session(sqlengine, request):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    def teardown():
        transaction.abort()
    request.addfinalizer(teardown)
    return session

def test_model_get_added(new_session):
    assert len(new_session.query(MyEntry).all()) == 0

@pytest.fixture()
def dummy_request(new_session):
    """creating a dummy request."""
    d_request = testing.DummyRequest(dbsession=new_session)
    return d_request

#------------------unittest-------------------------

def test_list_view(dummy_request, new_session):
    """Test list view returns my entry titles."""
    from .views.default import list_view
    new_session.add(MyEntry(
        title="testing title",
        creation_date=datetime.utcnow(),
        blog_entry="test blog entry"
    ))
    new_session.flush()
    response = list_view(dummy_request)
    assert response['entries'][0].title == "testing title"

def test_detail_view(new_session):
    """Test detail view return blog entry."""
    from .views.default import detail_view
    req = testing.DummyRequest(dbsession=new_session)
    new_session.add(MyEntry(
        title="testing title",
        creation_date=datetime.utcnow(),
        blog_entry="test blog entry"
    ))
    new_session.flush()
    req.matchdict = {"id": 1}
    response = detail_view(req)
    assert response['entry'].blog_entry == "test blog entry"

def test_create_view(dummy_request):
    """Test create view returning an empty dictionary."""
    from .views.default  import create_view
    response = create_view(dummy_request)
    assert response == {}

def test_create_page_takes_user_input(new_session, dummy_request):
    """Testing create page returns user input."""
    from .views.default import create_view
    dummy_request.method = 'POST' #making post request
    dummy_request.POST['title'] = "title" #setting info that user is posting
    dummy_request.POST['blog_entry'] = "blog_entry" #setting info that user is posting
    create_view(dummy_request) #calling create view function passing it your updated dummy request
    query = new_session.query(MyEntry).first()#give me 1st item in database(query)
    assert query.title == "title" #saying that that info we got back from db includes the attribut title

def test_update_view_error_when_no_entry(dummy_request):
    """Ensuring error when no entry found."""
    from .views.default import update_view
    dummy_request.matchdict = {"id": 1}
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)

def test_update_view_takes_changes(new_session, dummy_request):
    """Testing update view take change."""
    from .views.default import update_view
    new_session.add(MyEntry(
        title="original title",
        blog_entry="original entry"
    ))
    new_session.flush()
    dummy_request.method = 'POST'
    dummy_request.POST['blog_entry'] = "blog_entry"
    dummy_request.POST['title'] = "title"
    dummy_request.matchdict = {"id": 1}
    response = update_view(dummy_request)
    assert response.status_code == 302

def test_update_view(dummy_request, new_session):
    """Test update view return blog entry."""
    from .views.default import update_view
    new_session.add(MyEntry(
        title="this is my update",
        creation_date=datetime.utcnow(),
        blog_entry="update sexting"
    ))
    new_session.flush()
    dummy_request.matchdict = {"id": 1}
    response = update_view(dummy_request)
    assert response['entry'].blog_entry == "update sexting"

@pytest.fixture(scope="session")
def testapp(request, setup_test_env):
    from webtest import TestApp
    from learning_journal_basic import main
    app = main({}, **{"sqlalchemy.url": "sqlite:///:memory:"})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)
    return testapp

@pytest.fixture(scope="session")
def fill_db(testapp):
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(ENTRIES)

    return dbsession

@pytest.fixture(scope="function")
def new_session2(testapp, request):
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        session = get_tm_session(SessionFactory, transaction.manager)
    def teardown():
        transaction.abort()
    request.addfinalizer(teardown)
    return session
#----------------------  functional tests --------------------
def test_home_page_returns_list(testapp, fill_db):
    """Testing for titles."""
    response = testapp.get("/", status=200)
    body = response.body.decode('utf-8')
    assert body.count("<h2>") == 4

def test_detail_page_returns_single_entry(testapp, fill_db, new_session2):
    """Testing detail page returns a single entry."""

    response = testapp.get("/journal/1", status=200)
    entry = new_session2.query(MyEntry).get(1)
    assert entry.blog_entry in response.text

def test_detail_page_not_found(testapp, new_session2):
    """Testing for a 404 page."""
    response = testapp.get("/journal/40", status=404)
    entry = new_session2.query(MyEntry).get(40)
    assert "Page Not Found" in response.text

def test_create_page_returns_textarea(testapp):
    """Testing create page returns textarea."""
    response = testapp.get("/journal/new-entry", status=200)
    body = response.body.decode('utf-8')
    assert body.find("</textarea>")

def test_update_page_returns_entry_to_edit(testapp, fill_db, new_session2):
    """Test update page returns an entry to be edited."""
    response = testapp.get("/journal/1/edit-entry", status=200)
    entry = new_session2.query(MyEntry).get(1)
    assert entry.blog_entry in response.text
