from flask import Flask
import os
from dotenv import load_dotenv
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.tables import tables_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(tables_bp)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )