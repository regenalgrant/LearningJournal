import pytest
import transaction
from pyramid import testing
from .models import (
    MyEntry,
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from .models.meta import Base
from datetime import datetime

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

@pytest.fixture(scope="function")
def new_session(sqlengine, request):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    def teardown():
        transaction.abort()
    request.addfinalizer(teardown)
    return session

@pytest.fixture(scope="function")
def populate_db(request, sqlengine):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    with transaction.manager:
        session.add(MyEntry(
            title="Learning Journal",
            creation_date=datetime.utcnow(),
            blog_entry="blog_entry"
        ))
    def teardown():
        with transaction.manager:
            session.query(MyEntry).delete()

    request.addfinalizer(teardown)

def test_model_get_added(new_session):
    assert len(new_session.query(MyEntry).all()) == 0

@pytest.fixture()
def dummy_request(new_session):
    """creating a dummy request."""
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
    from .views.default  import create_view
    response = create_view(dummy_request)
    assert response == {}

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
