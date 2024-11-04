from django.shortcuts import render

from rest_framework.response import Response

from rest_framework import generics, status

from rest_framework.views import APIView

from django.contrib.auth import authenticate

from contract.models import ContractModel

from rest_framework.permissions import AllowAny

from contract.serializers import ContractSerializers

from rest_framework.authtoken.models import Token


class Contractview(generics.CreateAPIView):
    serializer_class = ContractSerializers
    queryset = ContractModel.objects.all()
    permission_classes = [AllowAny] 


    def perform_create(self, serializer):
        contract = serializer.save(
            who=self.request.user,
            status=ContractModel.STATUS_CHOICES.waiting.value
        )
        return contract


    def get(self, request, *args, **kwargs):
        contracts = self.get_object()
        serializer_data = self.serializer_class(contracts, many=True).data
        total_borrows = sum(borrow.amount for borrow in contracts if borrow.type == ContractModel.CONTRACT_TYPE.borrowed.value)