from rest_framework import serializers

#https://medium.com/wasd/restful-api-in-django-16fc3fb1a238


from code_master.models import AutoMarkMachine, AutoPressMachine, RpcagMachine, SmartCamMachine

class AutoMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoMarkMachine
        fields = ('__all__')

class RpcagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RpcagMachine
        fields = ('__all__')

class AutoPressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoPressMachine
        fields = ('__all__')

class SmartCamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartCamMachine
        fields = ('__all__')