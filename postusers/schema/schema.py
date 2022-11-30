from graphene_django import DjangoObjectType
import graphene
from postusers.models import Post as PostModel
from postusers.models import Author as AuthorModel

class PostType(DjangoObjectType):
    class Meta:
        model = PostModel
        fields = ['id', 'title', 'body', 'author']


class AuthorType(DjangoObjectType):
    class Meta:
        model = AuthorModel
        fields = ['id', 'name', 'posts']

    def resolve_posts(self, info):
                return PostModel.objects.filter(author=self)

    @classmethod
    def get_node(cls, info, id):
        return Author.objects.get(id=id)


class Query(graphene.ObjectType):
    authors = graphene.List(AuthorType)
    author = graphene.Field(AuthorType, id=graphene.ID())
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.ID())

    def resolve_authors(self, info):
        return AuthorModel.objects.all()

    def resolve_author(self, info, id):
        return AuthorModel.objects.get(pk=id)

    def resolve_posts(self, info):
        return PostModel.objects.all()

    def resolve_post(self, info, id):
        return PostModel.objects.get(pk=id)


class AuthorInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class PostInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    body = graphene.String()
    author = graphene.ID()


class CreatePost(graphene.Mutation):
    class Arguments:
        post_data = PostInput(required=True)

    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, post_data=None):
        post_instance = PostModel(
            title = post_data.title,
            body = post_data.body,
            author = post_data.author
            )
        post_instance.save()
        return CreatePost(post=post_instance)


class CreateAuthor(graphene.Mutation):
    class Arguments:
        author_data = AuthorInput(required=True)

    author = graphene.Field(AuthorType)

    @staticmethod
    def mutate(root, info, author_data=None):
        author_instance = AuthorModel(
            name = author_data.name
            )
        author_instance.save()
        return CreateAuthor(author=author_instance)


# class UpdatePost(graphene.Mutation):
#     pass


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    create_author = CreateAuthor.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)