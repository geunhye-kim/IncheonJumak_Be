from rest_framework import serializers
from alchol.models import Alchol


class AlcholSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alchol
        fields = "__all__"

class AlcholListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alchol
        fields = "__all__"