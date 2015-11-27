from django.contrib import admin

# Register your models here.
from energy.models import Consumer, \
    ConsumerType, Meter, \
    OrumType, Orum, OrumValue, Period, ProductionArea, PowerGridRegion, Point, NetworkOrganization, ProductionDepartment

class ChoiceOrumValue(admin.StackedInline):
    model = OrumValue
    extra = 0

class OrumAdmin(admin.ModelAdmin):
    inlines = [ChoiceOrumValue]

class PointAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']

admin.site.register(Orum, OrumAdmin)

admin.site.register(Consumer)
admin.site.register(ConsumerType)
# admin.site.register(Orum)
admin.site.register(OrumType)
admin.site.register(OrumValue)
admin.site.register(Meter)
admin.site.register(Period)
admin.site.register(ProductionArea)
admin.site.register(PowerGridRegion)
admin.site.register(Point, PointAdmin)
admin.site.register(NetworkOrganization)
admin.site.register(ProductionDepartment)
