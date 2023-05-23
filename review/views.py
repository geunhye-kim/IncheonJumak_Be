from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from review.models import Review
from review.serializers import ReviewSerializer, ReviewCreateSerializer, ReviewListSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# Create your views here.
class ReviewView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=ReviewCreateSerializer)
    def post(self, request):
        print(request.user)
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReviewDetailView(APIView):
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=ReviewCreateSerializer)
    def put(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        print(request.user)
        print(review.user)
        if request.user == review.user:
            serializer = ReviewCreateSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
    @swagger_auto_schema()
    def delete(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            review.delete()
            return Response("삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
    
class CommentView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass
    
class CommentDetailView(APIView):
    def put(self, request):
        pass
    def delete(self, request):
        pass
    
class LikeView(APIView):
    def post(self, request):
        pass