from django.contrib import admin

from .models import Fiction, Quote, Type, Pokemon


class FictionSiteAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name", "category")
    ordering = ("name",)


class QuoteSiteAdmin(admin.ModelAdmin):
    list_display = ("quote", "fiction")
    list_filter = ("fiction",)
    search_fields = ("quote", "fiction")
    ordering = ("fiction",)


class TypeSiteAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)


class PokemonSiteAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "primaryType", "secondaryType")
    list_filter = ("primaryType", "secondaryType")
    search_fields = ("number", "name")
    ordering = ("number",)


admin.site.register(Fiction, FictionSiteAdmin)
admin.site.register(Quote, QuoteSiteAdmin)
admin.site.register(Type, TypeSiteAdmin)
admin.site.register(Pokemon, PokemonSiteAdmin)