from rest_framework import serializers

from main.models import Key, NewKeysCounter


class KeySerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()

    class Meta:
        model = Key
        fields = ('value', 'status')

    def get_status(self, obj):
        return obj.get_status_display()


class NewKeysCounterSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewKeysCounter
        fields = ('new_keys', )
