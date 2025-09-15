# SECURITY: DEBUG must always be False in production
# SECURITY: CSRF and Session cookies are marked secure to enforce HTTPS
# SECURITY: CSP limits resources to trusted domains only
 HTTPS enforced with SECURE_SSL_REDIRECT
- HSTS enabled for 1 year with preload
- Cookies secured with SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE
- X_FRAME_OPTIONS set to DENY (prevents clickjacking)
- SECURE_BROWSER_XSS_FILTER and SECURE_CONTENT_TYPE_NOSNIFF enabled
- CSRF tokens included in all forms
- ORM used for database queries (avoiding SQL injection)