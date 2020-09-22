from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter

from account_manager.models import Account
from ebook.models import EbookPost
from ebook.api.serializers import EbookPostSerializer


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_ebook(request, slug):

    try:
        ebook_post = EbookPost.objects.get(slug=slug)
    except EbookPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = EbookPostSerializer(ebook_post)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAdminUser,))
def api_update_ebook(request, slug):

    try:
        ebook_post = EbookPost.objects.get(slug=slug)
    except EbookPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = EbookPostSerializer(ebook_post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAdminUser,))
def api_delete_ebook(request, slug):

    try:
        ebook_post = EbookPost.objects.get(slug=slug)
    except EbookPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        operation = ebook_post.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete successful"
        return Response(data=data)


@api_view(['POST', ])
@permission_classes((IsAdminUser,))
def api_create_ebook(request):
    if request.method == "POST":
        serializer = EbookPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiEbookList(ListAPIView):
    queryset = EbookPost.objects.all()
    serializer_class = EbookPostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'description', 'author')