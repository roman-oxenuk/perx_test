# coding: utf-8
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Key, NewKeysCounter
from main.serializers import KeySerializer, NewKeysCounterSerializer


class KeyIssue(APIView):

    def get(self, request, *args, **kwargs):
        with transaction.atomic():
            key = Key.objects.select_for_update(skip_locked=True).filter(status=Key.NEW).first()
            if key:
                key.status = Key.ISSUED
                key.save()
                return Response(KeySerializer(key).data)

            return Response({'error': 'Нет не выданных ключей'})


class KeyExpire(APIView):

    def get(self, request, *args, **kwargs):
        key_value = kwargs.get('key_value')
        with transaction.atomic():
            key = Key.objects.select_for_update().filter(
                status=Key.ISSUED,
                value=key_value
            ).first()
            if key:
                key.status = Key.EXPIRED
                key.save()
                return Response(KeySerializer(key).data)

            return Response({'error': 'Ключ {0} не выпушен или уже погашен'.format(key_value)}, status=404)


class KeyCheck(APIView):

    def get(self, request, *args, **kwargs):
        key_value = kwargs.get('key_value')
        key = Key.objects.filter(
            value=key_value
        ).first()
        if key:
            return Response(KeySerializer(key).data)

        return Response({'error': 'Ключ {0} не найден'.format(key_value)}, status=404)


class NewKeysCounterView(APIView):

    def get(self, request, *args, **kwargs):
        counter = NewKeysCounter.objects.get(table_name=Key._meta.db_table)
        return Response(NewKeysCounterSerializer(counter).data)
