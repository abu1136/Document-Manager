# Database Migration Guide

## Issue: Unable to Create Users

If you're experiencing errors when trying to create users after updating the codebase, this is due to a database schema change.

### Root Cause

The database column name was changed from `password_hash` to `password` for consistency. If your database was created before this update, it still has the old column name, causing errors when the code tries to write to the new column name.

### Symptoms

- Creating users fails with a database error
- Error message about missing column or field
- Admin user creation works, but regular user creation fails

### Solution 1: Run Migration Script (Recommended)

This preserves all your existing data.

#### Using Docker:
```bash
docker-compose exec backend python migrate_database.py
```

#### Manual Installation:
```bash
cd backend
python migrate_database.py
```

#### Expected Output:
```
Starting database migration...
Current columns in users table: ['id', 'username', 'password_hash', 'role', 'created_at']
Found password_hash column, renaming to password...
✓ Migration successful! Column renamed from password_hash to password
```

If already migrated:
```
Starting database migration...
Current columns in users table: ['id', 'username', 'password', 'role', 'created_at']
✓ Database already migrated - password column exists
```

### Solution 2: Recreate Database (⚠️ Deletes All Data)

If you don't need to preserve existing data:

#### Using Docker:
```bash
docker-compose down -v
docker-compose up -d
```

#### Manual Installation:
```bash
mysql -u root -p -e "DROP DATABASE IF EXISTS document_manager;"
mysql -u root -p < sql/init.sql
```

### Verify the Fix

1. Access the admin dashboard at `http://localhost:8000/ui/admin.html`
2. Navigate to "Users" page
3. Try creating a new user
4. You should see: "User created successfully"

### Technical Details

**What the migration does:**
```sql
ALTER TABLE users CHANGE COLUMN password_hash password VARCHAR(255) NOT NULL
```

**Changes made:**
- Old schema: `password_hash VARCHAR(255) NOT NULL`
- New schema: `password VARCHAR(255) NOT NULL`

The migration is:
- ✅ Safe to run multiple times
- ✅ Non-destructive (preserves data)
- ✅ Idempotent (same result if run repeatedly)
- ✅ Fast (executes instantly)

### Still Having Issues?

If the migration doesn't solve your problem:

1. Check database connectivity:
   ```bash
   docker-compose exec backend python -c "from app.database import engine; print(engine.connect())"
   ```

2. Check table structure:
   ```bash
   docker-compose exec mysql mysql -u docuser -pdocpass document_manager -e "DESCRIBE users;"
   ```

3. Check application logs:
   ```bash
   docker-compose logs backend
   ```

For additional help, see the [Troubleshooting section in README.md](README.md#troubleshooting).
