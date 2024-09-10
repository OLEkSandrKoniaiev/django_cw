from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.permissions.is_dealership_owner_or_admin import IsOwnerOrAdmin

from apps.dealerships.models import DealershipModel
from apps.dealerships.serializers import DealershipSerializer


class DealershipListView(ListAPIView):
    serializer_class = DealershipSerializer
    queryset = DealershipModel.objects.all()
    permission_classes = (AllowAny,)


class DealershipCreateView(CreateAPIView):
    serializer_class = DealershipSerializer
    queryset = DealershipModel.objects.all()
    permission_classes = (IsAuthenticated,)


class DealershipRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = DealershipSerializer
    queryset = DealershipModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)
        return (IsOwnerOrAdmin(),)
