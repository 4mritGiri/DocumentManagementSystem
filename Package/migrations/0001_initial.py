# Generated by Django 5.0 on 2023-12-31 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('branch_code', models.CharField(max_length=60)),
                ('branch_name', models.CharField(max_length=110)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('doc_id', models.AutoField(primary_key=True, serialize=False)),
                ('doc_classification_type', models.CharField(choices=[('Normal', 'Normal'), ('Classified', 'Classified')], default='Normal', max_length=90)),
                ('doc_type', models.CharField(choices=[('Vouchers', 'Vouchers'), ('Cheques', 'Cheques'), ('Client File', 'Client File'), ('Demand Draft', 'Demand Draft'), ('Guarantee', 'Guarantee'), ('Contracts', 'Contracts')], default='Vouchers', max_length=90)),
                ('doc_details', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RoomRackCompartment',
            fields=[
                ('room_rack_compartment_id', models.AutoField(primary_key=True, serialize=False)),
                ('room', models.CharField(max_length=90)),
                ('rack', models.CharField(max_length=90)),
                ('compartment', models.CharField(max_length=90)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('store_id', models.AutoField(primary_key=True, serialize=False)),
                ('store_name', models.CharField(max_length=90)),
                ('store_location', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('pkg_id', models.AutoField(primary_key=True, serialize=False)),
                ('pkg_name', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('packaging_size', models.CharField(choices=[('Box size 1', 'Box size 1'), ('Box size 2', 'Box size 2'), ('Plastic Bag', 'Plastic Bag')], default='Box size 1', max_length=90)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=90)),
                ('destruction_eligible_time', models.CharField(choices=[('1 Year', '1 Year'), ('2 Years', '2 Years'), ('3 Years', '3 Years'), ('4 Years', '4 Years'), ('5 Years', '5 Years'), ('6 Years', '6 Years'), ('7 Years', '7 Years'), ('8 Years', '8 Years')], default='1 Year', max_length=90)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Package.branch')),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Package.document')),
                ('store_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Package.roomrackcompartment')),
            ],
        ),
        migrations.CreateModel(
            name='PackageVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorizer', models.CharField(max_length=90)),
                ('verification_remarks', models.TextField()),
                ('verification_date', models.DateTimeField(auto_now_add=True)),
                ('package_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Package.package')),
            ],
        ),
        migrations.AddField(
            model_name='roomrackcompartment',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Package.store'),
        ),
    ]
