from tastypie.resources import ModelResource
from .models import Entry
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")


class _BasicAuthentication(BasicAuthentication):
    def _unauthorized(self):
        response = super(_BasicAuthentication, self)._unauthorized()
        response.status_code = 403
        return response


class DjangoAutentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        if request.user.is_authenticated:
            return True
        return False

    def get_identifier(self, request):
        return request.user.username


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authentication = BasicAuthentication()

class EntryResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Entry.objects.filter(show=1)
        resource_name = 'entry'
        allowed_methods = ['get']
        fields = ['title', 'create_date', 'id']

        # Some options here:
        # - if a user is not logged in, then suggest logging in with BasicAuthentication
        #   (so use MultipleAuthentication here)
        # - if a user is not logged in, redirect to login page
        # - leave as it is now
        authentication = DjangoAutentication()
        authorization = UserObjectsOnlyAuthorization()

