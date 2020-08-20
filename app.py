import base64
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hash_gen

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///code.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class Code(db.Model):
    __tablename__ = 'main'
    id = db.Column(db.Integer, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    hash = db.Column(db.String(300), nullable=False, primary_key=True)
    code = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)
    language = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Code %r>' % self.hash


class Images(db.Model):
    __tablename__ = 'images'
    img_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    depend_id = db.Column(db.Integer, db.ForeignKey('main.id'))
    image = db.Column(db.BLOB, nullable=True)
    # добавить колонку делитед для того чтобы определять будет ли пикча отображаться после фильтеред или нет

    def __repr__(self):
        return '<Images %r>' % self.depend_id


@application.route('/')
@application.route('/home')
def show_hello_page():
    return render_template('home.html')


@application.route('/about')
def show_about_page():
    return render_template('about.html')


@application.route('/code/<string:hash>/update', methods=['POST', 'GET'])
def code_update(hash):
    listOfImages = []
    code = Code.query.get(hash)
    image = Images.query.filter_by(depend_id=code.id).all()
    if request.method == 'POST':
        try:
            code.code = request.form['code']
            #code.description = request.form['description'] отключил из-за того что нужно верстать и определяться как читать файлы и картинки
            #image.image = request.form['image']
        except:
            return redirect('/add_code')

        try:
            db.session.commit()
            return redirect('/code/{}/update'.format(code.hash))
        except:
            return "Code editing error."

    else:
        if image[0].image != b'':
            for elem in image:
                encoded_image = base64.b64encode(elem.image).decode()
                listOfImages.append("data:image/png;base64,{encoded_image}".format(encoded_image=encoded_image))
        return render_template("code_update.html", code=code, code_pic=enumerate(listOfImages), lenList=len(listOfImages))


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
        # description = request.form['description']
        images = request.files.getlist('file')

        count = len(Code.query.all()) - 1
        hash = hash_gen.hash_password(count)
        text = request.form['description']

        codeAdd = Code(id=count + 1, name=name, code=code, hash=hash, description=text, language="Python")
        # codeAdd = Code(name=name, code=code, hash=hash, description=description)
        try:
            for image in images:
                imageAdd = Images(depend_id=codeAdd.id, image=image.read())
                print("#", end="")
                count += 1
                db.session.add(imageAdd)
                print("#", end="")
                db.session.commit()

            db.session.add(codeAdd)
            db.session.commit()

            return redirect('/code/{}/update'.format(codeAdd.hash))
        except:
            return "Code adding error."
    else:
        return render_template('add_code.html')


if __name__ == "__main__":
    # application.run(host='0.0.0.0', debug=False)
    application.run(debug=True)
