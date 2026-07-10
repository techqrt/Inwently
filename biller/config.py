from decouple import config
 
class Configurations:
    pagination_count = 20
    search_count = 10
    secret_key = config('SECRET_KEY')
    debug = False if config('DEBUG') == 'False' else True
    environment = config('ENVIRONMENT')
    kafka = {'enable': config('KAFKA_ENABLE', default=False, cast=bool), 'url': config('KAFKA_URL', default=None)}
    email_service_enable = config('EMAIL_SERVICE_ENABLE', default=False, cast=bool)
    email_host_user = config('EMAIL_HOST_USER', default=None)
