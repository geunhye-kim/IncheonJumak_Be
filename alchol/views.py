from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from alchol.models import Alchol
from alchol.serializers import AlcholSerializer
from rest_framework.pagination import PageNumberPagination
from alchol.serializers import AlcholListSerializer

class AlcholPagination(PageNumberPagination):
    page_size = 2 #임의 페이지 수 설정해놨으니 후에 수정하면 됨

    
class AlcholView(APIView):
    pagination_class = AlcholPagination
    serializer_class = AlcholListSerializer
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):

        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
    
    def get(self, request):
        alchols = Alchol.objects.all().order_by('id') # 순서 오류가 나서 일단 'id'순으로 정렬, 나중에 변경해도 됨
        page = self.paginate_queryset(alchols)
        serializer = AlcholSerializer(alchols, many=True)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(alchols, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)

class AlcholCategoryView(APIView):
    def get(self, request, sort):
        alchols = Alchol.objects.filter(sort=sort)
        serializer = AlcholSerializer(alchols, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AlcholDetailView(APIView):
    def get(self, request, alchol_id):
        alchol = get_object_or_404(Alchol, id=alchol_id)
        serializer = AlcholSerializer(alchol)
        return Response(serializer.data, status=status.HTTP_200_OK)