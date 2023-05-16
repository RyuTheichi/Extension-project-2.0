from django.contrib import admin
from .models import MenuItem, Categoria , OrderModel
# Registro dos modelos criados em model.py para gerenciar esses modelos
admin.site.register(MenuItem)
admin.site.register(Categoria)
admin.site.register(OrderModel)

