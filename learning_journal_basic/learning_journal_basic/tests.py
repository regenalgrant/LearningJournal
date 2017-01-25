import pytest
from pyramid import testing


# class ViewTests(unittest.TestCase):
#     def setUp(self):
#         self.config = testing.setUp()
#
#     def tearDown(self):
#         testing.tearDown()
#
#     def test_my_view(self):
#         from .views import my_view
#         request = testing.DummyRequest()
#         info = my_view(request)
#         self.assertEqual(info['project'], 'learning_journal_basic')

def test_list_view():
    """Testing if list populates within the list view."""
    from .views import list_view
    request = testing.DummyRequest()
    info = list_view(request)
    assert "id" in info['entries'][2] 

def test_detail_view():
    """Test that what's returned by the view contains what we expect."""
    from .views import detail_view
    request = testing.DummyRequest()
    info = detail_view(request)
    assert "title" in info

# class FunctionalTests(unittest.TestCase):
#     def setUp(self):
#         from learning_journal_basic import main
#         app = main({})
#         from webtest import TestApp
#         self.testapp = TestApp(app)
#
#     def test_root(self):
#         res = self.testapp.get('/', status=200)
#         self.assertTrue(b'Pyramid' in res.body)
#
#     @pytest.fixture()
#     def testapp():
#         """Create an instance of our app for testing."""
#         from learning_journal_basic import main
#         app = main({})
#         from webtest import TestApp
#         return TestApp(app)
#
#     def test_layout_root(testapp):
#         """Test that the contents of the root page contains <article>."""
#         response = testapp.get('/', status=200)
#         html = response.html
#         assert 'Created in the Code Fellows 401 Python Program' in html.find("footer").text
#
#     def test_root_contents(testapp):
#         """Test that the contents of the root page contains as many <article> tags as journal entries."""
#         from .views import ENTRIES
#
#         response = testapp.get('/', status=200)
#         html = response.html
#         assert len(ENTRIES) == len(html.findAll("article"))
