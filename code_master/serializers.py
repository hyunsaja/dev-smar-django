from rest_framework import serializers

#https://medium.com/wasd/restful-api-in-django-16fc3fb1a238


from code_master.models import AutoMarkMachine

class AutoMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoMarkMachine
        # fields = ('ship_no', 'por_no', 'seq_no', 'block_no', 'pcs_no', 'paint_code', 'lot_no', 'author', 'machine_id')
        fields = ('__all__')
