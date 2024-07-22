from graphene.test import Client
from django.test import TestCase
from .schema import schema  
from .models import Category, Quizzes


class GraphQLTests(TestCase):
    def setUp(self):
        # Create test data
        self.category1 = Category.objects.create(name="Category 1", slug="category-1")
        self.category2 = Category.objects.create(name="Category 2", slug="category-2")

        self.quiz1 = Quizzes.objects.create(name="Quiz 1", slug="quiz-1", category=self.category1)
        self.quiz2 = Quizzes.objects.create(name="Quiz 2", slug="quiz-2", category=self.category2)

        self.client = Client(schema)

    def test_all_categories_query(self):
        query = '''
            query {
                allCategories {
                    id
                    name
                    slug
                }
            }
        '''
        executed = self.client.execute(query)
        self.assertEqual(executed['data']['allCategories'], [
            {'id': str(self.category1.id), 'name': 'Category 1', 'slug': 'category-1'},
            {'id': str(self.category2.id), 'name': 'Category 2', 'slug': 'category-2'},
        ])

    def test_all_quizzes_query(self):
        query = '''
            query {
                allQuizzes {
                    id
                    name
                    slug
                    category {
                        id
                        name
                    }
                }
            }
        '''
        executed = self.client.execute(query)
        self.assertEqual(executed['data']['allQuizzes'], [
            {'id': str(self.quiz1.id), 'name': 'Quiz 1', 'slug': 'quiz-1', 'category': {'id': str(self.category1.id), 'name': 'Category 1'}},
            {'id': str(self.quiz2.id), 'name': 'Quiz 2', 'slug': 'quiz-3', 'category': {'id': str(self.category2.id), 'name': 'Category 2'}},
        ])
