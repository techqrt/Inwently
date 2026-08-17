# biller_apps/customer_quotation/serializers/request/review.py
from rest_framework import serializers
from biller_apps.customer_quotation.dataclasses.request.review import CustomerQuotationReview


class CustomerQuotationReviewSerializer(serializers.Serializer):
    customer_quotation_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=["phone_confirmed", "rejected", "cancelled"])

    def create(self, validated_data) -> CustomerQuotationReview:
        return CustomerQuotationReview(**validated_data)