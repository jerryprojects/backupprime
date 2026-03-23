#!/usr/bin/env python
"""
Complete backend initialization script
Running this will:
1. Create migrations
2. Run migrations
3. Create superuser
4. Load sample data
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))

django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
from api.models import UserProfile

def main():
    print("\n" + "="*60)
    print("PRIME BACKEND - INITIALIZATION SCRIPT")
    print("="*60 + "\n")
    
    # Step 1: Run migrations
    print("📦 Step 1: Running migrations...")
    try:
        call_command('migrate', verbosity=0)
        print("✅ Migrations completed\n")
    except Exception as e:
        print(f"❌ Migration error: {e}\n")
        return
    
    # Step 2: Create superuser
    print("👤 Step 2: Creating superuser...")
    if not User.objects.filter(username='admin').exists():
        try:
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("✅ Superuser created (admin/admin123)\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
    else:
        print("✅ Superuser already exists\n")
    
    # Step 3: Load sample data
    print("🎯 Step 3: Loading sample data...")
    try:
        call_command('load_sample_data', verbosity=0)
        print("✅ Sample data loaded\n")
    except Exception as e:
        print(f"⚠️  Note: Sample data loading - {e}\n")
    
    # Summary
    print("="*60)
    print("✅ INITIALIZATION COMPLETE!")
    print("="*60)
    print("\n📋 Next steps:\n")
    print("1. Start the server:")
    print("   python manage.py runserver\n")
    print("2. Access the API:")
    print("   http://localhost:8000/api/\n")
    print("3. Access admin panel:")
    print("   http://localhost:8000/admin/\n")
    print("4. Admin credentials:")
    print("   Username: admin")
    print("   Password: admin123\n")
    print("5. Sample users (after load_sample_data):")
    print("   - sarah/testpass123 (Student)")
    print("   - faculty_john/testpass123 (Faculty)")
    print("   - admin_user/testpass123 (Admin)\n")

if __name__ == '__main__':
    main()
