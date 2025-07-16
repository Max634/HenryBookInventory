from django.contrib import admin

from core.models import Book

admin.site.register(Book)

from core.models import Branch
admin.site.register(Branch)
from core.models import Inventory
admin.site.register(Inventory)