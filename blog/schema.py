import graphene
from graphene_django import DjangoObjectType
from Post.models import Post, Comment


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "publish_date", "description", "author_name", "comments" )

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "post", "text", "name")


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post_by_id = graphene.Field(PostType, id=graphene.Int(required=True))
    post_by_author = graphene.List(PostType, author_name=graphene.String(required=True))

#*****define Resolvers for the queries**********
    def resolve_all_posts(self, root):
        return Post.objects.all()


    def resolve_post_by_id(self, root, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            return None

    def resolve_post_by_author(self, root, author_name):
        return Post.objects.filter(author_name__iexact=author_name)

#****************Create New Post****************

class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        author_name = graphene.String()

    @classmethod
    def mutate(cls, self, info, title, description, author_name):
        post = Post(title=title, description=description, author_name=author_name)
        post.save()
        return CreatePost(post=post)

#****************Update existing Post by ID****************
class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        author_name = graphene.String()
        id = graphene.Int()

    @classmethod
    def mutate(cls, self, info, id, title, description, author_name):
        post = Post.objects.get(id=id)
        post.title = title
        post.description = description
        post.author_name = author_name
        post.save()
        return UpdatePost(post=post)

#**********Create New Comment************
class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        name = graphene.String()
        text = graphene.String()
        post_id = graphene.Int()

    @classmethod
    def mutate(cls, self, info, name, text, post_id):
        comment = Comment(name=name, text=text)
        post = Post.objects.get(id=post_id)
        comment.post = post
        comment.save()

        return CreateComment(comment=comment)

#****************Delete Existing Post by ID****************
class DeleteComment(graphene.Mutation):
    message = graphene.String(default_value="Comment not Found!!")

    class Arguments:
        id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            comment = Comment.objects.get(id=id)
            comment.delete()
            return DeleteComment(message="Comment deleted successfully")
        except Comment.DoesNotExist:
            return DeleteComment()


class Mutation(graphene.ObjectType):
    create_new_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
