import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Categories


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Categories
        filter_fields = ["name"]
        interfaces = (relay.Node,)


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryNode)

    @classmethod
    def mutate(cls, root, info, name):
        category = Categories(name=name)
        category.save()
        return CreateCategory(category=category)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)
    category = graphene.Field(CategoryNode)

    @classmethod
    def mutate(cls, root, id, name):
        try:
            category = Categories.objects.get(id=id)
            category.name = name
            category.save()
            return UpdateCategory(category=category)
        except Categories.DoesNotExist():
            print('category not found')


class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    category = graphene.Field(CategoryNode)

    @classmethod
    def mutate(cls, root, info, id):
        try:
            category = Categories.objects.get(id=id)
            category.delete()
            return DeleteCategory(category=category)
        except Categories.DoesNotExist:
            raise graphene.exceptions.ValidationError("category not found")


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()


class Query(graphene.ObjectType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)
