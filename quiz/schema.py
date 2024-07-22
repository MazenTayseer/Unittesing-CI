import graphene
from graphene_django.types import DjangoObjectType
from graphene_django import DjangoListField
from .models import Category, Quizzes


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        field = "__all__"


class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        field = "__all__"



class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryType, id=graphene.Int())
    all_quizzes = graphene.List(QuizzesType, id=graphene.Int())

    def resolve_all_categories(self, info, id=None):
        return Category.objects.filter(id=id) if id is not None else Category.objects.all()

    def resolve_all_quizzes(self, info, id=None):
        return Quizzes.objects.filter(id=id) if id is not None else Quizzes.objects.all()



schema = graphene.Schema(query=Query)
