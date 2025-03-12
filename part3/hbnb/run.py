from app import create_app
from app.db_init import init_db
import os

app = create_app('development')

# Initialize the database
with app.app_context():
    init_db(app)

if __name__ == '__main__':
    app.run(port=5001) 