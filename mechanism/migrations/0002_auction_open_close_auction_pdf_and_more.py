# Generated by Django 4.1.6 on 2023-03-04 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mechanism', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='open_close',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='auction',
            name='pdf',
            field=models.FileField(default=1, upload_to='Auction_pdf/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auction',
            name='saved_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bid',
            name='bail_trn_id',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='remaining_trn_id',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='bid',
            name='saved_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notification',
            name='purpose',
            field=models.CharField(choices=[('0', 'New Auction'), ('1', 'Outbid'), ('2', 'Auction Award'), ('3', 'New Like'), ('4', 'New Bid')], default='0', max_length=1),
        ),
    ]