from rest_framework import serializers
from apps.product.models import Product


class WebProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            "name",
            "composition",
            "count",
            "original_count",
            "price1",
            "price2",
            "expired_date",
            "seria",
            "active",
            'warehouse_count',
            'image_mobile',
            'image'
        ]


class WebCreateProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=400)
    composition = serializers.CharField()
    count = serializers.IntegerField()
    original_count = serializers.CharField()
    price1 = serializers.FloatField()
    price2 = serializers.FloatField()
    expired_date = serializers.CharField()
    seria = serializers.CharField()
    active = serializers.BooleanField()
    image_mobile = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = [
            "name",
            "composition",
            "count",
            "original_count",
            "price1",
            "price2",
            "expired_date",
            "seria",
            "active",
            'warehouse_count',
            'image_mobile'
        ]

    def create(self, validated_data: dict):
        request_user = self.context['request'].user
        validated_data['created_by'] = request_user
        validated_data['warehouse_count'] = validated_data['count']
        product = Product.objects.create(**validated_data)
        return product


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            "name",
            'composition',
            'count',
            'image_mobile'
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def update(self, instance: Product, validated_data: dict):
        if validated_data.get('warehouse_count'):
            instance.warehouse_count = validated_data.get('warehouse_count')
        instance.name = validated_data.get('name')
        instance.composition = validated_data.get('composition')
        instance.count = validated_data.get('count')
        instance.original_count = validated_data.get('original_count')
        instance.price1 = validated_data.get('price1')
        instance.expired_date = validated_data.get('expired_date')
        instance.active = validated_data.get('active')
        instance.image = validated_data.get('image')
        instance.image_mobile = validated_data.get('image_mobile')
        instance.created_by = instance.created_by
        instance.save()
        return instance


class ProductCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=400)
    composition = serializers.CharField()
    count = serializers.IntegerField()
    original_count = serializers.CharField()
    price1 = serializers.FloatField()
    price2 = serializers.FloatField()
    expired_date = serializers.CharField()
    seria = serializers.CharField()
    active = serializers.BooleanField()
    # image = serializers.CharField(required=False)
    image_mobile = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = [
            "name",
            "composition",
            "count",
            "original_count",
            "price1",
            "price2",
            "expired_date",
            "seria",
            "active",
            # "image",
            'warehouse_count',
            'image_mobile'
        ]

    def create(self, validated_data: dict):
        request_user = self.context['request'].user
        validated_data['created_by'] = request_user
        validated_data['warehouse_count'] = validated_data['count']
        product = Product.objects.create(**validated_data)
        return product
