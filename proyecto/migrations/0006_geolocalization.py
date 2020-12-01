# Written by Sebastian Betancourt

from django.contrib.postgres import operations
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0005_persona_edad'),
    ]

    operations = [
        operations.CreateExtension('postgis')
    ]
