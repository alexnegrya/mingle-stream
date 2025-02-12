from rest_framework import serializers


class ChangeChatSerializer(serializers.Serializer):
    chat_id = serializers.IntegerField(required=True)
    title = serializers.CharField(required=False, max_length=25)
    description = serializers.CharField(required=False, max_length=10000)
    img_url = serializers.URLField(required=False)
    bg_url = serializers.URLField(required=False)
