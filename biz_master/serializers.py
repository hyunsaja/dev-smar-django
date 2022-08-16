from rest_framework import serializers
from .models import BizMaster

# 비즈마스터 list 검색
class BizMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BizMaster
        fields = ('__all__')

# 비즈코드 list 검색
class BizCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BizMaster
        fields = ('UserID', 'Material', 'work_select')

# test/serializers.py
# class BasePersonSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     phone = serializers.CharField()
#     addr = serializers.CharField()
#
#     def create(self, validated_data):
#         """
#         검증한 데이터로 새 `Person` 인스턴스를 생성하여 리턴합니다.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         검증한 데이터로 기존 `Person` 인스턴스를 업데이트한 후 리턴합니다.
#         """
#         return instance
