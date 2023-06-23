from django import template
from store.models import Category, FavoriteProducts

register = template.Library()


@register.simple_tag()
def get_subcategories(category):
    return Category.objects.filter(parent=category)


@register.simple_tag()
def get_categories():
    return Category.objects.filter(parent=None)


@register.simple_tag()
def get_sorted():
    sorters = [
        {
            'title': 'By price',
            'sorters': [
                ('price', 'Ascending'),
                ('-price', 'Descending')
            ],
        },
        {
            'title': 'By color',
            'sorters': [
                ('color', 'A to Z'),
                ('-color', 'Z to A')
            ]
        },
        {
            'title': 'By size',
            'sorters': [
                ('size', 'Ascending'),
                ('-size', 'Descending')
            ]
        }
    ]
    return sorters


@register.simple_tag()
def get_favorite_products(user):
    fav = FavoriteProducts.objects.filter(user=user)
    products = [i.product for i in fav]
    return products
