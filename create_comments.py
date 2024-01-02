from faker import Faker

from comments.models import Comment

def main():
    fake = Faker()

    for _ in range(5):
        comment = Comment.object.create(
            text = fake.text()
        )

    comments = Comment.objects.all()

    print(f'Comments in DB {comments.count()}')


if __name__ == "__main__":
    import os
    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mystore.settings')

    application = get_wsgi_application()

    main()