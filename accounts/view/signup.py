from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from accounts.serializers import GhasedSignUpSerializer
from accounts.jwt import get_jwt_token


class GhasedSignUpView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = GhasedSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        refresh, access = get_jwt_token(account)
        return Response(data={
            'access_token': access,
            'refresh_token': refresh
        }, status=HTTP_200_OK)
