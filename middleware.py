import traceback
from datetime import datetime

from django.conf import settings

from .models import RequestPerformanceLog, Config
from .config import DEFAULT_THRESHOLD, DEFAULT_DUPLICATE_RECORD
from .triggers import ErrorTrigger, LogTrigger


class PerformanceMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = datetime.now()
        response = self.get_response(request)
        end = datetime.now()
        data = dict()
        try:
            time_consume = int((end - start).microseconds / 1000)
            threshold = getattr(settings, "THRESHOLD", DEFAULT_THRESHOLD)
            duplicate_record = getattr(settings, "DUPLICATE_RECORD", DEFAULT_DUPLICATE_RECORD)
            expression_res = time_consume > threshold and Config.is_enabled()
            if expression_res:
                data = {
                    "time_consume": time_consume,
                    "threshold": threshold,
                    "updated_at": start,
                    "method": request.method,
                    "path": request.path
                }
                if duplicate_record:
                    RequestPerformanceLog.objects.create(**data)
                else:
                    qs = RequestPerformanceLog.objects.filter(method=request.method, path=request.path)
                    if qs.exists():
                        # to trigger model save()
                        obj = qs.first()
                        if obj.threshold != threshold:
                            data["hit_num"] = 0
                        obj.__dict__.update(**data)
                        obj.save()
                    else:
                        RequestPerformanceLog.objects.create(**data)
        except:
            ErrorTrigger.use(traceback.format_exc())
        else:
            if expression_res:
                LogTrigger.use(data)
        finally:
            return response
