from django.shortcuts import render,get_object_or_404
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.models import Group,User
from datetime import date
from django.core.paginator import Paginator,EmptyPage
from .models import Category,MenuItem,Cart,Order,OrderItem
from .serializers import CategorySerializer,MenuItemSerializer,CartSerializer,OrderItemSerializer,OrderSerializer
# Create your views here.

class MenuItemsView(generics.ListCreateAPIView):
    queryset=MenuItem.objects.all()
    serializer_class= MenuItemSerializer
    ordering_fields=['price']
    filterset_fields=['price']
    search_fields = ['title','category__title']
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return []

@api_view(['GET','POST'])
def categories(request):
    if request.method=='GET':
        items=Category.objects.all()
        serialized_item=CategorySerializer(items,many=True)
        return Response(serialized_item.data,status.HTTP_200_OK)
    elif request.method=='POST':
        if request.user.is_superuser:
            serialized_item=CategorySerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.validated_data,status.HTTP_201_CREATED)
        else:
            return Response({'message':"You ar not authorized"},status.HTTP_403_FORBIDDEN)

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def single_category(request,id):
    if request.method=='GET':
        item =get_object_or_404(Category,pk=id)
        serialized_item=CategorySerializer(item)
        return Response(serialized_item.data,status.HTTP_200_OK)
    elif request.method=='PUT':
        if request.user.is_superuser:
            serialized_item=CategorySerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.validated_data,status.HTTP_201_CREATED)
        else:
            return Response({'message':"You ar not authorized"},status.HTTP_403_FORBIDDEN)
    elif request.method=='DELETE':
        if request.user.is_superuser:
            item=get_object_or_404(Category,pk=id)
            item.delete()
            return Response({'message':"category removed"})
        else:
            return Response({'message':"You ar not authorized"},status.HTTP_403_FORBIDDEN)




@api_view(['GET','PUT','DELETE'])
def single_item(request,id):
    if request.method=='GET':
        item =get_object_or_404(MenuItem,pk=id)
        serialized_item=MenuItemSerializer(item)
        return Response(serialized_item.data,status.HTTP_200_OK)
    else:
        if request.user.groups.filter(name='Manager').exists():
            if request.method=='PUT':
                serialized_item=MenuItemSerializer(data=request.data)
                serialized_item.is_valid(raise_exception=True)
                serialized_item.save()
                return Response(serialized_item.validated_data,status.HTTP_201_CREATED)
            elif request.method=='DELETE':
                item=get_object_or_404(MenuItem,pk=id)
                item.delete()
        else:
            return Response({'message':"You ar not authorized"})


@api_view(['POST','DELETE'])
@permission_classes([IsAdminUser])
def managers(request):
    tar_username=request.data['username']
    if tar_username:
        user=get_object_or_404(User,username=tar_username)
        managers = Group.objects.get(name='Manager')
        if request.method=='POST':
            managers.user_set.add(user)
            return Response({'message':"user added to the manager group"})
        elif request.method=='DELETE':
            managers.user_set.remove(user)
            return Response({'message':"user removed to the manager group"})
    return Response({'message':"error"},status.HTTP_400_BAD_REQUEST)



@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    if request.user.groups.filter(name='Manager').exists():
        tar_username=request.data['username']
        if tar_username:
            user=get_object_or_404(User,username=tar_username)
            delivery_crew=Group.objects.get(name='Delivery')
            if request.method=='POST':
                delivery_crew.user_set.add(user)
                return Response({'message':"user added to the delivery crew group"})
            elif request.method=='DELETE':
                delivery_crew.user_set.remove(user)
                return Response({'message':"user removed to the delivery crew group"})
        else:
            return Response({'message':"error"},status.HTTP_400_BAD_REQUEST)
    else:
            return Response({'message':"You ar not authorized"},status.HTTP_403_FORBIDDEN)



@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def single_order(request,id):
    item=get_object_or_404(Order,pk=id)
    if request.method=='GET':
        if item.user == request.user:
            serialized_item= OrderItemSerializer(item)
            return Response(serialized_item.data,status.HTTP_200_OK)
        else:
            return Response({'message':"You ar not authorized"})
    elif request.method=='PATCH':
        if request.user.groups.filter(name='Manager').exists():
            serialized_item= OrderItemSerializer(item,data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.validated_data,status.HTTP_205_RESET_CONTENT)
        elif request.user.groups.filter(name='Delivery').exists():
            status=request.data['status']
            update_data={'status':status}
            serialized_item= OrderItemSerializer(item,data=update_data,partial=True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.validated_data,status.HTTP_205_RESET_CONTENT)
        else:
            return Response({'message':"You ar not authorized"})
    elif request.method=='DELETE':
        if item.user == request.user or request.user.groups.filter(name='Manager').exists():
            item.delete()
        else:
            return Response({'message':"You ar not authorized"})

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def ordering(request):
    if request.method=='GET':
        if request.user.groups.filter(name='Manager').exists():
            items=Order.objects.all()
            tar_price=request.query_params.get('total')
            tar_date=request.query_params.get('date')
            search=request.query_params.get('search')
            ordering=request.query_params.get('ordering')
            perpage=request.query_params.get('perpage',default=2)
            page=request.query_params.get('page',default=1)

            if tar_price:
                items=items.filter(total=tar_price)
            if tar_date:
                items=items.filter(date=tar_date)
            if search:
                items=items.filter(delivery_crew__contains=search)
            if ordering:
                ordering_fields=ordering.split(",")
                for ordering_field in ordering_fields:
                    items= items.order_by(ordering_field)

            paginator=Paginator(items,per_page=perpage)
            try:
                items=paginator.page(number=page)
            except EmptyPage:
                items=[]
            serialized_item=MenuItemSerializer(items,many=True)
            return Response(serialized_item.data)
        else:
            return Response({'message':"You ar not authorized"})
    elif request.method=='POST':
        cart = get_object_or_404(Cart,user=request.user)
        total=0.00
        for i in cart:
            total += i['price']
        order_data={'user':request.user,'status':False,'total':total,'date':date.ctime()}
        serialized_order=OrderSerializer(data= order_data)
        serialized_order.is_valid(raise_exception=True)
        order = serialized_order.save()
        orderitems_data={'order':order,'menuitem':cart['menuitem'],'quantity':cart['quantity'],'unit_price':cart['unit_price'],'price':cart['price']}
        serialized_items=OrderSerializer(data= orderitems_data)
        serialized_items.is_valid(raise_exception=True)
        serialized_items.save()
        cart.delete()
        return Response(serialized_order.validated_data,status.HTTP_201_CREATED)


@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def cart(request):
    if Cart.objects.filter(user=request.user).exists():
        cart= Cart.objects.get(user=request.user)
        if request.method=='GET':
            serialized_items=CartSerializer(cart)
            return Response(serialized_items.data,status.HTTP_200_OK)
        elif request.method=='DELETE':
            cart.delete()
            return Response({'message':"cart is removed"},status.HTTP_204_NO_CONTENT)
        elif request.method=='POST':
            return Response({'message':"you already have one"})
    else:
        if request.method=='POST':
            serialized_item=CartSerializer(data= request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response(serialized_item.validated_data,status.HTTP_201_CREATED)
        else:
            return Response({'message':'there is nothing'},status.HTTP_400_BAD_REQUEST)











# @api_view(['GET','POST'])
# def menu_items(request):
#     if request.method=='GET':
#         items=MenuItem.objects.all()
#         category_name=request.query_params.get('category')
#         tar_price=request.query_params.get('price')
#         search=request.query_params.get('search')
#         ordering=request.query_params.get('ordering')
#         perpage=request.query_params.get('perpage',default=2)
#         page=request.query_params.get('page',default=1)

#         if category_name:
#             items=items.filter(category__title=category_name)
#         if tar_price:
#             items=items.filter(price=tar_price)
#         if search:
#             items=items.filter(title__contains=search)
#         if ordering:
#             ordering_fields=ordering.split(",")
#             for ordering_field in ordering_fields:
#                 items= items.order_by(ordering_field)

#         paginator=Paginator(items,per_page=perpage)
#         try:
#             items=paginator.page(number=page)
#         except EmptyPage:
#             items=[]
#         serialized_item=MenuItemSerializer(items,many=True)
#         return Response(serialized_item.data)
#     elif request.method=='POST':
#         if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
#             serialized_item=MenuItemSerializer(data= request.data)
#             serialized_item.is_valid(raise_exception=True)
#             serialized_item.save()
#             return Response({'message':"ok"})
#         return Response({'message':"You ar not authorized"})