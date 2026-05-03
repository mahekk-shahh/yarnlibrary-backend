from django.contrib import admin

from api.models import Contact, User, News, Exhibition, Product

# Register your models here.

admin.site.site_header = "Yarn Library Admin"
admin.site.site_title = "Yarn Library Admin Portal"
admin.site.index_title = "Welcome to Yarn Library Admin Portal"
admin.site.register(Contact)
admin.site.register(User)
admin.site.register(News)
admin.site.register(Exhibition)
admin.site.register(Product)
