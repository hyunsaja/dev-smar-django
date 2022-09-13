from rest_framework import serializers

#https://medium.com/wasd/restful-api-in-django-16fc3fb1a238


from code_master.models import AutoMarkMachine, AutoPressMachine, RpcagMachine

class AutoMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoMarkMachine
        # fields = ('ship_no', 'por_no', 'seq_no', 'block_no', 'pcs_no', 'paint_code', 'lot_no', 'author', 'machine_id')
        fields = ('__all__')

class RpcagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RpcagMachine
        fields = ('__all__')

class AutoPressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoPressMachine
        fields = ('__all__')