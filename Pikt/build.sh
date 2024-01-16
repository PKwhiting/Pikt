# build.sh
echo "Starting application..."
python manage.py collectstatic --no-input
ls -la /opt/render/project/src/Pikt/staticfiles
gunicorn Pikt.wsgi:application --bind 0.0.0.0:10000
ls -la /opt/render/project/src/Pikt/staticfiles