from django.contrib import admin

from users.models import User

from products.admin import BasketsAdmin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	inlines = (BasketsAdmin,)