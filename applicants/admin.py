from django.contrib import admin
from .models import Applicant

# Register your models here.

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'years_of_exp', 'phone_number', 'email', 'current_salary', 'expected_salary', 'status')
    list_filter = ('status', 'gender', 'years_of_exp')
    search_fields = ('name', 'email', 'phone_number')
    list_editable = ('status',)
    list_per_page = 25

admin.site.register(Applicant, ApplicantAdmin)
