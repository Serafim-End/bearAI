# coding: utf-8
from django.db import DataError

from base_storage_adapter import BaseStorageAdapter


class StorageAdapter(BaseStorageAdapter):
    """
    there django class can be used as models
    """

    def save(self, cls, **kwargs):
        cls = self.get_class(cls)

        instance = cls(**kwargs)
        try:
            if instance.is_valid():
                return instance.save()
        except DataError:
            pass  # Запись слишком длинная.

        raise BaseStorageAdapter.SerializerException(
            msg='Instance was not saved'
        )
