from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView
from graphene_django.views import GraphQLView

from .views import GraphQLPlaygroundView
from .schema import schema


app_name= "GraphQL"


urlpatterns = [
    path(
        "graphql",
        csrf_exempt(
            FileUploadGraphQLView.as_view(
                graphiql=False,
                # schema=schema,
            )
        ),
        name= "GraphQL",
    ),
    path("playground",
        csrf_exempt(
            GraphQLPlaygroundView.as_view(endpoint="/graphql"),
        ),
        name= "Playground",
    ),
    path(
        "defaultGraphql",
        csrf_exempt(
            GraphQLView.as_view(graphiql=True, schema=schema),
        ),
        name= "DefaultGraphQL",
    ),
]
