import sys
sys.path.append("../libs")
from libs.lib import *
sys.path.append("../utils")
from utils.manga_db import *


def manga2block(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        data = f.readlines()
    new_list = [item.strip() for item in data if item.strip() != ""]
    return new_list
black_list = manga2block(txt_path)


def getAuthorInfo(author_list):
    for idx_, i in enumerate(author_list):
        authors = session.query(Authors).filter(Authors.name == i).all()
        for author in authors:
            author_dict = dict()
            author_dict["id"] = author.id
            author_dict["name"] = author.name
            author_list[idx_] = author_dict
    return author_list


def getCategoriesInfo(data):
    for idx_, i in enumerate(data):
        categories = session.query(Categories).filter(Categories.title == i).all()
        for category in categories:
            data_dict = dict()
            data_dict["id"] = category.id
            data_dict["name"] = category.title
            data[idx_] = data_dict
    return data


def getChapterInfobyID(manga_id):
    chapters = session.query(Chapters).filter(Chapters.manga_id == manga_id).all()
    alldata = list()
    for chapter in chapters:
        data = dict()
        # data['id'] = chapter.id
        data["manga_id"] = chapter.manga_id
        data["chapter_id"] = chapter.chapter_id
        data["manga_name"] = chapter.manga_name
        data["chapter_name"] = chapter.chapter_name
        data["thumbnail_count"] = chapter.thumbnail_count
        data["created_at"] = chapter.created_at
        data["updated_at"] = chapter.updated_at
        data["deleted_at"] = chapter.deleted_at
        alldata.append(data)
    return alldata
    

class GetManga(Resource):
    def get(self):
        try:
            page = request.args.get("page", 1, type=int)
            page_size = request.args.get("page_size", 36, type=int)
            start = (page - 1) * page_size
            end = start + page_size
            data_ = dict()
            manga_count = session.query(func.count(Manga.id)).scalar()
            # print(manga_count)
            mangas = (
                session.query(Manga)
                .filter(Manga.id > start, Manga.id <= end)
                .limit(page_size)
                .all()
            )

            result = []
            for manga in mangas:
                if manga.manga_name not in black_list:
                    author_list = manga.authors.split(",")
                    author_list = getAuthorInfo(author_list)
                    result.append(
                        {
                            "id": manga.id,
                            "manga_id": manga.manga_id,
                            "manga_name": manga.manga_name,
                            "authors": author_list,
                            "categories": manga.categories,
                            "thumbnail": manga.image,
                            "description": manga.description,
                            "rate": manga.rank,
                            "view": manga.view,
                            "slug": manga.slug,
                            "chapter_count": manga.chapter_count,
                            "status": manga.status,
                            "created_at": manga.created_at,
                            "release_at": manga.release_at,
                            "updated_at": manga.updated_at,
                        }
                    )
            meta_data = dict()
            meta_data["current"] = page
            meta_data["page_size"] = page_size
            meta_data["total_page"] = manga_count // page_size + 1

            data_["data"] = result
            data_["pagination"] = meta_data
            return jsonify(data_)
        except:
            session.rollback()
            raise
        finally:
            session.close()


class MangaDetail(Resource):
    def get(self, manga_id):
        try:
            manga = session.query(Manga).filter_by(manga_id=manga_id).first()
            if manga and manga.manga_name not in black_list:
                author_list = manga.authors.split(",")
                author_list = getAuthorInfo(author_list)

                categories_list = manga.categories.split(", ")
                categories_list = getCategoriesInfo(categories_list)

                return {
                    "id": manga.id,
                    "manga_id": manga.manga_id,
                    "manga_name": manga.manga_name,
                    "authors": author_list,
                    "categories": categories_list,
                    "thumbnail": manga.image,
                    "description": manga.description,
                    "rate": manga.rank,
                    "view": manga.view,
                    "slug": manga.slug,
                    "chapter_count": manga.chapter_count,
                    "chapters": getChapterInfobyID(manga_id),
                    "status": manga.status,
                    "created_at": manga.created_at,
                    "release_at": manga.release_at,
                    "updated_at": manga.updated_at,
                }
            else:
                return {"message": "Manga Not Found"}, 404
        except:
            session.rollback()
            raise
        finally:
            session.close()


class GetChapterByID(Resource):
    def get(self, manga_id):
        try:
            return {"data": getChapterInfobyID(manga_id)}
        except:
            session.rollback()
            raise
        finally:
            session.close()


class ChapterDetail(Resource):
    def get(self, manga_id, chapter_id):
        try:
            chapter_thumbnails = (
                session.query(Chapters_Detail)
                .filter_by(manga_id=manga_id, chapter_id=chapter_id)
                .all()
            )
            alldata = list()
            if chapter_thumbnails:
                data = dict()
                data["chapter_id"] = chapter_thumbnails[0].chapter_id
                data["chapter_name"] = chapter_thumbnails[0].chapter_name
                data["id"] = chapter_thumbnails[0].id
                thumbnails = list()
                for i, chapter in enumerate(chapter_thumbnails):
                    chapter_thumbnail = dict()
                    chapter_thumbnail["id"] = i + 1
                    chapter_thumbnail["url"] = chapter.thumbnail_url
                    thumbnails.append(chapter_thumbnail)
                data["thumbnails_url"] = thumbnails

                return jsonify({"data": data})
            else:
                return {"message": "Chapter Not Found"}, 404
        except:
            session.rollback()
            raise
        finally:
            session.close()


class UserRegister(Resource):
    def post(self):
        try:
            now = datetime.now(tz)
            current_time = now.strftime("%Y/%m/%d %H:%M:%S")

            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]

            users = session.query(User_Info).filter_by(username=username).first()
            if users:
                return {"message": f"{username} is already registed!"}
            else:
                user = User_Info(
                    username=username,
                    email=email,
                    password=password,
                    created_at=current_time,
                    updated_at=current_time,
                    provider="email",
                    is_active=0,
                )
                session.add(user)
                session.commit()
                return {"message": "Registed Successfully!"}
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get(self):
        try:
            return {
                "username": "Type here",
                "email": "Type here",
                "password": "Type here",
            }
        except:
            session.rollback()
            raise
        finally:
            session.close()


class UserLogin(Resource):
    def get(self):
        try:
            return {
                "username": "Type here",
                "email": "Type here",
                "password": "Type here",
            }
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def post(self):
        try:
            now = datetime.now(tz)
            current_time = now.strftime("%Y/%m/%d %H:%M:%S")

            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]

            users = session.query(User_Info).filter_by(username=username).first()
            if users:
                if (
                    users.username == username
                    and users.password == password
                    or users.email == email
                    and users.password == password
                ):
                    if users.is_active == 1:
                        return {"message": "username is already logged in!"}
                    else:
                        users.is_active = 1
                        session.commit()
                        return {"message": "Login successfully!"}
                else:
                    return {"message": "Wrong information"}
            else:
                return {"message": "Account Not Found"}, 404
        except:
            session.rollback()
            raise
        finally:
            session.close()


class UserLogout(Resource):
    def post(self):
        try:
            now = datetime.now(tz)
            current_time = now.strftime("%Y/%m/%d %H:%M:%S")

            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]

            users = session.query(User_Info).filter_by(username=username).first()
            if users:
                if users.is_active == 1:
                    users.is_active = 0
                    users.last_login = current_time
                    users.updated_at = current_time
                    session.commit()
                    return {"message": "logged out successfully!"}
                else:
                    return {"message": "please log in first"}
            else:
                return {"message": "Account Not Found"}, 404
        except:
            session.rollback()
            raise
        finally:
            session.close()


class PostComment(Resource):
    def get(self, manga_id):
        try:
            alldata = list()

            page = request.args.get("page", 1, type=int)
            page_size = request.args.get("page_size", 10, type=int)
            start = (page - 1) * page_size
            end = start + page_size

            comments = (
                session.query(Comments)
                .filter(Comments.comment_id > start, Comments.comment_id <= end)
                .limit(page_size)
                .all()
            )
            for comment in comments:
                data = dict()
                user_data = dict()

                users = session.query(User_Info).filter_by(id=comment.user_id).first()
                user_data["avatar"] = users.avatar
                user_data["email"] = users.email
                user_data["id"] = users.id
                user_data["is_active"] = users.is_active
                user_data["name"] = users.username
                user_data["phone number"] = users.phone_number
                user_data["last_login"] = users.last_login
                user_data["provider"] = users.provider

                data["content"] = comment.content
                data["comment_id"] = comment.comment_id
                data["manga_id"] = comment.manga_id
                data["updated_at"] = comment.updated_at
                data["created_at"] = comment.created_at
                data["user"] = user_data
                alldata.append(data)
            return jsonify({"data": alldata})
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def post(self, manga_id):
        try:
            now = datetime.now(tz)
            current_time = now.strftime("%Y/%m/%d %H:%M:%S")

            user_id = request.form["user_id"]
            content = request.form["content"]

            users = session.query(User_Info).filter_by(id=user_id).first()
            total_comment_count = session.query(
                func.count(Comments.comment_id)
            ).scalar()
            manga_check = session.query(Manga).filter_by(manga_id=manga_id).first()
            if manga_check:
                if users:
                    if users.is_active == 1:
                        comment = Comments(
                            comment_id=total_comment_count + 1,
                            manga_id=manga_id,
                            user_id=user_id,
                            parent_id="1",
                            content=content,
                            updated_at=current_time,
                            created_at=current_time,
                        )
                        session.add(comment)
                        session.commit()
                        return {"message": f"Comment: {content} is added"}
                    else:
                        return {"message": f"Please Log in first"}
                else:
                    return {"message": "Account Not Found"}, 404
            else:
                return {"message": "Manga Not Found"}, 404
        except:
            session.rollback()
            raise
        finally:
            session.close()


class EditComment(Resource):
    def put(self, manga_id, comment_id):
        try:
            content = request.form["content"]
            comment = (
                session.query(Comments)
                .filter_by(manga_id=manga_id, comment_id=comment_id)
                .first()
            )
            if comment:
                comment.content = content
                session.commit()
                return {"message": f"edit comment :{content} successfully"}
            else:
                return {"message": "Comment Not Found"}, 404
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def delete(self, manga_id, comment_id):
        try:
            comment = (
                session.query(Comments)
                .filter_by(manga_id=manga_id, comment_id=comment_id)
                .first()
            )
            if comment:
                session.delete(comment)
                session.commit()
                return {"message": f"Delete comment successfully"}
            else:
                return {"message": "Comment Not Found"}, 404
        except:
            session.rollback()
            raise
        finally:
            session.close()


class UserInfo(Resource):
    def get(self):
        try:
            username = request.form["username"]
            users = session.query(User_Info).filter_by(username=username).first()
            if users:
                data = dict()
                data["activated_at"] = None
                data["avatar"] = users.avatar
                data["created_at"] = users.created_at
                data["deleted_at"] = users.deleted_at
                data["email"] = users.email
                data["email_verified_at"] = users.verified_at
                data["id"] = users.id
                data["is_active"] = users.is_active
                data["last login"] = users.last_login
                data["name"] = users.username
                data["phone number"] = users.phone_number
                data["provider"] = users.provider
                data["updated_at"] = users.updated_at
                return jsonify({"data": data})
            else:
                return {"message": "User Not Found"}, 404
        except:
            session.rollback()
            raise
        finally:
            session.close()


class ChangePassword(Resource):
    def put(self):
        try:
            username = request.form["username"]
            old_password = request.form["old_password"]
            new_password = request.form["new_password"]
            users = session.query(User_Info).filter_by(username=username).first()
            if users:
                if old_password == users.password:
                    users.password = new_password
                    session.commit()
                    return {"message": "password has been changed"}
                else:
                    return {"message": "old password is wrong"}
            else:
                return {"message": "User Not Found"}, 404
        except:
            session.rollback()
            raise
        finally:
            session.close()


class EditFavorite(Resource):
    def post(self, manga_id):
        try:
            now = datetime.now(tz)
            current_time = now.strftime("%Y/%m/%d %H:%M:%S")

            username = request.form["username"]
            is_favorite = request.form["is_favorite"]
            users = session.query(User_Info).filter_by(username=username).first()
            # manga_count = session.query(func.count(Manga.manga_id)).scalar()
            manga_count = session.query(Manga).filter_by(manga_id=manga_id).first()
            if manga_count:
                if users:
                    if is_favorite == "1":
                        if users.favorite_manga == None:
                            fvmanga_list = []
                        else:
                            fvmanga_list = users.favorite_manga.split(",")
                        if str(manga_id) not in fvmanga_list:
                            fvmanga_list.append(str(manga_id))
                            fvmanga = ",".join(fvmanga_list)
                            users.favorite_manga = fvmanga
                            users.updated_at = current_time
                            session.commit()
                            return {
                                "message": f"This manga has added to your favorite {fvmanga}"
                            }
                        else:
                            return {"message": "This manga is already in your favorite"}
                    else:
                        if users.favorite_manga == None:
                            return jsonify("you dont have any favorite manga")
                        else:
                            fvmanga_list = users.favorite_manga.split(",")
                        if str(manga_id) not in fvmanga_list:
                            return {
                                "message": "You haven't add this manga to your favorite"
                            }
                        else:
                            fvmanga_list.pop(fvmanga_list.index(str(manga_id)))
                            fvmanga = ",".join(fvmanga_list)
                            users.favorite_manga = fvmanga
                            session.commit()
                            return {
                                "message": f"This manga is removed from your favorite {fvmanga}"
                            }

                        return {"message": "0"}
                else:
                    return {"message": "User Not Found"}, 404
            else:
                return {"message": f"Manga Not Found: {manga_count}"}, 404
        except:
            session.rollback()
            raise
        finally:
            session.close()


class FavoriteManga(Resource):
    def get(self):
        try:
            alldata = list()
            username = request.form["username"]
            users = session.query(User_Info).filter_by(username=username).first()
            
            if users.favorite_manga == None:
                return jsonify(f"you dont have any favorite manga")
            else:
                fvmanga_list = users.favorite_manga.split(",")

            for manga_id in fvmanga_list:
                if manga_id != "":
                    data = dict()
                    manga = session.query(Manga).filter_by(manga_id=int(manga_id)).first()
                    data["manga_id"] = manga.manga_id
                    data["manga_name"] = manga.manga_name
                    data["chapter_count"] = manga.chapter_count
                    data["description"] = manga.description
                    data["rank"] = manga.rank
                    data["view"] = manga.view
                    data["release_at"] = manga.release_at
                    alldata.append(data)
            return {"data": alldata}
        except:
            session.rollback()
            raise
        finally:
            session.close()


class GetCategories(Resource):
    def get(self):
        try:
            categories = session.query(Categories).all()
            alldata = list()
            for category in categories:
                data = dict()
                data["created_at"] = category.created_at
                data["id"] = category.category_id
                data["title"] = category.title
                data["total_manga"] = len(category.total_manga.split(","))
                data["updated_at"] = category.updated_at
                data["slug"] = category.slug
                alldata.append(data)
            return {"data": alldata}
        except:
            session.rollback()
            raise
        finally:
            session.close()


class GetMangaByCategory(Resource):
    def get(self, category_id):
        try:
            alldata = list()
            page = request.args.get("page", 1, type=int)
            page_size = request.args.get("page_size", 36, type=int)
            start = (page - 1) * page_size
            end = start + page_size

            categories = (
                session.query(Categories).filter_by(category_id=category_id).first()
            )
            for manga_id in categories.total_manga.split(",")[start : end + 1]:
                manga = session.query(Manga).filter_by(manga_id=manga_id).first()
                
                if manga.manga_name not in black_list:
                    author_list = manga.authors.split(",")
                    author_list = getAuthorInfo(author_list)

                    categories_list = manga.categories.split(", ")
                    categories_list = getCategoriesInfo(categories_list)

                    data = {
                        "id": manga.id,
                        "manga_id": manga.manga_id,
                        "manga_name": manga.manga_name,
                        "authors": author_list,
                        "categories": categories_list,
                        "thumbnail": manga.image,
                        "description": manga.description,
                        "rate": manga.rank,
                        "view": manga.view,
                        "slug": manga.slug,
                        "chapter_count": manga.chapter_count,
                        "status": manga.status,
                        "release_at": manga.release_at,
                        "updated_at": manga.updated_at,
                    }
                    alldata.append(data)

            total_manga = len(categories.total_manga.split(","))
            metadata = dict()
            metadata["current_page"] = page
            metadata["page_size"] = page_size
            metadata["total_manga"] = total_manga
            metadata["total_pages"] = total_manga // page_size + 1
            return {"data": alldata, "paginition": metadata}
        except:
            session.rollback()
            raise
        finally:
            session.close()


class Home(Resource):
    def get(self):
        try:
            page = request.args.get("page", 1, type=int)
            page_size = request.args.get("page_size", 36, type=int)
            start = (page - 1) * page_size
            end = start + page_size
            data_ = dict()
            manga_count = session.query(func.count(Manga.id)).scalar()
            # print(manga_count)
            mangas = (
                session.query(Manga)
                .filter(Manga.id > start, Manga.id <= end)
                .limit(page_size)
                .all()
            )

            result = []
            for manga in mangas:
                author_list = manga.authors.split(",")
                author_list = getAuthorInfo(author_list)
                result.append(
                    {
                        "id": manga.id,
                        "manga_id": manga.manga_id,
                        "manga_name": manga.manga_name,
                        "authors": author_list,
                        "categories": manga.categories,
                        "thumbnail": manga.image,
                        "description": manga.description,
                        "rate": manga.rank,
                        "view": manga.view,
                        "slug": manga.slug,
                        "chapter_count": manga.chapter_count,
                        "status": manga.status,
                        "created_at": manga.created_at,
                        "release_at": manga.release_at,
                        "updated_at": manga.updated_at,
                    }
                )
            meta_data = dict()
            meta_data["current"] = page
            meta_data["page_size"] = page_size
            meta_data["total_page"] = manga_count // page_size + 1

            data_["data"] = result
            data_["pagination"] = meta_data
            return jsonify(data_)
        except:
            session.rollback()
            raise
        finally:
            session.close()