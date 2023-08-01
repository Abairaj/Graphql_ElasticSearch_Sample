import graphene

from . import category_schema
from . import book_schema
from . import author_schema


class Mutation(category_schema.Mutation, book_schema.Mutation, author_schema.Mutation, graphene.ObjectType):
    pass


class Query(category_schema.Query, book_schema.Query, author_schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
