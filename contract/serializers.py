from rest_framework import serializers

from contract.models import ContractModel


class ContractSerializers(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(required=False)
    note = serializers.CharField(max_length=255, required=False)
    type = serializers.ChoiceField(choices=ContractModel.CONTRACT_TYPE)
    currency = serializers.ChoiceField(choices=ContractModel.CURRENCY)


    class Meta:
        model = ContractModel
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'who', 'status']