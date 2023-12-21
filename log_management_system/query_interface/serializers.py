from rest_framework import serializers


class DateSerializer(serializers.Serializer):
    from_date = serializers.DateTimeField(
        required=True, allow_null=False, format="%Y-%m-%dT%H:%M:%SZ"
    )
    to_date = serializers.DateTimeField(
        required=False, allow_null=False, format="%Y-%m-%dT%H:%M:%SZ"
    )


class QuerySerializer(serializers.Serializer):
    size = serializers.IntegerField(required=False, allow_null=False)
    level = serializers.CharField(required=False, allow_blank=False)
    message = serializers.CharField(required=False, allow_blank=False)
    resourceId = serializers.CharField(required=False, allow_blank=False)
    timestamp = serializers.DateTimeField(
        required=False, allow_null=False, format="%Y-%m-%dT%H:%M:%SZ"
    )
    date = DateSerializer(required=False)
    traceId = serializers.CharField(required=False, allow_blank=False)
    spanId = serializers.CharField(required=False, allow_blank=False)
    commit = serializers.CharField(required=False, allow_blank=False)
    parentResourceId = serializers.CharField(required=False, allow_blank=False)
