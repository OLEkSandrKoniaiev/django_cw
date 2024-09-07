from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.dealerships.models import DealershipModel
from apps.dealerships.serializers import DealershipSerializer


class DealershipListCreateView(ListCreateAPIView):
    serializer_class = DealershipSerializer
    queryset = DealershipModel.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        return {'request': self.request}
