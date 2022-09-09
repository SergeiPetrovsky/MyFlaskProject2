from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///art_photo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Article %r>' % self.id


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    url = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Photo %r>' % self.id

class Advert(db.Model):         # объявления
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Photo %r>' % self.id

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контакты')
@app.route('/documents')
def documents():
    return render_template('documents.html', title='Регистрационные документы')


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Главная')

@app.route('/about')
def about():
    return render_template('about.html', title='О проекте')

#___________________________________С Т А Т Ь И_____________________________________

@app.route('/post-create', methods=['POST','GET'])
def post_create():
    if request.method == "POST":
        if request.form['password'] == 'coldwater':
            title = request.form['title']
            intro = request.form['intro']
            text = request.form['text']

            article = Article(title=title, intro=intro, text=text)
            try:
                db.session.add(article)
                db.session.commit()
                return redirect('/posts')
            except:
                return 'При добавлении статьи произошла ошибка'
        else:
            return 'Вы не можете добавлять статьи на этом сайте'

    else:
        return render_template('post-create.html', title='Создание статьи')

@app.route('/posts')
def posts():
    articles = Article.query.order_by(desc(Article.date)).all()
    return render_template('posts.html', title='Статьи', articles=articles)

@app.route('/post-detail/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)

@app.route('/posts-admin')
def posts_admin():
    articles = Article.query.order_by(desc(Article.date)).all()
    return render_template('posts_admin.html', title='Статьи', articles=articles)

@app.route('/post-delete/<int:id>', methods=['POST','GET'])
def post_delete(id):
    article = Article.query.get(id)
    if request.method == "POST":
        if request.form['password'] == 'coldwater':
            try:
                db.session.delete(article)
                db.session.commit()
                return redirect('/posts')
            except:
                return 'При удалении возникла ошибка'
        else:
            return 'У вас нет доступа для удаления статей на этом сайте'

    else:
        return render_template('auth.html',title='Удаление статьи', article=article)


@app.route('/post-edit/<int:id>', methods=['POST','GET'])
def post_edit(id):
    article = Article.query.get(id)
    if request.method == "POST":
        if request.form['password'] == 'coldwater':

            article.title = request.form['title']
            article.intro = request.form['intro']
            article.text = request.form['text']
            try:
                db.session.commit()

                return render_template('post_detail.html', article=article)
            except:
                return 'При редактировании статьи произошла ошибка'
        else:
            return 'У вас нет доступа к редактированию статей на этом сайте'

    else:
        return render_template('post_edit.html', article=article)



@app.route('/photo')
def photo():
    photos = Photo.query.order_by(desc(Photo.date)).all()
    return render_template('photo.html', title='Наши фото', photos=photos)

@app.route('/photo-admin')
def photo_admin():
    photos = Photo.query.order_by(desc(Photo.date)).all()
    return render_template('photo_admin.html', title='Наши фото', photos=photos)


@app.route('/photo-add', methods=['POST','GET'])
def photo_add():
    if request.method == "POST":
        title = request.form['title']
        url = request.form['url']

        photo = Photo(title=title, url=url)
        try:
            db.session.add(photo)
            db.session.commit()
            return redirect('/photo')
        except:
            return 'При добавлении фотографии произошла ошибка'

    else:
        return render_template('photo_add.html', title='Добавление фото')

@app.route('/photo-delete/<int:id>', methods=['POST','GET'])  #################################################################
def photo_delete(id):
    photo = Photo.query.get(id)
    if request.method == "POST":
        if request.form['password'] == 'coldwater':
            try:
                db.session.delete(photo)
                db.session.commit()
                return redirect('/photo')
            except:
                return 'При удалении возникла ошибка'
        else:
            return 'У вас нет доступа для удаления фото на этом сайте'

    else:
        return render_template('auth.html', title='Удаление фото', photo=photo)


@app.route('/calendar')   # календарь событий
def calendar():
    return render_template('calendar.html')


#____________________________ О Б Ъ Я В Л Е Н И Я ______________________________
@app.route('/advert')
def advert():
    adverts = Advert.query.order_by(desc(Advert.date)).all()
    return render_template('advert.html',title='Объявления', adverts=adverts)

@app.route('/advert-admin')
def advert_admin():
    adverts = Advert.query.order_by(desc(Advert.date)).all()
    return render_template('advert_admin.html',title='Объявления', adverts=adverts)

@app.route('/advert-create', methods=['POST','GET'])
def advert_create():
    if request.method == "POST":
        if request.form['password'] == 'coldwater':
            title = request.form['title']
            text = request.form['text']
            advert = Advert(title=title, text=text)
            try:
                db.session.add(advert)
                db.session.commit()
                return redirect('/advert')
            except:
                return 'При добавлении  произошла ошибка'
        else:
            return 'Вы не можете добавлять объявления на этом сайте'

    else:
        return render_template('advert_create.html', title='Создание объявления')

@app.route('/advert-delete/<int:id>', methods=['POST','GET'])
def advert_delete(id):
    advert = Advert.query.get(id)
    if request.method == "POST":
        if request.form['password'] == 'coldwater':
            try:
                db.session.delete(advert)
                db.session.commit()
                return redirect('/advert')
            except:
                return 'При удалении возникла ошибка'
        else:
            return 'У вас нет доступа для удаления объявлений на этом сайте'

    else:
        return render_template('auth.html', title='Удаление объявления', advert=advert)


@app.route('/advert-edit/<int:id>', methods=['POST','GET'])
def advert_edit(id):
    advert = Advert.query.get(id)
    if request.method == "POST":
        if request.form['password'] == 'coldwater':
            advert.title = request.form['title']
            advert.text = request.form['text']
            try:
                db.session.commit()
                return redirect('/advert')

            except:
                return 'При редактировании  произошла ошибка'
        else:
            return 'У вас нет доступа к редактированию  на этом сайте'

    else:
        return render_template('advert_edit.html', advert=advert)





if __name__ == '__main__':
    app.run(debug=True)
