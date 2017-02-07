import pytest
import transaction
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

TITLE = ["learning journal 1", "learning journal 2", "learning journal 3"]

FAKE = faker.Faker()

ENTRIES = [MyEntry(
    title=random.choice(TITLE),
    blog_entry=FAKE.text(100),
    creation_date=datetime.utcnow()
)
    for i in range(3)]


@pytest.fixture(scope="function")
def sqlengine(request):
    config = testing.setUp(settings={
        "sqlalchemy.url": "sqlite:///:memory:"
    })
    config.include(".models")
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    def teardown():
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


def test_model_get_added(new_session):
    assert len(new_session.query(MyEntry).all()) == 0


@pytest.fixture()
def dummy_request(new_session):
    """Creating a dummy request."""
    d_request = testing.DummyRequest(dbsession=new_session)
    return d_request


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
    from .views.default import create_view
    response = create_view(dummy_request)
    assert response == {}


def test_update_view(dummy_request, new_session):
    """Test update view return blog entry."""
    from .views.default import update_view
    new_session.add(MyEntry(
        title="this is my update",
        creation_date=datetime.utcnow(),
        blog_entry="update to blog entry"
    ))
    new_session.flush()
    dummy_request.matchdict = {"id": 1}
    response = update_view(dummy_request)
    assert response['entry'].blog_entry == "update sexting"


# ----------------------  functional tests --------------------

@pytest.fixture(scope="session")
def testapp(request):
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
def new_session(testapp, request):
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        session = get_tm_session(SessionFactory, transaction.manager)

    def teardown():
        transaction.abort()
    request.addfinalizer(teardown)
    return session


def test_home_page_returns_list(testapp, fill_db):
    """Testing for titles."""
    response = testapp.get("/", status=200)
    body = response.body.decode('utf-8')
    assert body.count("<h2>") == 4


def test_detail_page_returns_single_entry(testapp, new_session):
    """Testing detail page returns a single entry."""
    response = testapp.get("/journal/1", status=200)
    entry = new_session.query(MyEntry).get(1)
    assert entry.blog_entry in response.text


def test_create_page_returns_textarea(testapp):
    """Testing create page returns textarea."""
    response = testapp.get("/journal/new-entry", status=200)
    body = response.body.decode('utf-8')
    assert body.find("</textarea>")


def test_update_page_returns_entry_to_edit(testapp, new_session):
    """Test upsdate page returns an entry to be edited."""
    response = testapp.get("/journal/1/edit-entry", status=200)
    entry = new_session.query(MyEntry).get(1)
    assert entry.blog_entry in response.text
