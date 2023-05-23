from rest_framework import serializers
from information.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"