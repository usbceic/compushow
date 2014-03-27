from votaciones.models import *
from django.contrib import admin
from django.db.models import Count

#Media:

class FotoInline(admin.TabularInline):
    fields = ('imagen', 'descripcion', 'vista_previa')
    readonly_fields = ('vista_previa',)

    model = Foto
    extra = 0

class VideoInline(admin.TabularInline):
    fields = ('link', 'descripcion', 'vista_previa')
    readonly_fields = ('vista_previa',)
    model = Video
    extra = 0
      
class MediaAdmin(admin.ModelAdmin):
    search_fields = ['id']
    inlines = [FotoInline, VideoInline]
      
admin.site.register(Media, MediaAdmin)


#Edicion:

class CategoriaInline(admin.TabularInline):
    model = Categoria
    extra = 0

class EdicionAdmin(admin.ModelAdmin):
    list_display = ('fecha',)
    search_fields = ['ano']
    inlines = [CategoriaInline]

    def fecha(self, edi):
        return str(edi.ano)
    fecha.short_description = 'fecha'

admin.site.register(Edicion, EdicionAdmin)



#Categoria:

class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'edicion', 'ganador']
    list_display = ('nombre', 'edicion', 'ganador')
    list_filter  = ['edicion']

admin.site.register(Categoria, CategoriaAdmin)



#Nominacion:

class VotoNominacionInline(admin.TabularInline):
    model = VotoNominacion
    extra = 0

class NominadoInline(admin.TabularInline):
    model = Nominado
    extra = 0

class NominacionAdmin(admin.ModelAdmin):
    list_display = ('nominados', 'nominaciones', 'categoria')
    list_filter  = ['categoria']
    inlines = [NominadoInline, VotoNominacionInline]

    def get_changelist(self, request, **kwargs):
        from django.contrib.admin.views.main import ChangeList
        class SortedChangeList(ChangeList):
            def get_query_set(self, *args, **kwargs):
                qs = super(SortedChangeList, self).get_query_set(*args, **kwargs)
                return qs.annotate(score=Count('votonominacion')).order_by('categoria', '-score')
        if request.GET.get('o'):
            return ChangeList
        else:
            return SortedChangeList


    def nominados(self, nom):
        return ', '.join(map(lambda x: x[0], nom.nominado_set.values_list('nombre')))

    def edicion(self, nom):
        return nom.categoria.edicion.ano


admin.site.register(Nominacion, NominacionAdmin)


#Voto de Nominacion
class NominacionInline(admin.TabularInline):
    model = Nominacion
    extra = 0

class MediaInline(admin.TabularInline):
    model = Media
    extra = 0

class VotoNominacionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'nominacion','fecha')

admin.site.register(VotoNominacion, VotoNominacionAdmin)


#Voto final:
class VotoFinalAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'nominacion','fecha')

admin.site.register(VotoFinal, VotoFinalAdmin)


#Carnet:

class CarnetAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'numero']
    list_display = ('nombre', 'numero', 'usado')
    list_filter  = ['usado']

admin.site.register(Carnet, CarnetAdmin)


