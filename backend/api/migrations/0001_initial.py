# Generated migration file - initial schema

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('student', 'Student'), ('faculty', 'Faculty'), ('admin', 'Admin')], default='student', max_length=10)),
                ('bio', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.CharField(default=lambda: f'proj-{uuid.uuid4().hex[:8]}', editable=False, max_length=50, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('abstract', models.TextField()),
                ('domains', models.JSONField(default=list, help_text='List of project domains/categories')),
                ('year', models.CharField(help_text='Academic year (e.g., 2024-25)', max_length=20)),
                ('license', models.CharField(blank=True, max_length=100)),
                ('tech_stack', models.JSONField(default=list, help_text='List of technologies used')),
                ('status', models.CharField(choices=[('public', 'Public'), ('locked', 'Locked'), ('approved', 'Approved')], default='public', max_length=20)),
                ('approval_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_projects', to='auth.user')),
                ('approved_faculty', models.ManyToManyField(blank=True, help_text='Faculty members with access to this project', related_name='approved_projects', to='auth.user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.CharField(default=lambda: f'tm-{uuid.uuid4().hex[:8]}', editable=False, max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('contribution', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_members', to='api.project')),
            ],
            options={
                'unique_together': {('project', 'email')},
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.CharField(default=lambda: f'notif-{uuid.uuid4().hex[:8]}', editable=False, max_length=50, primary_key=True, serialize=False)),
                ('notification_type', models.CharField(choices=[('access_request', 'Access Request'), ('access_granted', 'Access Granted'), ('project_updated', 'Project Updated'), ('team_member_added', 'Team Member Added'), ('admin_message', 'Admin Message')], max_length=50)),
                ('title', models.CharField(max_length=500)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('related_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='auth.user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AccessRequest',
            fields=[
                ('id', models.CharField(default=lambda: f'ar-{uuid.uuid4().hex[:8]}', editable=False, max_length=50, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('granted', 'Granted'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('responded_at', models.DateTimeField(blank=True, null=True)),
                ('response_message', models.TextField(blank=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access_requests', to='api.project')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access_requests', to='auth.user')),
            ],
            options={
                'ordering': ['-requested_at'],
                'unique_together': {('project', 'requester')},
            },
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['-created_at'], name='api_project_created_idx'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['status'], name='api_project_status_idx'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['owner'], name='api_project_owner_idx'),
        ),
    ]
