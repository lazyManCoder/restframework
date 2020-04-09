# author navigator


from rest_framework.views import Response,exception_handler as drf_exception
from rest_framework.views import status
def exception_handler(exc,context):
    response = drf_exception(exc,context)
    print(exc,context)
    if response is None:
        return Response({
            'detail':'服务器错误'
        },status=500)
    return response