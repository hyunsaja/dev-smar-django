from rest_framework import serializers
from .models import PlateChamferMachine, RpcmS300Machine, RpcmAgcutMachine
from .models import CoamingMachine, MijuRobotWeldingMachine

class PlateChamferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlateChamferMachine
        fields = '__all__'

class RpcmS300Serializer(serializers.ModelSerializer):
    class Meta:
        model = RpcmS300Machine
        fields = '__all__'

class RpcmAgcutSerializer(serializers.ModelSerializer):
    class Meta:
        model = RpcmAgcutMachine
        fields = '__all__'

class CoamingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoamingMachine
        fields = '__all__'

class MijuRobotWeldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MijuRobotWeldingMachine
        fields = '__all__'