from rest_framework import serializers

from .models import Feedback, FeedbackCategory


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"