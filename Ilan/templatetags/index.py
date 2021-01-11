from django import template
register = template.Library()

#Html üzerinde indise göre işlem yapmak için yazılmış bir fonksiyon
@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter()
def range(x):
    return range(x)