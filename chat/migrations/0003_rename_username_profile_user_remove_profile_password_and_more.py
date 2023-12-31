# Generated by Django 4.2.6 on 2023-10-13 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_item_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='username',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='password',
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='benz.jpg', upload_to='profile'),
        ),
    ]
