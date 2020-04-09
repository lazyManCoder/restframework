渲染模块
首先要注册 rest_framework
浏览器和postman渲染的形式不一样
self.response = self.finalize_response(request, response, *args, **kwargs)

 def finalize_response(self, request, response, *args, **kwargs):
	"""
	Returns the final response object.
	"""
	# Make the error obvious if a proper response is not returned
	assert isinstance(response, HttpResponseBase), (
		'Expected a `Response`, `HttpResponse` or `HttpStreamingResponse` '
		'to be returned from the view, but received a `%s`'
		% type(response)
	)

	if isinstance(response, Response):
		if not getattr(request, 'accepted_renderer', None):
			neg = self.perform_content_negotiation(request, force=True)
			#解压分值
			request.accepted_renderer, request.accepted_media_type = neg

		response.accepted_renderer = request.accepted_renderer
		response.accepted_media_type = request.accepted_media_type
		response.renderer_context = self.get_renderer_context()

	# Add new vary headers to the response instead of overwriting.
	vary_headers = self.headers.pop('Vary', None)
	if vary_headers is not None:
		patch_vary_headers(response, cc_delim_re.split(vary_headers))

	for key, value in self.headers.items():
		response[key] = value

	return response
	
	
neg = self.perform_content_negotiation(request, force=True)	
def perform_content_negotiation(self, request, force=False):
	"""
	Determine which renderer and media type to use render the response.
	"""
	#获取渲染类
	renderers = self.get_renderers()
	conneg = self.get_content_negotiator()

	try:
		return conneg.select_renderer(request, renderers, self.format_kwarg)
	except Exception:
		if force:
			return (renderers[0], renderers[0].media_type)
		raise

self.get_renderers()	
def get_renderers(self):
	"""
	Instantiates and returns the list of renderers that this view can use.
	"""
	#self.renderer_classes  == views.render_classes  优先找类对象中的属性方法
	return [renderer() for renderer in self.renderer_classes]


drf提供的渲染类
'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    ],
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	