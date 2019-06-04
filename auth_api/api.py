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

    def delete_list(self, object_list, bundle):
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


class CookieAuthentication(BasicAuthentication):
    def __init__(self, *args, **kwargs):
        super(CookieAuthentication, self).__init__(*args, **kwargs)

    def is_authenticated(self, request, **kwargs):
        from django.contrib.sessions.models import Session
        if 'sessionid' in request.COOKIES:
            s = Session.objects.get(pk=request.COOKIES['sessionid'])
            if '_auth_user_id' in s.get_decoded():
                u = User.objects.get(id=s.get_decoded()['_auth_user_id'])
                if request.user == u:
                    return True
        return super(CookieAuthentication, self).is_authenticated(request, **kwargs)


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
        authentication = CookieAuthentication()
        authorization = UserObjectsOnlyAuthorization()

