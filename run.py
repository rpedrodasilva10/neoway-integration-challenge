from website_api import create_app

app = create_app('config.ProdConfig')

if __name__ == "__main__":
    app.run()
