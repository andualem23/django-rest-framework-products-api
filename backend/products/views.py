from rest_framework import generics, mixins, permissions, authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.DjangoModelPermissions]
    
    def perform_create(self, serializer):
        title = serializer.validated_data.get('title'),
        content = serializer.validated_data.get('content') or None
        
        if content is None:
            content = title
            
        serializer.save(content=content)
        
        
product_list_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk' ??


product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.DjangoModelPermissions]
    
    
    def perform_update(self, serializer):
        instance = serializer.save()
        
        if not instance.content:
            instance.content = instance.title
            instance.save()


product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

product_delete_view = ProductDestroyAPIView.as_view()



class ProductMixinView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
        
    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content') or None
        
        if content is None:
            content = "This single view doing amazing stuff"
            
        serializer.save(content=content)

product_mixin_view = ProductMixinView.as_view()


@api_view(['GET', 'POST'])
def product_alt_view(request,pk= None ,*args, **kwargs):
    method = request.method
    
    if method == 'GET':
        if pk  is not None:
            product = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(product).data
            return Response(data)
        
        qs = Product.objects.all()
        data = ProductSerializer(qs, many=True).data
        return Response(data)
    
    if method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title'),
            content = serializer.validated_data.get('content') or None
            
            if content is None:
                content = title
                
            serializer.save(content=content)
            return Response(serializer.data)
        
        return Response({"invalid": "not good data"}, status=400)