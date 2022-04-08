from django.db import models
from functools import lru_cache


class RequestPerformanceLog(models.Model):
    path = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    method = models.CharField(max_length=24)
    time_consume = models.IntegerField()
    threshold = models.IntegerField()
    hit_num = models.IntegerField(default=0)
    alerted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.method} on the path {self.path} takes {self.time_consume}'

    def save(self, *args, **kwargs):
        self.hit_num += 1
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        index_together = ["path", "method"]


class Config(models.Model):
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.is_active:
            return "active"
        return "inactive"

    def save(self, *args, **kwargs):
        is_already_exists = Config.objects.exists()
        if not is_already_exists or self.id:
            Config.is_enabled.cache_clear()
            super().save(args, **kwargs)

    @staticmethod
    @lru_cache(1)
    def is_enabled():
        config_obj = Config.objects.first()
        if not config_obj:
            return True
        return config_obj.is_active
