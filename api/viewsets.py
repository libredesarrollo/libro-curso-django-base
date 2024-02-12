from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from elements.models import Element, Category, Type
from comments.models import Comment
from .serializer import ElementReadOnlySerializer, ElementCreateUpdateDestroySerializer, CategorySerializer, TypeSerializer, CommentSerializer

class CreateUpdateDestroyViewSet(mixins.CreateModelMixin, 
                                 mixins.DestroyModelMixin, 
                                 mixins.UpdateModelMixin, 
                                 viewsets.GenericViewSet):
    pass

class ElementReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = Element.objects.all()
    serializer_class = ElementReadOnlySerializer

    @action(detail=False, methods=['get'])
    def all(self, request):
        queryset = Element.objects.all()
        serializer = ElementReadOnlySerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def url(self, request):
        queryset = Element.objects.get(slug=request.query_params['slug'])
        serializer = ElementReadOnlySerializer(queryset, many=False)
        return Response(serializer.data)



class ElementCreateUpdateDestroyViewSet(CreateUpdateDestroyViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementCreateUpdateDestroySerializer

    # def perform_create(self, serializer):
    #     cateid = self.request.data.get("category")
    #     typeid = self.request.data.get("type")
    #     serializer.save(
    #         category=Category.objects.get(pk=cateid),
    #         type=Type.objects.get(pk=typeid)
    #     )

# class ElementReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Element.objects.all()
#     serializer_class = ElementSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # authentication_classes = [ BasicAuthentication, SessionAuthentication ]
    # permission_classes = [ IsAuthenticated ]