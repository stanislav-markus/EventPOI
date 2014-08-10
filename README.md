EventPOI
========

EventPOI is a place to share your Points Of Interest

sudo -u postgres dropdb eventpoi_db
sudo -u postgres createdb -T template_postgis -O eventpoi_user eventpoi_db
python manage.py syncdb

python manage.py migrate photologue
python manage.py migrate core
python manage.py migrate tastypie

rm public/cache/cache.json

python manage.py upload_data
