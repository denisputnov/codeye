from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///code.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)


class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    ## TODO: Add fields

    def __repr__(self):
        return '<Code %r>' % self.id


@application.route('/')
@application.route('/home')
def show_hello_page():
    return render_template('home.html')


@application.route('/code/<int:id>')
def show_code_page(id):
    code = Code.query.get(id)
    return render_template('code.html', code=code)


@application.route('/about')
def show_about_page():
    return render_template('about.html')


@application.route('/code/<int:id>/update', methods=['POST', 'GET'])
def code_update(id):
    code = Code.query.get(id)
    if request.method == 'POST':
        code.name = request.form['name']
        code.code = request.form['code']
        code.date = request.form['date']

        try:
            db.session.commit()
            return redirect("/code/<int:id>")
        except:
            return "Code editing error."

    else:
        return render_template("code_update.html", code=code)


@application.route('/code/<int:id>/delete', methods=['POST', 'GET'])
def code_delete(id):
    code = Code.query.get_or_404(id)

    try:
        db.session.delete(code)
        db.session.commit()
        return redirect("/home")
    except:
        return "Post deleting error."


@application.route('/add_code', methods=['POST', 'GET'])
def add_code():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        print(name, code)

        codeAdd = Code(name=name, code=code)
        print(codeAdd)
        try:
            db.session.add(codeAdd)
            db.session.commit()
            return redirect("/")
        except:
            return "Code adding error."
        # return redirect(f'/{id}')
    else:
        return render_template('add_code.html')


if __name__ == "__main__":
    application.run(debug=True)
