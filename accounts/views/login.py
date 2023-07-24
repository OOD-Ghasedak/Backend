from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from accounts.models import Ghased
from accounts.views.serializers import GhasedLoginSerializer


class GhasedLoginView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = GhasedLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        ghased = Ghased.objects.get(user__username=validated_data['username'])
        refresh, access = ghased.get_jwt_tokens()
        return Response(data={
            'access_token': access,
            'refresh_token': refresh
        }, status=HTTP_200_OK)
