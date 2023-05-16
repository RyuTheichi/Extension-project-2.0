import json
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from cliente.models import MenuItem, OrderModel , Categoria



class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cliente/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cliente/about.html')

         
         #Obtem os itens do menu de cada categoria especifica  atraves do metodo get e depois e renderizada na area do admin
class Order(View):
    def get(self, request, *args, **kwargs):
        # pegar cada item de uma categoria
        hamburgers = MenuItem.objects.filter(categoria__nome__contains='Hamburgers')
        acompanhamentos = MenuItem.objects.filter(categoria__nome__contains='Acompanhamentos')
        adicionais = MenuItem.objects.filter(categoria__nome__contains='Adicionais')
        bebidas = MenuItem.objects.filter(categoria__nome__contains='Bebidas')

        # Insercao de valores a chaves, ex : no caso a chave hamburgers esta associada com a variavel hamburger
        context = {
            'hamburgers': hamburgers,
            'acompanhamentos': acompanhamentos,
            'adicionais': adicionais,
            'bebidas': bebidas,
        }

        # rendererizar o template
        return render(request, 'cliente/order.html', context)
    
    #Extrai os inputs dos formularios que estao em order.html

    def post(self, request, *args, **kwargs):
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        complemento = request.POST.get('complemento')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'nome': menu_item.nome,
                'preco': menu_item.preco,
            }

            order_items['items'].append(item_data)
        ##Calculo do preco total dos pedidos
            preco = 0
            item_ids = []

        for item in order_items['items']:
            preco += item['preco']
            item_ids.append(item['id'])

       
        order = OrderModel.objects.create(preco=preco,
                                          nome=nome,
                                          email=email,
                                          telefone=telefone,
                                          rua=rua,
                                          bairro=bairro,
                                          complemento=complemento)
        order.items.add(*item_ids)
        #Enviar e-mail de confirmação após tudo estiver pronto
        body = 'Seu pedido está sendo preparado e logo estará a caminho\n' \
        f'Total da compra: {preco}\n' \
        'Obrigado por escolher nosso estabelecimento!'
        send_mail(
            'Pedido confirmado',
            body,
            'insiraoemailaqui@exemplo.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'preco': preco
        }
        return redirect('order-confirmation', pk=order.pk)



class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        
        context = {
            'pk': order.pk,
            'items': order.items,
            'preco': order.preco,
        }
        return render(request, 'cliente/order_confirmation.html', context)
    def post(self,request,pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['pago']:
            order = OrderModel.objects.get(pk=pk)
            order.pago = True
            order.save()
        return redirect('payment-confirmation')

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request,'cliente/order_pay_confirmation.html')
