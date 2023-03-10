# Generated by Django 3.2.15 on 2023-03-10 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0043_auto_20230310_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pay_method',
            field=models.CharField(choices=[('specify', 'Выяснить'), ('cash', 'Наличные'), ('card', 'Карта')], db_index=True, default='Выяснить', max_length=50, verbose_name='Способ оплаты'),
        ),
    ]
