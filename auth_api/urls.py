from .api import EntryResource
from tastypie.api import Api
from django.urls import path
from .views import index


v1_api = Api(api_name='v1')
v1_api.register(EntryResource())

urlpatterns = [
    path('', index, name='index'),
]