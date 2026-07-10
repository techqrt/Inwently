from rest_framework import serializers
from biller_apps.organisation.dataclasses.request.version import Version, VersionDetail
import re
from django.core.validators import RegexValidator, MinValueValidator

class VersionDetailResponseSerializer(serializers.Serializer):
    version = serializers.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^\d+\.\d+\.\d+$',
                message='Version must be in x.y.z format',
                code='invalid_version'
            )
        ],
        error_messages={
            'required': 'Version is required'
        },
    )
    build = serializers.IntegerField(
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Build number must be greater than 0'
            )
        ],
        error_messages={
            'required': 'Build number is required'
        },
    )

class VersionCreateSerializer(serializers.Serializer):
    repo_url = serializers.URLField(default=None,required=False,allow_null=True)
    file_name = serializers.CharField(max_length=255,default=None, required=False,allow_null=True)
    minimum_version = VersionDetailResponseSerializer(required=True)
    latest_stable_version = VersionDetailResponseSerializer(required=True)
    previous_stable_version = VersionDetailResponseSerializer(required=True)
    beta_version = VersionDetailResponseSerializer(default=None,required=False, allow_null=True)
    other_versions = VersionDetailResponseSerializer(many=True, default=None, required=False, allow_null=True)
    changes_in_latest_stable = serializers.ListField(child=serializers.CharField(),required=True)

    def create(self, validated_data) -> Version:
        return Version(**validated_data)
