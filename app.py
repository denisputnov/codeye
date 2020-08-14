from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hash_gen

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///code.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)


class Code(db.Model):
    # id = db.Column(db.Integer)
    name = db.Column(db.String(100), nullable=False)
    hash = db.Column(db.String(300), nullable=False, primary_key=True)
    code = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    code_image = db.Column(db.BLOB, nullable=True)
    description = db.Column(db.Text, nullable=True)

    ## TODO: Add fields

    def __repr__(self):
        return '<Code %r>' % self.hash


@application.route('/')
@application.route('/home')
def show_hello_page():
    return render_template('home.html')


# @application.route('/code/<int:id>')
# def show_code_page(id):
#    code = Code.query.get(id)
#    return render_template('code.html', code=code)


@application.route('/about')
def show_about_page():
    return render_template('about.html')


@application.route('/code/<string:hash>/update', methods=['POST', 'GET'])
def code_update(hash):
    code = Code.query.get(hash)
    if request.method == 'POST':
        try:
            # code.name = request.form['name']
            code.code = request.form['code']
            ## такие же поля для добавления текста сбоку и картинок
            code.description = request.form['description']
        except:
            return redirect('/add_code')
            # render_template("add_code.html")
            # redirect('/code/{}/add_code')

        try:
            db.session.commit()
            return redirect('/code/{}/update'.format(code.hash))
        except:
            return "Code editing error."

    else:
        return render_template("code_update.html", code=code)


""""@application.route('/code/<string:hash>/delete', methods=['POST', 'GET'])
def code_delete(hash):
    code = Code.query.get_or_404(hash)

    try:
        db.session.delete(code)
        db.session.commit()
        return redirect("/home")
    except:
        return "Post deleting error."""""


@application.route('/add_code', methods=['POST', 'GET'])
def add_code():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']

        count = len(Code.query.all()) - 1
        print(count)
        # hash = request.form["{}".format(hash_gen.hash_password(count))]

        codeAdd = Code(name=name, code=code, hash=hash_gen.hash_password(count))
        # print(codeAdd.hash)
        try:
            db.session.add(codeAdd)
            print(1)
            db.session.commit()
            print(2)
            return redirect('/code/{}/update'.format(codeAdd.hash))
        except:
            return "Code adding error."
        # return redirect(f'/{id}')
    else:
        return render_template('add_code.html')


if __name__ == "__main__":
    application.run(debug=True)
