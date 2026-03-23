#!/usr/bin/env python
"""
Script to initialize the database with sample data and settings
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Project, TeamMember, UserProfile


def create_sample_data():
    """Create sample users and projects"""
    print("Creating sample data...")
    
    # Create users
    users = [
        ('sarah', 'sarah@university.edu', 'Sarah', 'Johnson', 'student'),
        ('mike', 'mike@university.edu', 'Mike', 'Chen', 'student'),
        ('emma', 'emma@university.edu', 'Emma', 'Davis', 'student'),
        ('faculty_john', 'john@university.edu', 'John', 'Smith', 'faculty'),
        ('admin_user', 'admin@university.edu', 'Admin', 'User', 'admin'),
    ]
    
    created_users = {}
    for username, email, first_name, last_name, role in users:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password='testpass123'
            )
            user.profile.role = role
            user.profile.save()
            created_users[username] = user
            print(f"✓ Created user: {username} ({role})")
        else:
            created_users[username] = User.objects.get(username=username)
    
    # Create projects
    projects = [
        {
            'title': 'AI-Powered Chatbot for Student Support',
            'abstract': 'An intelligent chatbot system using natural language processing to provide 24/7 student support.',
            'domains': ['AI', 'NLP'],
            'year': '2024-25',
            'license': 'MIT',
            'tech_stack': ['Python', 'TensorFlow', 'React', 'Node.js'],
            'status': 'public',
            'owner': 'sarah',
        },
        {
            'title': 'Smart Campus IoT System',
            'abstract': 'A comprehensive IoT solution for monitoring campus resources.',
            'domains': ['IoT', 'Hardware'],
            'year': '2023-24',
            'license': 'Apache 2.0',
            'tech_stack': ['Arduino', 'Raspberry Pi', 'MQTT'],
            'status': 'locked',
            'owner': 'mike',
        },
        {
            'title': 'Blockchain Certificate Verification',
            'abstract': 'Decentralized platform for academic certificate verification.',
            'domains': ['Blockchain', 'Web'],
            'year': '2024-25',
            'license': 'GPL-3.0',
            'tech_stack': ['Solidity', 'Ethereum', 'Web3.js'],
            'status': 'locked',
            'owner': 'sarah',
        },
    ]
    
    for proj_data in projects:
        owner = created_users[proj_data.pop('owner')]
        project, created = Project.objects.get_or_create(
            title=proj_data['title'],
            defaults={**proj_data, 'owner': owner}
        )
        if created:
            print(f"✓ Created project: {project.title}")
    
    print("\n✅ Sample data created successfully!")


if __name__ == '__main__':
    try:
        create_sample_data()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
