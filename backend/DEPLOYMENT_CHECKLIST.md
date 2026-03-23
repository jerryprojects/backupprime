# Production Deployment Checklist

Use this checklist when deploying to production.

## Pre-Deployment

- [ ] All tests passing: `python manage.py test`
- [ ] No unused imports or models
- [ ] All migrations created: `python manage.py makemigrations`
- [ ] All migrations applied: `python manage.py migrate`
- [ ] Database backed up
- [ ] Code committed to git

## Environment Configuration

- [ ] Create `.env` file with production values
- [ ] Generate strong `SECRET_KEY`
- [ ] Set `DEBUG = False`
- [ ] Update `ALLOWED_HOSTS` with domain(s)
- [ ] Update `CORS_ALLOWED_ORIGINS` with frontend domain
- [ ] Configure database connection (PostgreSQL recommended)
- [ ] Set up static files directory
- [ ] Set up media files directory
- [ ] Configure logging

## Database Setup

- [ ] PostgreSQL or MySQL installed
- [ ] Database created
- [ ] Database user created with proper permissions
- [ ] Backup system configured
- [ ] Auto-backup scheduled

## Security

- [ ] Enable HTTPS/SSL certificate
- [ ] Set `SECURE_SSL_REDIRECT = True`
- [ ] Set `SESSION_COOKIE_SECURE = True`
- [ ] Set `CSRF_COOKIE_SECURE = True`
- [ ] Review all security settings in Django docs
- [ ] Set strong database password
- [ ] Update ALLOWED_HOSTS (no wildcards)
- [ ] Configure firewall rules
- [ ] Set up rate limiting (optional)

## Server Setup

- [ ] Server OS updated and patched
- [ ] Python 3.8+ installed
- [ ] pip and virtualenv installed
- [ ] Create and activate virtual environment
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create non-root user for running app
- [ ] Set proper file permissions

## Application Deployment

- [ ] Clone/pull latest code
- [ ] Install dependencies in virtual environment
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Test local runserver works

## Web Server Setup (Gunicorn + Nginx)

### Gunicorn
- [ ] Install Gunicorn: `pip install gunicorn`
- [ ] Test with: `gunicorn config.wsgi:application --bind 0.0.0.0:8000`
- [ ] Create systemd service file for auto-start
- [ ] Enable and start service

### Nginx
- [ ] Install Nginx
- [ ] Create nginx config
- [ ] Configure as reverse proxy to Gunicorn
- [ ] Enable and start service
- [ ] Test with curl

### Supervisor (Optional)
- [ ] Install Supervisor
- [ ] Create program configuration
- [ ] Test process monitoring

## Performance

- [ ] Enable database connection pooling
- [ ] Configure caching (Redis recommended)
- [ ] Set up CDN for static files (optional)
- [ ] Enable gzip compression
- [ ] Configure database indexes
- [ ] Set up monitoring/alerts

## Monitoring & Logging

- [ ] Configure logging to file
- [ ] Set up log rotation
- [ ] Configure monitoring (New Relic, DataDog, etc.)
- [ ] Set up uptime monitoring
- [ ] Configure error tracking (Sentry, etc.)
- [ ] Set up performance monitoring
- [ ] Configure database backup verification

## Backups

- [ ] Automated daily backups configured
- [ ] Backup storage off-server
- [ ] Test restore procedure
- [ ] Document backup location and procedure
- [ ] Set up backup alerts

## Final Testing

- [ ] Test all API endpoints
- [ ] Test authentication flow
- [ ] Test file uploads
- [ ] Test email functionality (if applicable)
- [ ] Stress test with load testing
- [ ] Test from different geographic locations
- [ ] Test with different devices/browsers
- [ ] Load test with ApacheBench or similar

## Post-Deployment

- [ ] Create superuser account
- [ ] Test with test data
- [ ] Verify logging is working
- [ ] Monitor error logs
- [ ] Monitor application performance
- [ ] Set up regular backup verification
- [ ] Document deployment procedure
- [ ] Create rollback procedure
- [ ] Set up monitoring alerts

## DNS & SSL

- [ ] DNS records point to server
- [ ] SSL certificate installed and valid
- [ ] Auto-renewal configured (Let's Encrypt recommended)
- [ ] Force HTTPS redirect working

## Documentation

- [ ] Document deployment steps
- [ ] Document environment variables
- [ ] Create troubleshooting guide
- [ ] Create recovery procedures
- [ ] Document backup procedures
- [ ] Keep contact information for support

## Maintenance

- [ ] Schedule regular database maintenance
- [ ] Schedule regular security updates
- [ ] Schedule backup verification
- [ ] Monitor disk space
- [ ] Monitor system resources
- [ ] Review logs regularly
- [ ] Update dependencies monthly

## Scaling (If Needed)

- [ ] Set up load balancer
- [ ] Configure multiple application servers
- [ ] Set up database replication
- [ ] Configure cache layer (Redis)
- [ ] Set up CDN for static files
- [ ] Monitor and optimize under load

## Quick Deployment Command

```bash
# 1. Pull latest code
git pull origin main

# 2. Activate environment
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Collect static files
python manage.py collectstatic --noinput

# 6. Restart application server
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## Rollback Procedure

```bash
# 1. Backup current database
pg_dump production_db > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Checkout previous version
git checkout previous_commit

# 3. Install dependencies (if changed)
pip install -r requirements.txt

# 4. Run any migrations backwards
python manage.py migrate api 0N  # where N is the migration number

# 5. Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# 6. Monitor error logs
tail -f /var/log/django/error.log
```

## Emergency Contacts

- DevOps/System Admin: _______________
- Database Admin: _______________
- Security Officer: _______________
- Application Owner: _______________

---

✅ Complete this checklist before going live!
