# Django实战之自定义分页



首先看下效果图

为什么分页：

数据库中的数据有很多，如果一起展示，会造成不美观，如果数据量很大也可以造成数据库查询缓慢，这里主要是前端显示，优化的数据库暂且放置

需求：

- 将数据库中的数据放置在页面上，每页放置6条数据（自定义），右下角的页码一直保持11个（1-11），当然小于11也做出了判断。



思路：

- 1.查看数据库中的数量，可以通过 `models.Content.objects.all().count()`先看下数据中的文章数量。
- 2.在后端中通过 `mark_safe` 的验证方式将前端的代码提交到前端，



分批次进行

将数据库中的对象保存到LIST列表中，为后面切片做准备

```
LIST = []
all = models.Content.objects.all()  #所有的对象
for i in all:
    LIST.append(i)
```

页码与数据进行匹配（获取当前页）

```
current_page = request.GET.get('p',1) #第一次执行，不能获取href中页码值，故默认为1
current_page = int(current_page)

start = (current_page-1) * 10
end = current_page *10
data = LIST[start:end]  #进行切片 一页只能显示数据库中的10条数据
all_count = len(LIST)
count,y = divmod(all_count,data)   #divmod 可以求出除数（页数） 余数（剩下不够一页的数据）
if y:
	count += 1
	
page_str = []
for i in range(1,count+1):
	if i == current_page:		# 如果是当前页，设置active样式
		temp = "<a class="active" href="/user_list/?p=%s">%s</a>"%(i,i) #添加样式
	else:
		temp = "<a href="/user_list/?p=%s">%s</a>"%(i,i)
	page_list.append(temp)

from django.utils.safestring import mark_safe

page_str = "".join(page_list)  #变成字符串
page_str = mark_safe(page_str) #为了防止有人恶意像网站中写入js代码（XSS过滤)
```

继续改进

如果我们的数据十分多，这时候页码就会占用我们很多空间这是我们不希望看到的所以，对页码的数量要进行判断

```
page_num = 11
if self.all_count < page_num:
   start_index = 1
   end_index = self.all_count + 1
else:
   if self.current_page <= (page_num+1)/2:
      start_index = 1
      end_index = page_num + 1
   else:
      start_index = self.current_page - (page_num-1)/2
      end_index = self.current_page + (page_num+1)/2
      if self.current_page + (page_num-1)/2 > self.all_count:
         end_index = self.all_count + 1
         start_index = self.all_count - page_num + 1
  
  #这样我们就可以设置页码是固定的长度，而且不会出现超出这个范围的页码
  for i in range(1,count+1):
  for i in range(start_index,end_index)
```

再加上上一页、下一页的效果

```
if self.current_page == 1: #在第一页的时候就不要执行上一页的操作
   prev = """<li >
               <a href="javascript:void(0);" aria-label="Previous">
                  <span aria-hidden="true">&laquo;</span>
               </a>
              </li>"""
else:
   prev = """<li >
                <a href="%s?p=%s" aria-label="Previous">
                   <span aria-hidden="true">&laquo;</span>
                </a>
             </li>"""%(base_url,self.current_page-1)
page_str.append(prev)

for i in range(int(start_index), int(end_index)):
   if i == self.current_page:
       temp = '<li class="active"><a href="%s?p=%s">%s</a>' %(base_url,i,i)
    else:
       temp = '<li><a href="%s?p=%s">%s</a>' %(base_url,i,i)
    page_str.append(temp)
    
if self.current_page == self.all_count:
    next = """<li>
            <a href="javascript:void(0);" aria-label="Next">
               <span aria-hidden="true">&raquo;</span>
            </a>
            </li>"""
else:
  next = """<li>
                   <a href="%s?p=%s" aria-label="Next">
                      <span aria-hidden="true">&raquo;</span>
                     </a>
                   </li>"""%(base_url,self.current_page+1)
page_str.append(next)  #要按照顺序去加
```



视图中主要写的是业务代码，而且分页功能不只是在一个页面上应用，所以我们应该将它封装起来

可以在创建一个 `utils`的目录 ，在目录中创建一个 `pagination`(自定义)

下面便是全部的代码

```
# author navigator
from django.utils.safestring import mark_safe
class Page:
    def __init__(self,current_page,data_count,per_page=6,page_num=11):
        self.current_page = current_page
        self.data_count = data_count
        self.per_page = per_page
        self.page_num = page_num

    def start(self):
        return (self.current_page - 1) * self.per_page
        
    def end(self):
        return self.current_page * self.per_page

    @property
    def all_count(self):
        u, y = divmod(self.data_count, self.per_page)
        if y:
            u += 1
        return u


    def page_str(self,base_url):
        page_str = []
        page_num = 11
        if self.all_count < page_num:
            start_index = 1
            end_index = self.all_count + 1
        else:
            if self.current_page <= (page_num+1)/2:
                start_index = 1
                end_index = page_num + 1
            else:
                start_index = self.current_page - (page_num-1)/2
                end_index = self.current_page + (page_num+1)/2
                if self.current_page + (page_num-1)/2 > self.all_count:
                    end_index = self.all_count + 1
                    start_index = self.all_count - page_num + 1
        if self.current_page == 1:
            prev = """<li >
                        <a href="javascript:void(0);" aria-label="Previous">
                            <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>"""
        else:
            prev = """<li >
                        <a href="%s?p=%s" aria-label="Previous">
                            <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>"""%(base_url,self.current_page-1)
        page_str.append(prev)
        for i in range(int(start_index), int(end_index)):
            if i == self.current_page:
                temp = '<li class="active"><a href="%s?p=%s">%s</a>' %(base_url,i,i)
            else:
                temp = '<li><a href="%s?p=%s">%s</a>' %(base_url,i,i)
            page_str.append(temp)
        if self.current_page == self.all_count:
            next = """<li>
                        <a href="javascript:void(0);" aria-label="Next">
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>"""
        else:
            next = """<li>
                        <a href="%s?p=%s" aria-label="Next">
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>"""%(base_url,self.current_page+1)
        page_str.append(next)

        jump = """
            <input id="t1" type="text" /><a onclick='jumpTo(this,"%s?p=");'>GO</a>
        """%(base_url)
        page_str.append(jump)
        page_str = "".join(page_str)
        page_str = mark_safe(page_str)
        return page_str
```



在views.py中的代码

```
def content(request):
		LIST = []
        all = models.Content.objects.all()
        for i in all:
            LIST.append(i)
        current_page = request.GET.get('p',1)
        current_page = int(current_page)
        page_obj = Page(current_page,len(LIST))
        data = LIST[page_obj.start():page_obj.end()]
        return render(request, "content.html", {'content_all': data,'page_str':page_obj.page_str('/home/content.html')})
```





补充

- 在前端也可以进行xss过滤

```
{{ page_str | safe }}
```

- 在模板语言中的include

```
{% for item in li %}
{% include 'li.html' %} #创建一个li.html 中 <li>{{item}}</li>
{% endfor %}
```











