from django.db import migrations

from users.models import User

def create_system_user(apps, schema_editor):
    system_user = User.objects.create_system_user()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_user_is_system')
    ]

    operations = [
        migrations.RunPython(create_system_user)
    ]
