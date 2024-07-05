from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Workshop,Organization,UserOrganization,LoginWorkshop

admin.site.register(Workshop)
admin.site.register(Organization)
admin.site.register(UserOrganization)
admin.site.register(LoginWorkshop)

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('', {'fields':('role','bio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('', {'fields':('email','role','bio')}),
    )
        
    
