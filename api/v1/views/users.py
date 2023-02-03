from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.v1.serializers.users import ChefSerializer
from apps.users.models import Chef


class ChefViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Chef's Model
    """
    serializer_class = ChefSerializer
    queryset = Chef.objects.filter(active=True).order_by('nickname')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.active = False
            instance.save()
        else:
            raise NotFound(_('Chef Not Found.'))
        return Response(status=status.HTTP_204_NO_CONTENT, content_type='json')
