# build.sh
echo "Starting application..."
pip install -r requirements.txt
python manage.py collectstatic --no-input
ls -la /opt/render/project/src/Pikt/staticfiles
ls -la /opt/render/project/src/Pikt/staticfiles