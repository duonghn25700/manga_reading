from libs.lib import *
from utils.manga_db import *
from controller.beetoon import *
from manga_similar import *

app = Flask(__name__, template_folder="template")
app.config.from_pyfile("config.cfg")

CORS(app)
app.app_context().push()
mail=Mail(app)
api = Api(app)
s=URLSafeTimedSerializer(app.config["SECRET_KEY"])
port_id = 5689


@app.route("/send-verify", methods=["GET","POST"])
def confirmEmail():
    email = request.form['email']
    try:
        users = session.query(User_Info).\
                filter_by(email=email).first()
        
        if users.verified_at == "" or users.verified_at == None:
            token = s.dumps(email, salt="email-confirm")

            msg = Message('Confirm Email', 
            sender='duonghoangnguyen333@gmail.com', recipients=[email])
            
            link = url_for('confirm', token=token, external=True)

            msg.body = f'Your link is {link}'

            mail.send(msg)

            return jsonify(f"The email entered is {email}, token : {token}")
        else:
            return jsonify(f"this email was verified")
    except:
        session.rollback()
        raise
    finally:
        session.close()


@app.route("/confirm/<token>")
def confirm(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        now = datetime.now(tz)
        current_time = now.strftime("%Y/%m/%d %H:%M:%S")

        email = request.form["email"]
        users = session.query(User_Info).\
            filter_by(email=email).first()
        if users:
            if users.is_active == 1:
                users.verified_at = current_time
                session.commit()
                return {"message": f"Email confirmed!"}
            else:
                return {"message": f"Please login first"}
        else:
            return {"message": "Account Not Found"}, 404
    except Exception as err:
        print("Error's message ||||||| ",err)
        if "Signature age" in str(err):
            return 'the token is expired!'
        else:
            session.rollback()
            raise
    finally:
        session.close()


@app.route("/recommend/<int:manga_id>", methods=["GET", "POST"])
def recommend_manga(manga_id):
    manga = session.query(Manga).\
                filter_by(manga_id=manga_id).first()
    desc = manga.description
    data = get_similar_manga(desc, k=10)
    return jsonify({"data":data})


api.add_resource(GetManga, "/manga")
api.add_resource(MangaDetail, "/manga/<int:manga_id>")
api.add_resource(GetCategories, "/manga/categories")
api.add_resource(GetMangaByCategory, "/manga/categories/<int:category_id>")
api.add_resource(GetChapterByID, "/manga/<int:manga_id>/chapter")
api.add_resource(ChapterDetail, "/manga/<int:manga_id>/chapter/<int:chapter_id>")


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(UserInfo, "/info")
api.add_resource(ChangePassword, "/user/change-password")


api.add_resource(PostComment, "/manga/<int:manga_id>/comments")
api.add_resource(EditComment, "/manga/<int:manga_id>/comments/<int:comment_id>")
api.add_resource(EditFavorite, "/favorite/<int:manga_id>")
api.add_resource(FavoriteManga, "/favorite")

api.add_resource(Home, "/home")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port_id, debug=True)