"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from texthandle.views import *

# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)

class TexthandleViewsTest(TestCase):

    def test_string_process():
        """
        string_process() should return queries with corresponding Boolean Operator
        """
        pass # to be completed

    def test_snippet_process(self):
        """
        snippet_process() should return a list of tokens without stopwords
        or words with capital-letter in it
        """
        snippet = """Python is a widely used general-purpose, high-level
                    programming language Its design philosophy emphasizes
                    code readability, and its syntax allows programmers to"""
        processed_tokens = ['python', 'widely', 'general-purpose',\
                             'high-level', 'programming', 'language', 'design',\
                             'philosophy', 'emphasizes', 'code', 'readability',\
                             'syntax', 'allows', 'programmers']

        self.assertEqual(snippet_process(snippet), processed_tokens)

    def test_flatten_with_flat_list(self):
        """
        flatten() should return the same list as passed if the list
        is already flat
        """
        flat_list = ['foo', 'bar', 'spam', 'egg']

        self.assertEqual(flatten(flat_list), flat_list)

    def test_flatten_with_nest_list(self):
        """
        flatten() should return one-level list if the list provided
        has nested list(s)
        """
        nested_list = [
                        ['foo', 'bar'], 
                        [
                            'spam', 
                            'egg', 
                            ['monty', 'python']
                        ], 
                        [
                            'alpha', 
                            [
                                'beta', 
                                [
                                    'sigma', 
                                    ['delta', 'omega']
                                ]
                            ]
                        ]
                    ]
        flattened_list = ['foo', 'bar', 'spam', 'egg', 'monty', 'python',\
                            'alpha', 'beta', 'sigma', 'delta', 'omega']

        self.assertEqual(flatten(nested_list), flattened_list)