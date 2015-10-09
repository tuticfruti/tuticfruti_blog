from django.conf import settings


def ckeditor(request):
    return {'CKE_CODESNIPPET_THEME': settings.CKEDITOR_CONFIGS.get('default').get('codeSnippet_theme')}
