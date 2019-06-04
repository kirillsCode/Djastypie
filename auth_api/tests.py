from django.test import TestCase
from unittest import skip
from auth_api.models import Entry, User
from django.utils import timezone
from tastypie.test import ResourceTestCaseMixin
from django.http.cookie import SimpleCookie


# testing models and api
class EntryTest(ResourceTestCaseMixin, TestCase):

    def setUp(self):
        super(EntryTest, self).setUp()
        self.title = "this is a test"
        self.number_of_entries = 1
        self.username = 'root'
        self.password = 'pass'
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.entry = Entry.objects.create(title=self.title,
                                          user=self.user,
                                          create_date=timezone.now())

    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)

    def tearDown(self):
        pass

    def test_entry_validation(self):
        self.assertTrue(isinstance(self.entry, Entry))
        self.assertEqual(self.entry.__str__(), self.entry.title)

    def test_entry_get(self):
        result = str(Entry.objects.get(pk=1))
        self.assertEqual(self.title, result)

    @skip("WIP")
    def test_entry_update(self):
        Entry.objects.filter(show=0).update(show=1)

    def test_get_api_json(self):
        self.api_client.cookies = SimpleCookie({
            'sessionid': 'go4d6wt6rpx28n3ut1e53r6olgsie3xo|ZTE3M2RhMzA2OGRmODY1Y2I0ZGQ3NDliODkzYmUwNTkyZGZmNzY0YTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYmMwMGRlZDc1Y2UyNTU0MjI4NTJhNzJjNDRkZmY3NjIxZmU3Mjg5In0='})
        resp = self.api_client.get('/api/v1/entry/', format='json',
                                   )
        self.assertValidJSONResponse(resp)

    def test_get_api_xml(self):
        resp = self.api_client.get('/api/v1/entry/', format='xml',
                                   authentication=self.get_credentials())
        self.assertValidXMLResponse(resp)

    def test_get_api_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/v1/entry/'))

