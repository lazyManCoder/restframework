# Django的模板语言中的Simple_tag和filter

## Simple_tag

初识方法

```python
{{time | date:"Y-m-d H:i:s"}}    #将日期以年月日时分秒的形式显示
{{name | truncatewords:"10" }}   #截取前10个字符
{{name | first | upper}}		 #第一个字大写
{{name | lower}}                 #全部小写
```

通过管道符连接后面的方法，我们就可以在前端展示我们想要的数据

当然了上面方面都是固定用法，在开发中我们通常会自定义这些函数。

- 首先在我们所注册的app下创建一个名字为 `templatetags` 的目录，不可更改名字

- 在目录中可以任意定义 py 文件名了（例如：demo.py)，打个样

```
from django import template
from django.utils.safestring import mark_safe
register = template.Library()
@register.simple_tag

#下面就可以写自定义的函数喽
def test():
	return “hello” 

#在函数中可以接受参数
```

- 怎样可以在模板中实现这个玩意呢

```
{% load demo %}
{% test %}   #{% test 2 2 %} 传参 可以传递多个参数，不在意空格
```

OK了，这样就以在前端显示  hello 了

以上便是创建出Simple_tag的自定义及实现的流程



## filter

和Simple_tag的创建方法一致不同的是装饰器不同

```
from django import template
from django.utils.safestring import mark_safe
register = template.Library()
@register.filter

def addstr(t1,t2):
	return t1 + t2
```

在前端显示

```
{% load demo %}
{% name | addstr:":hello" %}
```

- 这个规定比较上文较为严格，空格不能随意添加
- 参数只能有两个，但是它可以作为模板语言中的 `if`判断的条件





总结：两种方法都是为了可以使数据更加清晰的展现在前端，可以通过实际进行筛选不同的方法。