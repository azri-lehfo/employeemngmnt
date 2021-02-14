from django.conf import settings as local_settings


def settings(request):
    return {'settings': local_settings}
