# author navigator
from rest_framework.views import exception_handler as drf_excepion_handler
from rest_framework.views import Response
def exception_handler(exc, context):
	response = drf_excepion_handler(exc,context)
	if response is None:
		ret = "%s-%s-%s"%(context["view"],context["request"].method,exc)
		print(ret)
		return Response({  #通过context exc记录详细的异常
			'detail':ret
			})
	return response