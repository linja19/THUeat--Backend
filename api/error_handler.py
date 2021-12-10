from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # ovverride IsAuthenticated permission class exception
    if (response.data['detail'].code == 'not_authenticated'):
        response.data['code'] = 400
        response.data['message'] = "口令有误"
        del response.data['detail']
    elif (response.data['detail'].code == 'authentication_failed'):
        response.data['code'] = 400
        response.data['message'] = "口令有误"
        del response.data['detail']
    elif (response.data['detail'].code == 'permission_denied'):
        response.data['code'] = 400
        response.data['message'] = "没有权限"
        del response.data['detail']

    return response