from django.contrib import admin


from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from energy.models import CustomUser

# Register your models here.
from energy.models import Legal, \
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

class EntityAdmin(admin.ModelAdmin):
    inlines = []

class MeterPassportAdmin(admin.ModelAdmin):
    list_filter = ('check', 'active')
    search_fields = ['title', 'pk']

class MeterReadingEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority']

admin.site.register(Orum, OrumAdmin)

admin.site.register(Legal, EntityAdmin)
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


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'password',
            'subdivision',
            'title',
            'is_active',
            'is_admin',
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'get_full_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('subdivision', 'title')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'subdivision', 'title',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)