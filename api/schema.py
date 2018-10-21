import graphene

from geo.schema import GeoQuery
from users.schema import UserQuery


class RootQuery(graphene.ObjectType, UserQuery, GeoQuery):
    pass

schema = graphene.Schema(query=RootQuery)