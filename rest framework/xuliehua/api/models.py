from django.db import models

# Create your models here.
class User(models.Model):
    SEX = (
        (1,'男'),
        (2,'女'),
    )
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    sex = models.IntegerField(choices=SEX)
    icon = models.ImageField(upload_to='icon',default='icon/2.jpg')

    class Meta:
        db_table = 'usersex'
        verbose_name = '信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<<%s>>' % self.name

#基表
class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    #z作为基表models不能在数据库中形成对应的表，设置 abstract = True
    #因为每个人都想先创建一个，因为设置成抽象的，就不需要再次创建了
    class Meta:
        abstract = True

class Book(BaseModel):
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    img = models.ImageField(upload_to='icon',default='img/2.jpg')
    public = models.ForeignKey(
            to="Publish",
            db_constraint=False,
            related_name='books',
            on_delete=models.DO_NOTHING,
    )
    authors = models.ManyToManyField(
            "Author",
            db_constraint=False,
            related_name='books'
    )

    @property
    def author_list(self):
        return self.authors.values('name','age','detail__mobile')

    @property
    def fn(self):
        return 'hello'

    class Meta:
        db_table = 'book'
        verbose_name = '书籍'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Publish(BaseModel):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
    class Meta:
        db_table = 'publish'
        verbose_name = '出版社'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Author(BaseModel):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    class Meta:
        db_table = 'author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class AuthorDetail(BaseModel):
    mobile = models.CharField(max_length=32)
    author = models.OneToOneField(
            to='Author',
            db_constraint=False,
            related_name="detail" , #反向找名字
            default = 0 ,
            on_delete = models.SET_DEFAULT
    )
    class Meta:
        db_table = 'authot_detail'
        verbose_name = '作者详情'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.author.name