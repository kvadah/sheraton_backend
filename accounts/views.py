from django.shortcuts import render
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework.views import APIView
# Create your views here.
from rest_framework import status


class RegisterView(APIView):

    def post(self,request):
        serializer = RegisterSerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response ({'Register Successfull'})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
