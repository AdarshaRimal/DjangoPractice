# Generated by Django 5.1.1 on 2024-12-20 15:55

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_alter_collection_featured_product_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="store.cart",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="cartitem",
            unique_together={("cart", "product")},
        ),
    ]