from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# !Crear los modelos aqui

# * Categorias
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre

# * Productos (Madre)
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.FloatField()
    descripcion = models.TextField(blank=True, null=True)
    ofertas = GenericRelation('Oferta', related_query_name='producto')
    imagenes = GenericRelation('imagenProducto', related_query_name='producto')
    inventario = GenericRelation('Inventario', related_query_name='producto')

    @property
    def precio_actual(self):
        # Busca la oferta activa más reciente.
        oferta_activa = self.ofertas.filter(fecha_inicio__lte=timezone.now(), fecha_fin__gte=timezone.now()).first()
        if oferta_activa:
            return oferta_activa.precio_oferta
        return self.precio

    class Meta: 
        abstract = True 
    
    def __str__(self):
        return self.nombre
    
# * Paneles SiP
class PanelSIP(Producto):
    tipo_obs = models.CharField(max_length=100, blank=True,null=True)
    madera_union = models.CharField(max_length=100, blank=True,null=True)
    espesor = models.DecimalField(max_digits=5, decimal_places=2)  # ! cm o mm?
    largo = models.DecimalField(max_digits=7, decimal_places=2)  
    ancho = models.DecimalField(max_digits=5, decimal_places=2)
    categorias =models.ManyToManyField(Categoria, related_name="paneles", blank=True)  

# * Kits de autoconstruccion
class KitConstruccion(Producto):
    m2 = models.DecimalField(max_digits=8, decimal_places=2)
    dormitorios = models.PositiveIntegerField(default=0)
    banos = models.PositiveIntegerField(default=0)
    categorias =models.ManyToManyField(Categoria, related_name="kits", blank=True)
    
# * Imagen 
def ruta_imagen(instance, filename):
    parent_type = instance.content_type.model
    if parent_type == 'kitconstruccion': # !si la imagen es de un kit 
        return f"kit/{filename}"
    elif parent_type == 'panelsip': # !si la imagen es de un panel
        return f"panel/{filename}"
    else: #! fallback por si no pertenece a ninguno
        return f"otros{filename}"

class imagenProducto(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('content_type', 'object_id')
    imagen = models.ImageField(upload_to=ruta_imagen) #Guardar la imagen en carpeta correspondiente

    def clean(self):
        """Validar que el archivo subido sea realmente una imagen."""
        if self.imagen:
            # Verificar tipo MIME
            if not self.imagen.file.content_type.startswith('image/'):
                raise ValidationError("Solo puedes subir archivos de imagen (jpg, png, etc).")

            # Validar tamaño máximo (opcional, ej: 5 MB)
            if self.imagen.size > 5 * 1024 * 1024:
                raise ValidationError("La imagen no puede superar los 5 MB.")
            
    def __str__(self):
        return f"Imagen de {self.producto}"

#*Inventario
class Inventario(models.Model):
    TIPO_STOCK = [
        ('stock', 'Con stock'),
        ('pedido', 'Por pedido'),
    ]
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('content_type', 'object_id')

    disponible = models.PositiveIntegerField(default=0)
    reservado = models.PositiveIntegerField(default=0)
    modo_stock = models.CharField(max_length=20, choices=TIPO_STOCK, default='pedido')

    def ajustar_reservado(self, nuevo_reservado):
        self.reservado = nuevo_reservado
        self.save(update_fields=['reservado'])

    @property
    def stock_real_disponible(self):
        """Disponible real restando lo reservado."""
        return max(self.disponible - self.reservado, 0)

    def __str__(self):
        return f"Inventario de {self.producto} - Disponible: {self.disponible} / Reservado: {self.reservado}"

#*Ofertas
class Oferta(models.Model):
    # !GenericForeignKey para apuntar a cualquier modelo de producto concreto
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('content_type', 'object_id')
    precio_oferta = models.FloatField()
    porcentaje_dcto = models.PositiveIntegerField(null=True,blank=True)
    fecha_inicio = models.DateTimeField(null=True,blank=True)
    fecha_fin =models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"Oferta de {self.producto.nombre}"

# *Comentarios
class Comentario(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('content_type', 'object_id')
    autor =  models.CharField(max_length=200,null=True,blank=True)
    texto = models.TextField()
    fecha_comentario = models.TimeField(auto_now_add=True)
    estrellas = models.DecimalField( max_digits=3,decimal_places=1, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    def __str__(self):
        return f"Comentario de {self.autor} en {self.producto.nombre}"
    
class Resena(models.Model):
    autor = models.CharField(max_length=200, null=True, blank=True)
    texto = models.TextField()
    fecha_comentario = models.DateTimeField(default=timezone.now)
    revisado = models.BooleanField(default=False)  # Nuevo campo

    def __str__(self):
        return f"{self.autor} - {self.texto[:30]}"




