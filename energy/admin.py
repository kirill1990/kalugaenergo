from django.contrib import admin

# Register your models here.
from energy.models import Consumer, \
    Meter, \
    OrumType, Orum, OrumDateUse, Period, \
    ProductionArea, Point, \
    PointMeter, \
    OrumSetting, OrumCorrection, MeterPassport, \
    MeterReading, MeterCorrection, MeterReadingEvent, \
    Transformer, Wire

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
    list_display = ['title', 'value']
    search_fields = ['number_in_t2']

class ProductionAreaAdmin(admin.ModelAdmin):
    list_display = ['title', 'current_period']


class ChoicePoint(admin.StackedInline):
    model = Point
    extra = 0

class ConsumerAdmin(admin.ModelAdmin):
    inlines = [ChoicePoint]

class MeterPassportAdmin(admin.ModelAdmin):
    list_filter = ('check', 'active')
    search_fields = ['title', 'pk']

class MeterReadingEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority']

admin.site.register(Orum, OrumAdmin)

admin.site.register(Consumer, ConsumerAdmin)
admin.site.register(Transformer)
admin.site.register(Wire)
# admin.site.register(Orum)
admin.site.register(OrumType)
# admin.site.register(OrumDateUse)
admin.site.register(Meter)
admin.site.register(Period)
admin.site.register(ProductionArea, ProductionAreaAdmin)
admin.site.register(Point, PointAdmin)
admin.site.register(PointMeter)
admin.site.register(MeterPassport, MeterPassportAdmin)
admin.site.register(MeterReading)
admin.site.register(MeterReadingEvent, MeterReadingEventAdmin)
admin.site.register(MeterCorrection)
