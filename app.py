
from flask import Flask
from website.views import main_blueprint

app = Flask(__name__, template_folder="website/templates")

# Register blueprint for routes
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)