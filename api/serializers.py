from django.db import transaction
from rest_framework import serializers

from api.models import Citizen, Import


class RelativesField(serializers.RelatedField):
    queryset = Citizen.objects.none()

    def to_representation(self, citizen):
        return citizen.citizen_id

    def to_internal_value(self, citizen_id):
        return citizen_id


class CitizenSerializer(serializers.ModelSerializer):
    relatives = RelativesField(many=True)

    class Meta:
        model = Citizen
        fields = ['citizen_id', 'town', 'street', 'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives']

    def update(self, instance, validated_data):
        if len(validated_data) == 0:
            raise serializers.ValidationError({'message': 'Update request cannot be empty'})

        if 'citizen_id' in validated_data:
            raise serializers.ValidationError(
                {'message': 'Cannot update citizen_id'})

        relatives_data = validated_data.pop('relatives', None)

        instance = super().update(instance, validated_data)

        if relatives_data:
            import_citizens = Citizen.objects.filter(enclosing_import=instance.enclosing_import)
            instance.relatives.clear()
            instance.relatives.add(*[import_citizens.get(citizen_id=relative_id) for relative_id in relatives_data])

        return instance


class ImportSerializer(serializers.ModelSerializer):
    citizens = CitizenSerializer(many=True)

    class Meta:
        model = Import
        fields = '__all__'

    def create(self, validated_data):
        citizens = []
        relatives = []
        citizen_map = {}
        citizens_data = validated_data.pop('citizens')

        with transaction.atomic():
            enclosing_import = super().create(validated_data)

            for citizen_data in citizens_data:
                relatives.append(citizen_data.pop('relatives'))
                citizen = Citizen.objects.create(enclosing_import=enclosing_import, **citizen_data)
                citizens.append(citizen)
                citizen_map[citizen.citizen_id] = citizen

            for i, citizen in enumerate(citizens):
                for citizen_id in relatives[i]:
                    if citizen_id not in citizen_map:
                        raise serializers.ValidationError(
                            {'message': 'There is no relative with citizen_id = {}'.format(citizen_id)})
                    citizen.relatives.add(citizen_map[citizen_id])

            return enclosing_import
