from django.contrib import admin
from .models import Staff, StaffListPosition, Direction, Sertificate
from .models import Project, Stage, Role

# Register your models here.
admin.site.register(Staff)
admin.site.register(StaffListPosition)
admin.site.register(Direction)
admin.site.register(Sertificate)
admin.site.register(Project)
admin.site.register(Stage)
admin.site.register(Role)

