from django.contrib import admin

from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "percent")
    list_editable = ("percent",)


@admin.register(DetailItem)
class DetailItemAdmin(admin.ModelAdmin):
    list_display = ("category", "content")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "company_name", "featured")
    list_filter = ("featured",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("title", "institution", "year_range")


class Tech_toolsInline(admin.TabularInline):
    model = Tech_tools
    extra = 1

class CustomerInline(admin.TabularInline):
    model = customerServices
    extra = 1

@admin.register(Tech_tools)
class Tech_toolsAdmin(admin.ModelAdmin):    
    list_display = ("name",)  

@admin.register(customerServices)
class customerServicesAdmin(admin.ModelAdmin):   
    list_display = ("name", "icon", "details", "customer_services")
    


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "featured")
    list_filter = ("featured",)
    inlines = [Tech_toolsInline, CustomerInline]


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "year")
    list_filter = ("category",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    ordering = ("-created_at",)

