from django.contrib import admin

# Register your models here.
from energy.models import Consumer, \
    ConsumerType, Meter, \
    OrumType, Orum, OrumDateUse, Period, \
    ProductionArea, PowerGridRegion, Point, \
    NetworkOrganization, ProductionDepartment, MeterOrum, \
    OrumSetting, OrumCorrection, MeterPassport, \
    MeterReading, MeterCorrection, MeterReadingEvent

class ChoiceOrumValue(admin.StackedInline):
    model = OrumDateUse
    extra = 0

class ChoiceOrumCorrection(admin.StackedInline):
    model = OrumCorrection
    extra = 0

class ChoiceOrumSetting(admin.StackedInline):
    model = OrumSetting
    extra = 0

class OrumAdmin(admin.ModelAdmin):
    inlines = [ChoiceOrumSetting, ChoiceOrumCorrection, ChoiceOrumValue]
    # list_display = ['__str__', 'value']

class PointAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']

class MeterPassportAdmin(admin.ModelAdmin):
    list_filter = ('active', 'check')

class MeterReadingEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority']

admin.site.register(Orum, OrumAdmin)

admin.site.register(Consumer)
admin.site.register(ConsumerType)
# admin.site.register(Orum)
admin.site.register(OrumType)
# admin.site.register(OrumDateUse)
admin.site.register(Meter)
admin.site.register(Period)
admin.site.register(ProductionArea)
admin.site.register(PowerGridRegion)
admin.site.register(Point, PointAdmin)
admin.site.register(NetworkOrganization)
admin.site.register(ProductionDepartment)
admin.site.register(MeterOrum)
admin.site.register(MeterPassport, MeterPassportAdmin)
admin.site.register(MeterReading)
admin.site.register(MeterReadingEvent, MeterReadingEventAdmin)
admin.site.register(MeterCorrection)
