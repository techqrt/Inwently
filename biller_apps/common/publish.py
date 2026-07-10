from rest_framework.request import Request

from biller.config import Configurations
from biller_apps.status.models import Status


class Publish:
    @staticmethod
    def status_update(func):
        def check(*args, **kwargs):
            if Configurations.kafka['enable']:
                request: Request = args[0]
                uuid = request.uuid
                status_model = Status()
                status_model.uuid = uuid
                status_model.status = 'In_progress'
                status_model.progress = 0
                status_model.save()
                try:
                    result = func(*args, **kwargs)

                    status_model = Status.objects.get(status_id=status_model.status_id)
                    status_model.uuid = uuid
                    status_model.status = 'successful'
                    status_model.progress = 100
                    status_model.save()
                    return result
                except:
                    status_model = Status.objects.get(status_id=status_model.status_id)
                    status_model.uuid = uuid
                    status_model.status = 'failed'
                    status_model.progress = 0
                    status_model.save()
                    return False

            return func(*args, **kwargs)

        return check
