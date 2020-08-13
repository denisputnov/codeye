from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code =  db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    ## TODO: Add fields

    def __repr__(self):
        return '<Code %r>' % self.id

@app.route('/')
def show_hello_page():
    return render_template('home.html')

@app.route('/<int:id>')
def show_code_page(id):
    code = Code.query.get(id)
    return render_template('code.html', code=code)
    

@app.route('/about')
def show_about_page():
    return render_template('about.html')

@app.route('/add_code', methods=['POST', 'GET'])
def show_add_code_page():
    if request.method == "POST":
        
        # TODO: Add db oberations
        pass
        # return redirect(f'/{id}')
    else:
        return render_template('add_code.html')


if __name__ == "__main__":
    app.run(debug=True)