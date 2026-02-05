#!/usr/bin/env python3
"""
Database migration script to rename password_hash to password
Run this if you get errors creating users after updating the code
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import text, inspect
from app.database import engine, SessionLocal

def migrate():
    """Rename password_hash column to password if it exists"""
    print("Starting database migration...")
    
    try:
        # Create a connection
        with engine.connect() as conn:
            # Check if password_hash column exists
            inspector = inspect(engine)
            columns = [col['name'] for col in inspector.get_columns('users')]
            
            print(f"Current columns in users table: {columns}")
            
            if 'password_hash' in columns and 'password' not in columns:
                print("Found password_hash column, renaming to password...")
                
                # Rename column
                conn.execute(text(
                    "ALTER TABLE users CHANGE COLUMN password_hash password VARCHAR(255) NOT NULL"
                ))
                conn.commit()
                
                print("✓ Migration successful! Column renamed from password_hash to password")
                return True
                
            elif 'password' in columns:
                print("✓ Database already migrated - password column exists")
                return True
                
            else:
                print("✗ Error: Neither password_hash nor password column found!")
                return False
                
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrate()
    sys.exit(0 if success else 1)
