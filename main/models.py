# coding: utf-8
from django.db import models


class Key(models.Model):

    NEW = 0
    ISSUED = 1
    EXPIRED = 2

    KEYS_STATUSES = (
        (NEW, 'Не выдан'),
        (ISSUED, 'Выдан'),
        (EXPIRED, 'Погашен'),
    )

    value = models.CharField(
        verbose_name='Значение ключа',
        max_length=4,
        primary_key=True
    )
    status = models.PositiveIntegerField(
        verbose_name='Статус ключа',
        choices=KEYS_STATUSES,
        default=NEW,
        db_index=True
    )

    class Meta:
        verbose_name = 'Ключ'
        verbose_name_plural = 'Ключи'

    def __str__(self):
        return self.value


class NewKeysCounter(models.Model):
    """
    Модель для хранения кешированого значения Key.objects.filter(status=0).count()
    Заполняется в миграции 0004_insert_counter_initial_value
    и обновляется через триггер, созданный в миграции 0005_add_counter_trigger
    """

    table_name = models.CharField(
        max_length=255,
        default=Key._meta.db_table,
        primary_key=True
    )
    new_keys = models.PositiveIntegerField(
        verbose_name='Счётчик новых не выданных ключей',
        default=0
    )

    class Meta:
        verbose_name = 'Счётчик новых не выданных ключей'

    def __str__(self):
        return '{0} has {1} new keys'.format(
            self.table_name,
            self.new_keys
        )

