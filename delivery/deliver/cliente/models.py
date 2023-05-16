from django.db import models

class MenuItem(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='menu_images/')
    preco = models.DecimalField(max_digits=5, decimal_places=2) 
    categoria = models.ManyToManyField('Categoria', related_name='item')

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    preco = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem' , related_name='orders', blank=True)
    nome = models.CharField(max_length=50, blank=True)
    email =models.CharField(max_length=50, blank=True)
    rua = models.CharField(max_length=50, blank=True)
    bairro = models.CharField(max_length=50, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    telefone = models.IntegerField(blank=True, null=True)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I:%M %p")}'
