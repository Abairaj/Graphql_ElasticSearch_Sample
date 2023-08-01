import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Author


class AuthorNode(DjangoObjectType):
    class Meta:
        model = Author
        filter_fields = ["name"]
        interfaces = (relay.Node,)


class CreateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        place = graphene.String()
        gender = graphene.String()
        nationality = graphene.String()
    author = graphene.Field(AuthorNode)
    @classmethod
    def mutate(cls, root, info, name, place, gender, nationality):
        author = Author(name=name, place=place, gender=gender,
                        nationality=nationality)
        author.save()
        return CreateAuthor(author=author)


class UpdateAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        place = graphene.String()
        gender = graphene.String()
        nationality = graphene.String()
    author = graphene.Field(AuthorNode)

    @classmethod
    def mutate(cls, root, info, name, place, gender, nationality):
        author = Author.objects.get(id=id)
        if name:
            author.name = name
        if place:
            author.place = place
        if gender:
            author.gender = gender
        if nationality:
            author.nationality = nationality

        author.save()
        return UpdateAuthor(author=author)


class DeleteAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    author = graphene.Field(AuthorNode)

    @classmethod
    def mutate(cls, root, info, id):
        try:
            author = Author.objects.get(id=id)
            author.delete()
        except Author.DoesNotExist():
            print('author not found')


class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()


class Query(graphene.ObjectType):
    author = relay.Node.Field(AuthorNode)
    all_author = DjangoFilterConnectionField(AuthorNode)
