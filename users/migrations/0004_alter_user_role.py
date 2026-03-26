# Generated manually for role simplification: 5 roles → 3 roles
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[
                    ('ADMIN', 'Admin'),
                    ('MANAGER', 'Manager'),
                    ('EMPLOYEE', 'Employee'),
                ],
                default='EMPLOYEE',
                max_length=20,
            ),
        ),
    ]
