from rest_framework import serializers
from .models import CamMaster

class CamMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CamMaster
        fields = '__all__'