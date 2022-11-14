import graphene_django_optimizer as gql_optimizer
from django.db.models.query import QuerySet
from graphene import Field, ObjectType, String
from graphene_django.filter import DjangoFilterConnectionField

from GraphQL.mutations import AppResolverInfo
from .models import Article
from .types import ArticleNode
from .filters import ArticleFilterSet


class ArticleQuery(ObjectType):
    articles = DjangoFilterConnectionField(
        ArticleNode, filterset_class=ArticleFilterSet
    )
    get_article = Field(ArticleNode, slug=String(required=True))

    @staticmethod
    def resolve_articles(root, info: AppResolverInfo, **fields) -> QuerySet[Article]:
        return gql_optimizer.query(Article.objects.all(), info, disable_abort_only=True)

    @staticmethod
    def resolve_get_article(root, info: AppResolverInfo, **fields) -> QuerySet[Article]:
        optimized_query = gql_optimizer.query(
            Article.objects.filter(slug=fields.get("slug")),
            info,
            disable_abort_only=True,
        )
        return optimized_query.first()
