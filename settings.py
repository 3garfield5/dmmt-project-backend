class Settings():
    AWS_ACCESS_KEY_ID = 'minioadmin'
    AWS_SECRET_ACCESS_KEY = 'minioadmin'
    AWS_REGION = 'us-east-1'
    AWS_HOST = 'http://localhost:9000'
    AWS_BUCKET = 'images'

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

settings = Settings()