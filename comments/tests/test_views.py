from django.test import Client, TestCase

from comments.models import Comment

class ContactTests(TestCase):

    def setUp(self):
        Comment.objects.create(text='text 1')
        Comment.objects.create(text='text 2')
        # Comment.objects.create(text='text 3')
        self.comments = Comment.objects.all()
        # print(self.comments)
        self.client = Client()

    def test_index(self):
        response = self.client.get("/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,self.comments[0].text)
        self.assertContains(response,self.comments[1].text)
        self.assertTemplateUsed(response, "comments/index.html")

    def test_post_get(self):
        response = self.client.get("/tasks/add")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'<textarea name="text" cols="40" rows="10" required id="id_text">')
        self.assertTemplateUsed(response, "comments/add.html")
        
    def test_post_post(self):
        text = 'text comment'
        response = self.client.post("/tasks/add" , {'text':text})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/tasks/')
        comment = Comment.objects.order_by('-id')[0]
    
        self.assertEqual(comment.text,text)

    def test_update_get(self):

        comment = Comment.objects.get(id=2)
        response = self.client.get("/tasks/update/"+str(comment.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,f'<textarea name="text" cols="40" rows="10" required id="id_text">\n{comment.text}')
        self.assertTemplateUsed(response, "comments/add.html")
        
    def test_update_post(self):
        comment = Comment.objects.get(id=2)
        text = 'text comment new'
        response = self.client.post("/tasks/update/"+str(comment.id) , {'text':text})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/tasks/')
    
        comment_updated = Comment.objects.get(id=2)
        self.assertEqual(comment_updated.text,text)

    def test_delete_post(self):
        comment = Comment.objects.get(id=2)
        response = self.client.post("/tasks/delete/"+str(comment.id))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/tasks/')
    
        try:
            Comment.objects.get(id=2)
            raise Exception('El comentario deberia haber sido eliminado')
        except Comment.DoesNotExist:
            pass

    