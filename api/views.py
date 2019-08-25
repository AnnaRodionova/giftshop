import numpy as np
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Import, Citizen
from api.serializers import ImportSerializer, CitizenSerializer


@api_view(['POST'])
def import_list(request):
    serializer = ImportSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    import_instance = serializer.save()
    return Response({'data': {'import_id': import_instance.id}}, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def citizen(request, import_id, citizen_id):
    citizen_instance = get_object_or_404(Citizen, enclosing_import__id=import_id, citizen_id=citizen_id)
    serializer = CitizenSerializer(citizen_instance, data=request.data, partial=True, context={'import_id': import_id})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'data': serializer.data})


@api_view(['GET'])
def citizen_list(request, import_id):
    import_instance = get_object_or_404(Import, id=import_id)
    serializer = ImportSerializer(import_instance)
    return Response({'data': serializer.data.get('citizens')})


@api_view(['GET'])
def birthdays(request, import_id):
    import_citizens = get_object_or_404(Import, id=import_id).citizens
    months = {str(i): [] for i in range(1, 13)}

    for month in months:
        for citizen_with_presents_to_buy in import_citizens.filter(relatives__birth_date__month=month).all():
            months[month].append({
                'citizen_id': citizen_with_presents_to_buy.citizen_id,
                'presents': citizen_with_presents_to_buy.relatives.filter(birth_date__month=month).count()
            })

    return Response({'data': months})


@api_view(['GET'])
def age_percentile(request, import_id):
    import_citizens = get_object_or_404(Import, id=import_id).citizens

    result = []
    towns = import_citizens.values_list('town', flat=True).distinct()

    for town in towns:
        citizen_ages = [town_citizen.age for town_citizen in import_citizens.filter(town=town).all()]
        p50, p75, p99 = np.floor(np.percentile(citizen_ages, [50, 75, 99], interpolation='linear'))
        result.append({
            'town': town,
            'p50': p50,
            'p75': p75,
            'p99': p99
        })

    return Response({'data': result})
