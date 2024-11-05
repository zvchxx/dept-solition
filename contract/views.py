from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from contract.models import ContractModel
from contract.serializers import ContractSerializers


class DebtsView(ListCreateAPIView):
    serializer_class = ContractSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ContractModel.objects.filter(user=user, status='active')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyBorrowedDebtsView(ListCreateAPIView):
    serializer_class = ContractSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ContractModel.objects.filter(user=user, debt_type='borrowed', status='active')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, debt_type='borrowed')


class MyLentDebtsView(ListCreateAPIView):
    serializer_class = ContractSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ContractModel.objects.filter(user=user, debt_type='lent', status='active')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, debt_type='lent')


class InactiveDebtsView(ListCreateAPIView):
    serializer_class = ContractSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ContractModel.objects.filter(user=user, status='inactive')


class ChangeDebtStatusView(RetrieveUpdateAPIView):
    queryset = ContractModel.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        debt = self.get_object()
        debt.status = 'inactive'
        debt.save()
        return Response({"message": "Debt inactivated successfully"})


class GetAllDebtsView(ListAPIView):
    serializer_class = ContractSerializers
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ContractModel.objects.all()


class DetailedDebtView(RetrieveAPIView):
    queryset = ContractModel.objects.all()
    serializer_class = ContractSerializers
    permission_classes = [IsAdminUser]