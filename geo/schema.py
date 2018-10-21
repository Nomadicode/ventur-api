import graphene

from graphene_django.types import DjangoObjectType
from graphene_django import DjangoConnectionField

from .models import Continent, Country, Region, City


class ContinentType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Continent


class CountryType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Country


class RegionType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Region


class CityType(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = City


class GeoQuery(graphene.AbstractType):
    continents = graphene.List(ContinentType)
    countries = graphene.List(CountryType)
    regions = graphene.List(RegionType)
    cities = graphene.List(CityType)


    def resolve_continents(self, info, **kwargs):
        return Continent.objects.all()

    def resolve_countries(self, info, **kwargs):
        return Country.objects.all()

    def resolve_regions(self, info, **kwargs):
        return Region.objects.all()

    def resolve_cities(self, info, **kwargs):
        return City.objects.all()