from enum import unique
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, current_user, login_required
from flask_security.forms import RegisterForm
from wtforms import StringField, TextAreaField
from flask_wtf import FlaskForm
from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy


from wtforms.fields.simple import TextAreaField

app = Flask(__name__)

# Connection credentials
db_user = 'root'
db_pass = 'root'
db_name = 'flask'

# configuring our database uri
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@10.0.0.4:32000/{}".format(db_user, db_pass, db_name)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'somesaltfortheforum'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False



sql_run = """
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "alembic_version" (
	"version_num"	VARCHAR(32) NOT NULL,
	CONSTRAINT "alembic_version_pkc" PRIMARY KEY("version_num")
);
CREATE TABLE IF NOT EXISTS "role" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(80),
	"description"	VARCHAR(250),
	UNIQUE("name"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"email"	VARCHAR(255),
	"password"	VARCHAR(255),
	"name"	VARCHAR(255),
	"username"	VARCHAR(255),
	"active"	BOOLEAN,
	"confirmed_at"	DATETIME,
	UNIQUE("username"),
	UNIQUE("email"),
	CHECK("active" IN (0, 1)),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "roles_users" (
	"user_id"	INTEGER,
	"role_id"	INTEGER,
	FOREIGN KEY("role_id") REFERENCES "role"("id"),
	FOREIGN KEY("user_id") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "thread" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR(30),
	"description"	VARCHAR(200),
	"date_created"	DATETIME NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "reply" (
	"id"	INTEGER NOT NULL,
	"thread_id"	INTEGER,
	"user_id"	INTEGER,
	"message"	VARCHAR(200),
	"date_created"	DATETIME,
	FOREIGN KEY("thread_id") REFERENCES "thread"("id"),
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
INSERT INTO "alembic_version" ("version_num") VALUES ('438e5072aa7c');
INSERT INTO "user" ("id","email","password","name","username","active","confirmed_at") VALUES (1,'marwane.adala@supcom.tn','$2b$12$H40G.UVZ9i7k4KlsVvzRT.QH2dw/xAKv52EW.tHcO5/gc.GVq3hLC','MARWANE ADALA','maadac',1,NULL);
INSERT INTO "thread" ("id","title","description","date_created") VALUES (1,'Helllo more','more is gone','2021-11-21 13:45:32.509301'),
 (2,'greetings','hello again','2021-11-21 14:39:07.564067'),
 (3,'first comment','this is a comment for you','2021-11-21 15:18:16.011170'),
 (4,'test','just  a test','2021-11-21 15:22:58.764268'),
 (5,'another thread','test laast thread','2021-11-21 16:35:05.722422'),
 (6,'last test','this is the last test here','2021-11-21 19:50:47.236858');
INSERT INTO "reply" ("id","thread_id","user_id","message","date_created") VALUES (1,1,1,'this is the first message','2021-11-21 16:10:11.613918'),
 (2,1,1,'this is the first message','2021-11-21 16:18:05.878590'),
 (3,1,1,'this is the first message','2021-11-21 16:23:25.503527'),
 (4,1,1,'this is the first message','2021-11-21 16:26:21.178831'),
 (5,1,1,'Here you find another reply for me for this life
','2021-11-21 16:28:01.804839'),
 (6,5,1,'test retest test','2021-11-21 16:35:31.904890'),
 (7,6,1,'Hello, thank for these tests','2021-11-21 19:51:04.256607'),
 (8,6,1,'Youa are welcome, don''t worry!!!','2021-11-21 19:51:18.451327');
COMMIT;

"""


# basic model
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# db.engine.execute(sql_run)
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')) 
    
    )

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(250))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, 
                                backref=db.backref('users', lazy='dynamic'))
    replies = db.relationship('Reply', backref='user', lazy='dynamic')


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(200))
    date_created = db.Column(db.DateTime())

    replies = db.relationship('Reply', backref='thread', lazy='dynamic')
    def last_post_date(self):
        last_reply = Reply.query.filter_by(thread_id=self.id).order_by(Reply.id.desc()).first()
        if last_reply:
            return last_reply.date_created
        return self.date_created


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(200))
    date_created =db.Column(db.DateTime())

class ExtendRegisterForm(RegisterForm):
    name = StringField('Name')
    username = StringField('Username')


class NewThread(FlaskForm):
    title = StringField('Title')
    description = StringField('Description')

class NewReply(FlaskForm):
    message = TextAreaField('Message')

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form = ExtendRegisterForm)



@app.route('/', methods=['GET', 'POST'])
 
def index():
    form = NewThread()
    if form.validate_on_submit():
        #return 'Title: {}, Description: {}'.format(form.title.data, form.description.data)

        new_thread = Thread(title=form.title.data, description=form.description.data, 
                            date_created=datetime.now())
        db.session.add(new_thread)
        db.session.commit()

    threads = Thread.query.all()




    return render_template('index.html', form=form, threads=threads, current_user=current_user)

@app.route('/profile')
@login_required
def profile():
    #user = User.query.filter_by(id=current_user.id)
    return render_template('profile.html', current_user=current_user)

@app.route('/thread/<thread_id>', methods=['GET', 'POST'])

def thread(thread_id):
    form = NewReply() 
    thread = Thread.query.get(int(thread_id))

    if form.validate_on_submit():
        reply = Reply(user_id=current_user.id, message=form.message.data, date_created=datetime.now())
        thread.replies.append(reply)
        db.session.commit()
    replies = Reply.query.filter_by(thread_id=thread_id).all()
        
    return render_template('thread.html', thread=thread, form=form, replies=replies, current_user=current_user)


if __name__ == '__main__':
   app.run("0.0.0.0", port=80)
