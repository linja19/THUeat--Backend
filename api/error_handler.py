from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # ovverride IsAuthenticated permission class exception
    if (response.data['detail'].code == 'not_authenticated'):
        response.data['code'] = 400
        response.data['message'] = "Token not provided"
        del response.data['detail']

    return response