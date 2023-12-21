from rest_framework import serializers


class MetaDataSerializer(serializers.Serializer):
    parentResourceId = serializers.CharField(allow_blank=False)


class LogEntrySerializer(serializers.Serializer):
    level = serializers.CharField(allow_blank=False)
    message = serializers.CharField(allow_blank=False)
    resourceId = serializers.CharField(allow_blank=False)
    timestamp = serializers.DateTimeField(allow_null=False, format="%Y-%m-%dT%H:%M:%SZ")
    traceId = serializers.CharField(allow_blank=False)
    spanId = serializers.CharField(allow_blank=False)
    commit = serializers.CharField(allow_blank=False)
    metadata = MetaDataSerializer()
