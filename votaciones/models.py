from django.db import models
from datetime  import *
from django.db import IntegrityError
from django.utils.safestring import mark_safe


ETAPAS = (
  ('0','CERRADO'),
  ('1','NOMINANDO'),
  ('2','FILTRANDO'),
  ('3','VOTANDO'),
)

TIPO_CATEGORIA = (
  ('0','COMPUTISTA'),
  ('1','PROFESOR'),
  ('2','AGRUPACION'),
  ('3','OTRO'),
)


class Media(models.Model):
     def __unicode__(self):
        return str(self.pk)


class Foto(models.Model):
    imagen      = models.ImageField(upload_to = "media_subida/")
    descripcion = models.CharField(max_length=256)
    media       = models.ForeignKey(Media)

    def delete(self, *args, **kwargs):
        self.imagen.delete(save=False)
        super(Foto, self).delete(*args, **kwargs)

    def vista_previa(self):
        return mark_safe("""<img src="%s" height="128" />""" % self.imagen.url)
    vista_previa.short_description = 'Vista previa'

    def __unicode__(self):
        return str(self.imagen.name)

    class Meta:
        unique_together = ("imagen", "media")

class Video(models.Model):
    link        = models.CharField(max_length=100, primary_key = True)
    descripcion = models.CharField(max_length=256)
    media       = models.ForeignKey(Media)

    def vista_previa(self):
        return mark_safe("""<iframe width="200" height="128" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>""" % self.link)
    vista_previa.short_description = 'Vista previa'

    def __unicode__(self):
        return str(self.link)

    class Meta:
        unique_together = ("link", "media")


class Edicion(models.Model):
    ano    = models.IntegerField(primary_key = True)
    media  = models.OneToOneField(Media)
    activa = models.BooleanField()
    etapa  = models.CharField(max_length=1,choices=ETAPAS)

    def save(self, *args, **kwargs):
        try:
            super(Edicion, self).save(*args, **kwargs)
        except IntegrityError:
            media = Media()
            media.save()
            self.media = mediaVotoFinal
            super(Edicion, self).save()


    def __unicode__(self):
        return str(self.ano)

    @staticmethod
    def actual():
        return Edicion.objects.get_or_create(ano=datetime.now().year)[0]


class Nominacion(models.Model):
    categoria = models.ForeignKey('Categoria')
    foto_id   = models.ForeignKey(Foto, null=True, blank=True)

    def nominaciones(self):
        return self.votonominacion_set.count()

    def nominados(self):
        return ', '.join(map(lambda x: x[0], self.nominado_set.values_list('nombre')))

    def fotos(self):
        return Foto.objects.filter(media__in = self.votonominacion_set.values_list('media'))

    def videos(self):
        return Video.objects.filter(media__in = self.votonominacion_set.values_list('media'))

    def __unicode__(self):
        return self.nominados()+' | '+str(self.categoria)

    class Meta:
        ordering = ['categoria']


class Nominado(models.Model):
    nombre     = models.CharField(max_length=128)
    nominacion = models.ForeignKey(Nominacion)

    class Meta:
        ordering = ['nombre']


class Categoria(models.Model):
    nombre    = models.CharField(max_length=32)
    edicion   = models.ForeignKey(Edicion)
    ganador   = models.ForeignKey(Nominado, null=True, blank=True)
    descripcion      = models.CharField(max_length=128)
    maximo_nominados = models.IntegerField()
    minimo_nominados = models.IntegerField()
    tipo_categoria = models.CharField(max_length=1,choices=TIPO_CATEGORIA)

    def __unicode__(self):
        return self.nombre+' '+str(self.edicion)

    class Meta:
        unique_together = ("nombre", "edicion")
        ordering = ['edicion']


#Nominacion.categoria = models.ForeignKey(Categoria)


class Voto(models.Model):
    user_id = models.IntegerField()
    fecha   = models.DateField(auto_now = True)

    class Meta:
        abstract = True


class VotoNominacion(Voto):
    nominacion = models.ForeignKey(Nominacion)
    media      = models.ForeignKey(Media)

    def save(self, *args, **kwargs):
        try:
            super(VotoNominacion, self).save(*args, **kwargs)
        except IntegrityError:
            media = Media()
            media.save()
            self.media = media
            super(VotoNominacion, self).save()

    def delete(self, *args, **kwargs):
        self.media.delete()
        super(VotoNominacion, self).delete(*args, **kwargs)

    class Meta:
        unique_together = ("nominacion", "user_id")
        ordering = ['fecha', 'nominacion']


class VotoFinal(Voto):
    nominacion = models.ForeignKey(Nominacion)

    class Meta:
        #Cambiar por ("nominacion__categoria", "user_id")
        unique_together = ("nominacion", "user_id")
        ordering = ['fecha', 'nominacion']

class Carnet(models.Model):
    numero        = models.CharField(max_length = 12 , primary_key = True)
    nombre        = models.CharField(max_length = 64)
    usado         = models.BooleanField()
    tipo_carnet   = models.CharField(max_length=1, default='0',choices=TIPO_CATEGORIA)
    #es_estudiante = models.BooleanField(default=True)

    class Meta:
        ordering = ['numero', 'usado']