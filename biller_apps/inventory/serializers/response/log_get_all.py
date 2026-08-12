from rest_framework import serializers


class InventoryLogDataSerializer(serializers.Serializer):

    logId = serializers.IntegerField()

    inventoryId = serializers.IntegerField(
        allow_null=True
    )

    inventoryCode = serializers.CharField(
        allow_null=True
    )

    changeDate = serializers.DateTimeField()

    eventtype = serializers.CharField()

    batchId = serializers.UUIDField(
        allow_null=True
    )

    status = serializers.CharField()

    errorMessage = serializers.CharField(
        allow_null=True
    )