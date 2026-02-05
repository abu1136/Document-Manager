# Quick Fix Guide - 401 Unauthorized Errors

## Problem
You're getting 401 Unauthorized errors and JWT key length warnings even after pulling the latest code.

## Root Cause
The Docker container needs to be **rebuilt**, not just restarted, to pick up the code changes.

## Solution

### Step 1: Stop and rebuild containers
```bash
cd ~/test/Document-Manager  # or wherever your project is
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Step 2: Check the logs to verify the fix
```bash
docker-compose logs backend | grep "InsecureKeyLengthWarning"
```

You should **NOT** see the warning anymore. If you still see it, the old image is cached.

### Step 3: Force remove old images and rebuild
If the warning persists:
```bash
docker-compose down
docker rmi document-manager-backend  # Remove old image
docker-compose build --no-cache
docker-compose up -d
```

### Step 4: Clear browser cache and login
1. Open browser DevTools (F12)
2. Go to Application tab → Local Storage
3. Clear all entries for your domain
4. Navigate to http://localhost:8000/ui/login.html
5. Login with your admin credentials

## Verification

After rebuilding, you should see:
- ✅ No JWT key length warnings in logs
- ✅ Successful login (200 OK)
- ✅ Admin endpoints working (200 OK, not 401)

Example of correct logs:
```
backend-1  | INFO:     Started server process [1]
backend-1  | INFO:     Application startup complete.
backend-1  | INFO:     192.168.2.2:xxxxx - "POST /auth/login HTTP/1.1" 200 OK
backend-1  | INFO:     192.168.2.2:xxxxx - "GET /admin/users HTTP/1.1" 200 OK
```

## Why Restart Doesn't Work

- `docker-compose restart` only restarts the container with the existing image
- The code is baked into the Docker image during `docker-compose build`
- You must rebuild to get code changes

## Still Having Issues?

If you still get 401 errors after rebuilding:

1. Check environment variable is set:
   ```bash
   docker-compose exec backend printenv JWT_SECRET
   ```
   Should show: `supersecret_change_in_production_min32chars`

2. Verify the backend is using the correct secret:
   ```bash
   docker-compose exec backend python -c "import os; print('JWT_SECRET:', os.getenv('JWT_SECRET'))"
   ```

3. Check if there are multiple Python processes:
   ```bash
   docker-compose exec backend ps aux
   ```
   Should only see one uvicorn process.
