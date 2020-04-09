解析模块：
	def initialize_request(self, request, *args, **kwargs):
		"""
		Returns the initial request object.
		"""
		#准备要解析的数据
		parser_context = self.get_parser_context(request)

		return Request(
			request, #原生的
			#获取解析类
			parsers=self.get_parsers(),
			authenticators=self.get_authenticators(), #要先从UserView中查找
			negotiator=self.get_content_negotiator(),
			parser_context=parser_context
		)
		
	获取解析类 parsers = self.get_parsers
	def get_parsers(self):
		"""
		Instantiates and returns the list of parsers that this view can use.
		"""
		return [parser() for parser in self.parser_classes]
		
		
	走到settings.py中的APISettings
	全局解析类配置
	DEFAULT_PARSER_CLASSES': [
		'rest_framework.parsers.JSONParser',
		'rest_framework.parsers.FormParser',
		'rest_framework.parsers.MultiPartParser'
	]


	写在类属性中，就是局部配置
	解析类都在parsers.py 中
	实现了封装的思想，就是解析类中必须要有parse这个方法
	class BaseParser:
		"""
		All parsers should extend `BaseParser`, specifying a `media_type`
		attribute, and overriding the `.parse()` method.
		"""
		media_type = None

		def parse(self, stream, media_type=None, parser_context=None):
			"""
			Given a stream to read from, return the parsed representation.
			Should return parsed data, or a `DataAndFiles` object consisting of the
			parsed data and files.
			"""
			raise NotImplementedError(".parse() must be overridden.")

	class MultiPartParser(BaseParser):
		"""
		Parser for multipart form data, which may include file data.
		"""
		media_type = 'multipart/form-data'

		def parse(self, stream, media_type=None, parser_context=None):
			"""
			Parses the incoming bytestream as a multipart encoded form,
			and returns a DataAndFiles object.

			`.data` will be a `QueryDict` containing all the form parameters.
			`.files` will be a `QueryDict` containing all the form files.
			"""
			parser_context = parser_context or {}
			request = parser_context['request']
			encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
			meta = request.META.copy()
			meta['CONTENT_TYPE'] = media_type
			upload_handlers = request.upload_handlers

			try:
				parser = DjangoMultiPartParser(meta, stream, upload_handlers, encoding)
				data, files = parser.parse()
				return DataAndFiles(data, files)
			except MultiPartParserError as exc:
				raise ParseError('Multipart form parse error - %s' % str(exc))