from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from accounts.models import IsGhasedPermission
from accounts.views.serializers import ChangePasswordSerializer


class ChangePasswordView(APIView):
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsGhasedPermission]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(request.ghased, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={
            'status': 'ok',
        }, status=HTTP_200_OK)
