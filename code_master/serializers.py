from rest_framework import serializers

#https://medium.com/wasd/restful-api-in-django-16fc3fb1a238


from code_master.models import CodeMaster
class CodeMasterSerializer(serializers.ModelSerializer):
    # ForeignKey 처리
    # group = serializers.ReadOnlyField(source='DidDeviceGroup.id')
    class Meta:
        model = CodeMaster
        fields = ('id', 'machine_id', 'ship_no', 'por_no', 'seq_no', 'pcs_no', 'part_no',  'adate')
        # fields = '__all__'



