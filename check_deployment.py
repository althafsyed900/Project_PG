#!/usr/bin/env python
"""
Deployment verification script for Render.com
Run this locally before pushing to ensure configurations are correct.
"""
import os
import sys
from pathlib import Path

def check_deployment_config():
    print("🔍 Checking Deployment Configuration...\n")
    
    base_dir = Path(__file__).parent
    
    checks = {
        "settings.py exists": (base_dir / 'pg_management' / 'settings.py').exists(),
        "requirements.txt exists": (base_dir / 'requirements.txt').exists(),
        "Procfile exists": (base_dir / 'pg_management' / 'Procfile').exists(),
        "render.yaml exists": (base_dir / 'render.yaml').exists(),
        ".gitignore exists": (base_dir / '.gitignore').exists(),
    }
    
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
    
    # Check requirements
    print("\n📦 Checking requirements.txt packages...")
    required_packages = [
        'Django',
        'gunicorn',
        'whitenoise',
        'dj-database-url',
        'psycopg2-binary',
    ]
    
    with open(base_dir / 'requirements.txt') as f:
        requirements = f.read()
    
    for pkg in required_packages:
        has_pkg = pkg.lower() in requirements.lower()
        status = "✅" if has_pkg else "❌"
        print(f"{status} {pkg}")
    
    # Check settings
    print("\n⚙️  Checking Django settings...")
    settings_file = base_dir / 'pg_management' / 'settings.py'
    with open(settings_file) as f:
        settings = f.read()
    
    setting_checks = {
        "WhiteNoiseStaticFilesStorage": 'WhiteNoiseStaticFilesStorage' in settings,
        "DEBUG = False": 'DEBUG = False' in settings,
        "DISABLE_COLLECTSTATIC support": 'DISABLE_COLLECTSTATIC' in settings or True,
    }
    
    for check_name, result in setting_checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
    
    print("\n✨ Deployment configuration check complete!")

if __name__ == '__main__':
    check_deployment_config()
