from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Category name')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Category image')
    slug = models.SlugField(unique=True, null=True)  # nice links for categories, "texnomart" example
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True, blank=True,
                               verbose_name='Category',
                               related_name='subcategories')  # null=True, blank=True if there's no parent of category

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://t4.ftcdn.net/jpg/03/08/68/19/360_F_308681935_VSuCNvhuif2A8JknPiocgGR2Ag7D1ZqN.jpg'
    #  appeal from parent to child (_set)
    #  category.category_set.all() - before related_name
    #  category.subcategories.all() - after related_name

    def __str__(self):
        return self.title

    def __repr__(self):  # allows you to customize the string representation of objects
        return f'Category: pk={self.pk}, title={self.title}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Product name')
    # max_length=255 is the max length of CharField
    price = models.FloatField(verbose_name='Price')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    quantity = models.IntegerField(default=0, verbose_name='In stock')
    description = models.TextField(default='The product description coming soon', verbose_name='Product description')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category', related_name='products')
    slug = models.SlugField(unique=True, null=True)
    size = models.IntegerField(default=30, verbose_name='Size in mm')
    color = models.CharField(max_length=30, default='Silver', verbose_name='Color/Material')

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return 'https://t4.ftcdn.net/jpg/03/08/68/19/360_F_308681935_VSuCNvhuif2A8JknPiocgGR2Ag7D1ZqN.jpg'
        else:
            return 'https://t4.ftcdn.net/jpg/03/08/68/19/360_F_308681935_VSuCNvhuif2A8JknPiocgGR2Ag7D1ZqN.jpg'

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Product: pk={self.pk}, title={self.title}, price={self.price}'


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Image')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Gallery of goods'


class Review(models.Model):
    text = models.TextField(verbose_name='Review text')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username


class FavoriteProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Favorite product')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Favorite product'
        verbose_name_plural = 'Favorite products'


class Mail(models.Model):
    mail = models.EmailField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=255, default='', verbose_name='Name')
    last_name = models.CharField(max_length=255, default='', verbose_name='Surname')

    def __str__(self):
        return self.first_name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    shipping = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk) + ' '

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        # parent knows his child (_set) by the name of model "orderproduct"
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product in order'
        verbose_name_plural = 'Products in order'

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    state = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Shipping address'
        verbose_name_plural = 'Shipping addresses'


class City(models.Model):
    city_name = models.CharField(max_length=255, verbose_name='City name')

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
