from django.test import TestCase
from auth_api.models import Entry, User
from django.utils import timezone
from tastypie.test import ResourceTestCaseMixin

# testing models
class EntryTest(TestCase):

    def create_user(self, username="test_user", password="rootroot"):
        return User.objects.create(username=username, password=password)

    def create_entry(self, title="this is test"):
        user = self.create_user()
        return Entry.objects.create(title=title, user=user, create_date=timezone.now())

    def test_entry_creation(self):
        e = self.create_entry()
        self.assertTrue(isinstance(e, Entry))
        self.assertEqual(e.__str__(), e.title)


# testing api


class EntryResourceTest(ResourceTestCaseMixin, TestCase):

    def test_get_api_json(self):
        resp = self.api_client.get('/api/v1/entry/', format='json')
        self.assertValidJSONResponse(resp)

    def test_get_api_xml(self):
        resp = self.api_client.get('/api/v1/entry/', format='xml')
        self.assertValidXMLResponse(resp)

