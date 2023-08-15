from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView
from accounts.views.serializers import GhasedSignUpSerializer


class GhasedSignUpView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = GhasedSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ghased = serializer.save()
        refresh, access = ghased.get_jwt_tokens()
        return Response(data={
            'access_token': access,
            'refresh_token': refresh
        }, status=HTTP_201_CREATED)
