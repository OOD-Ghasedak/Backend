from rest_framework.serializers import ModelSerializer

from channels.models import ChannelContent


class ContentSerializer(ModelSerializer):

    class Meta:
        model = ChannelContent


class FreeContentSerializer(ContentSerializer):
    class Meta(ContentSerializer.Meta):
        fields = [
            'title', 'summary', 'is_perimum',
        ]


class
