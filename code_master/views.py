from django.shortcuts import render

# Create your views here.

from django.views import View
from django.http import HttpResponse
from django.utils.html import mark_safe
import sys

# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================

# https://d-yong.tistory.com/61
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from code_master.models import FieldMaster
from code_master.serializers import FieldMasterSerializer


class RestApiFieldMaster(APIView):
    '''
    GET /RestApiFieldMaster
    GET /RestApiFieldMaster/{id}
    '''

    def get(self, request, **kwargs):
        if self.kwargs.get('pk') is None:
            queryset = FieldMaster.objects.all()  # .filter(status=5)   #ref code table
            serializer = FieldMasterSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                queryset = FieldMaster.objects.get(id=self.kwargs.get('pk'))
                # queryset = FieldMaster.objects.get(machine_id=self.kwargs.get('pk')).first()
                print(queryset)
                serializer = FieldMasterSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return HttpResponse(None)

    # '''
    # POST /RestApiContent
    # '''
    # def post(self, request):
    #     serializer = ContentSerializer(data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)

