from rest_framework import serializers

from .models import AcceptedActivity, RejectedActivity, SavedActivity


class AcceptedActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptedActivity
        fields = "__all__"


class RejectedActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RejectedActivity
        fields = "__all__"


class SavedActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedActivity
        fields = "__all__"
