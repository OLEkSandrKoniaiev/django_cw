from django.utils.decorators import method_decorator

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from core.permissions.is_dealership_owner_or_admin import IsOwnerOrAdmin

from apps.dealerships.models import DealershipModel
from apps.dealerships.serializers import DealershipSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(security=[],))
class DealershipListView(ListAPIView):
    """
    get:
    Returns a list of all available car dealerships. Open to any user, no authentication required.
    """
    serializer_class = DealershipSerializer
    queryset = DealershipModel.objects.all()
    permission_classes = (AllowAny,)


class DealershipCreateView(CreateAPIView):
    """
    post:
    Allows authenticated users to create a new car dealership. Requires user authentication.
    """
    serializer_class = DealershipSerializer
    queryset = DealershipModel.objects.all()
    permission_classes = (IsAuthenticated,)


class DealershipRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    patch:
    Handles retrieving, updating, and deleting a specific car dealership. GET requests are open to any user,
    while other methods require the user to be the owner or an admin.
    put:
    Handles retrieving, updating, and deleting a specific car dealership. GET requests are open to any user,
    while other methods require the user to be the owner or an admin.
    get:
    Handles retrieving, updating, and deleting a specific car dealership. GET requests are open to any user,
    while other methods require the user to be the owner or an admin.
    delete:
    Handles retrieving, updating, and deleting a specific car dealership. GET requests are open to any user,
    while other methods require the user to be the owner or an admin.
    """
    serializer_class = DealershipSerializer
    queryset = DealershipModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)
        return (IsOwnerOrAdmin(),)
