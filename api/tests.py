import ast

from rest_framework.test import APITestCase, APIClient

from comments.models import Comment
from elements.models import Element, Category, Type

from api.serializer import CommentSerializer, ElementReadOnlySerializer

class CommentApiTest(APITestCase):
    def setUp(self):
        self.comment = Comment.objects.create(text='Text1')
        Comment.objects.create(text='Text2')
        Comment.objects.create(text='Text3')

        self.client = APIClient()

    # paginado
    def test_get_comments_pagination(self):
        response = self.client.get('/api/comment/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Text1')
        self.assertContains(response, 'Text2')
        self.assertContains(response, 'Text3')

        # prueba el objeto completo, equivalente a los assert de arriba individuales    
        bytes_dict_res = response.content
        dict_str = bytes_dict_res.decode('UTF-8').replace('null','""')
        self.assertIn(str(CommentSerializer(instance=self.comment).data).replace("'",'"').replace(" ",'').replace('None','""'), dict_str)
        
    def test_get_comments_detail(self):
        response = self.client.get('/api/comment/'+str(self.comment.id)+'/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.comment.text)

    def test_get_comments_detail_serializacion(self):
        response = self.client.get('/api/comment/'+str(self.comment.id)+'/')
        self.assertEqual(response.status_code, 200)

        # print(CommentSerializer(self.comment).data)

        self.assertJSONEqual(response.content, CommentSerializer(self.comment).data)

    def test_get_comments_create_success(self):

        data = { 'text':'Text 4' }
        response = self.client.post('/api/comment/', data)
        self.assertEqual(response.status_code, 201)
        bytes_dict_res = response.content
        dict_str = bytes_dict_res.decode('UTF-8').replace('null','""')
        # print(dict_str)
        # data_dict = ast.literal_eval(dict_str)
        data_dict = eval(dict_str)

        response = self.client.get('/api/comment/'+str(data_dict.get('id'))+'/')
        self.assertEqual(response.status_code, 200)

    def test_create_error_form(self):
        data = {'text':''}
        response = self.client.post('/api/comment/',data)
        self.assertEqual(response.status_code,400)
        self.assertJSONEqual(response.content, '{ "text": [ "This field may not be blank." ] }')

    def test_create_error_form_empty(self):
        data = {}
        response = self.client.post('/api/comment/',data)
        self.assertEqual(response.status_code,400)
        self.assertJSONEqual(response.content, '{ "text": [ "This field is required." ] }')

    def test_update_success(self):

        data = { 'text':'New Text' }
        response = self.client.put('/api/comment/'+str(self.comment.id)+'/', data)
        self.assertEqual(response.status_code, 200)
      
        comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(comment.text, data.get('text'))

    def test_delete(self):
        response = self.client.delete('/api/comment/'+str(self.comment.id)+'/')
        self.assertEqual(response.status_code, 204)

        try:
            Comment.objects.get(pk=self.comment.id)
            raise Exception('El comentario deberia haber sido eliminado')
        except Comment.DoesNotExist:
            pass

    def test_comment_serializer(self):
        cs = CommentSerializer(self.comment).data
        self.assertEqual(cs['id'], self.comment.id)
        self.assertEqual(cs['text'], self.comment.text)
        self.assertEqual(cs['count'], Comment.objects.filter(element_id = self.comment.element_id).count())
        # self.assertEqual(cs['element'], self.comment.element)


import json
class ElementApiTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Cate1', slug='cate-1')
        self.category2 = Category.objects.create(title='Cate2', slug='cate-2')
        self.type = Type.objects.create(title='Type1', slug='type-1')
        self.type2 = Type.objects.create(title='Type2', slug='type-2')

        self.element = Element.objects.create(title='Element1', slug='element-1', description='Element1description', category=self.category2, type=self.type)
        self.element2 = Element.objects.create(title='Element2', slug='element-2', description='Element 2 description', price=5.00, category=self.category2, type=self.type2)
        self.element3 = Element.objects.create(title='Element3', slug='element-3', description='Element 3 description', price=1.22, category=self.category, type=self.type)

        self.client = APIClient()

    # paginado
    def test_get_comments_pagination(self):
        response = self.client.get('/api/element/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.element.title)
        self.assertContains(response, self.element.slug)
        self.assertContains(response, self.element.description)
        self.assertContains(response, self.element.price)
        self.assertContains(response, self.element.category.title)
        self.assertContains(response, self.element.type.title)

        bytes_dict_res = response.content
        dict_str = bytes_dict_res.decode('UTF-8').replace('null','""')
        data = str(json.dumps(ElementReadOnlySerializer(self.element).data)).replace(" ",'')

        # equivalente a los assertContains de arriba pero compara el objeto completo
        self.assertIn(data, dict_str)
        #equivalente a al assert anterior
        self.assertContains(response, data)

    def test_get_comments_create_success(self):

        data = { 'title':'Element 4', 'slug': 'element-4','description':'Test test test...', 'category': self.category.id, 'type': self.type.id }
        response = self.client.post('/api/element2/', data)
        print(response.content)
        self.assertEqual(response.status_code, 201)
        bytes_dict_res = response.content
        dict_str = bytes_dict_res.decode('UTF-8')
        
        # # data_dict = ast.literal_eval(dict_str)
        data_dict = eval(dict_str)
        response = self.client.get('/api/element/'+str(data_dict.get('id'))+'/')
        self.assertEqual(response.status_code, 200)
    
    def test_update_success(self):

        data = { 'title':'Element 4 new', 'slug': 'element-4-new','description':'Test test test... new', 'category': self.category2.id, 'type': self.type2.id }
        response = self.client.put('/api/element2/'+str(self.element.id)+'/', data)
        self.assertEqual(response.status_code, 200)
      
        element = Element.objects.get(id=self.element.id)
        self.assertEqual(element.title, data.get('title'))
        self.assertEqual(element.slug, data.get('slug'))
        self.assertEqual(element.description, data.get('description'))
        self.assertEqual(element.category.id, data.get('category'))
        self.assertEqual(element.type.id, data.get('type'))

    def test_create_error_form(self):
        data = { 'title':'','description':'', 'category': '', 'type': '' }
        response = self.client.post('/api/element2/',data)
        self.assertEqual(response.status_code,400)
        self.assertJSONEqual(response.content, '{ "title": [ "This field may not be blank." ], "description": [ "This field may not be blank." ], "category": [ "This field may not be null." ], "type": [ "This field may not be null." ] }')

    def test_create_error_form_empty(self):
        data = { }
        response = self.client.post('/api/element2/',data)
        self.assertEqual(response.status_code,400)
        self.assertJSONEqual(response.content, '{ "title": [ "This field is required." ], "description": [ "This field is required." ], "category": [ "This field is required." ], "type": [ "This field is required." ] }')

    def test_delete(self):
        response = self.client.delete('/api/element2/'+str(self.element.id)+'/')
        self.assertEqual(response.status_code, 204)

        try:
            Element.objects.get(pk=self.element.id)
            raise Exception('El elemento deberia haber sido eliminado')
        except Element.DoesNotExist:
            pass

    def test_element_serializer(self):
        es = ElementReadOnlySerializer(self.element).data
        print(es)
        self.assertEqual(es['id'], self.element.id)
        self.assertEqual(es['title'], self.element.title)
        self.assertEqual(es['description'], self.element.description)
        self.assertEqual(es['slug'], self.element.slug)
        self.assertEqual(float(es['price']), self.element.price)
        self.assertTrue(es['category'] != None)
        self.assertTrue(es['type'] != None)


        # self.assertEqual(es['count'], Comment.objects.filter(element_id = self.comment.element_id).count())