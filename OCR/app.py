from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
db = SQLAlchemy(app)

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)

@app.route("/")
def main():
	return render_template('main.html')


@app.route("/result", methods=['POST'])
def result():
    img = request.files['pic']
        
    new_image = Images(name=img.filename, data=img.read())
    db.session.add(new_image)
    db.session.commit()

    return "Saved " + img.filename + " to the Database"

if __name__ == '__main__':
	app.run(debug=True)
