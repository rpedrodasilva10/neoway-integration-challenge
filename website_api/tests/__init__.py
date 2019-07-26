from website_api import create_app
from website_api.models import Company, db

app = create_app('config.DevConfig')
