import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import (
    Books,
    Categories,
    Author
)


class AuthorNode(DjangoObjectType):
    class Meta:
        model = Author
        filter_fields = ['name', 'place']
        interfaces = (relay.Node,)


class CategoryNode(DjangoObjectType):
    class Meta:
        model = Categories
        filter_fields = ['name']
        interface = (relay.Node,)


class BookNode(DjangoObjectType):
    class Meta:
        model = Books
        filter_fields = ['title', 'author', 'category']
        interfaces = (relay.Node,)

    author = graphene.Field(AuthorNode)
    category = graphene.Field(CategoryNode)

    def resolve_author(self, info):
        return self.author

    def resolve_category(self, info):
        return self.category


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author_id = graphene.ID(required=True)
        category_id = graphene.ID(required=True)
        price = graphene.ID(required=True)
        description = graphene.String()

    book = graphene.Field(BookNode)

    @classmethod
    def mutate(cls, root, info, title, author_id, category_id, description, price):
        author = Author.objects.get(id=author_id)
        category = Categories.objects.get(id=category_id)
        book = Books(title=title, author=author, category=category,
                     description=description, price=price)
        book.save()
        return CreateBook(book=book)


class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        author_id = graphene.ID()
        category_id = graphene.ID()
        price = graphene.ID()
        description = graphene.String()
        title = graphene.String()
    book = graphene.Field(BookNode)

    @classmethod
    def mutate(cls, root, info, id, title=None, author_id=None, category_id=None, description=None, price=None):
        book = Books.objects.get(id=id)
        book = None
        if title:
            book.title = title
        if author_id:
            author = Author.objects.get(id=author_id)
            book.author = author
        if category_id:
            category = Categories.objects.get(id=category_id)
            book.category = category
        if description:
            book.description = description
        if price:
            book.price = price

        book.save()
        return UpdateBook(book=book)


class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    book = graphene.Field(BookNode)

    @classmethod
    def mutate(cls, root, info, id):
        try:
            book = Books.objects.get(id=id)
            book.delete()
        except Books.DoesNotExist():
            print('Book does not exist')
        return DeleteBook(book=book)


class Mutation(graphene.ObjectType):
    create_books = CreateBook.Field()
    update_books = UpdateBook.Field()
    delete_books = DeleteBook.Field()


class Query(graphene.ObjectType):
    books = relay.Node.Field(BookNode)
    all_books = DjangoFilterConnectionField(BookNode)
