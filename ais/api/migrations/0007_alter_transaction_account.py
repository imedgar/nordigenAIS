# Generated by Django 4.0.1 on 2022-01-10 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='account',
            field=models.ForeignKey(db_column='account_id', on_delete=django.db.models.deletion.CASCADE, to='api.account'),
        ),
    ]