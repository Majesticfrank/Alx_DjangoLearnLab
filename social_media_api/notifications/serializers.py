from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source='actor.username', read_only=True)
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor_name', 'verb', 'target_repr', 'is_read', 'timestamp']

    def get_target_repr(self, obj):
        return str(obj.target)
