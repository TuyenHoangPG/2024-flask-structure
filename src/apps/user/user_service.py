from sqlalchemy import text

from src.apps.user.dtos.requests.view_list_user_request import UserSearchByEnum
from src.commons.models.user_model import User
from src.commons.extensions import Singleton
from src.commons.constants.constant import USER_ROLES, SORT_TYPE, USER_STATUS
from src.commons.constants.message import ERROR_MESSSAGE
from src.commons.middlewares.exception import ApiException


class UserService(Singleton):
    def get_by_email(self, email: str):
        return User.query.filter(User.email == email.lower()).first()

    def get_by_id(self, user_id: str):
        return User.query.filter_by(id=user_id).first()

    def get_list(
        self,
        page,
        page_size,
        keyword=None,
        search_by=None,
        sort_by=None,
        sort_type=None,
    ):
        query = User.query.filter(User.role == USER_ROLES.USER)

        if keyword and search_by:
            if search_by == UserSearchByEnum.EMAIL:
                query = query.filter(text(f'"users"."email" ILIKE :email')).params(
                    email=f"%{keyword}%"
                )
            elif search_by == UserSearchByEnum.NAME:
                query = query.filter(text(f'"users"."full_name" ILIKE :name')).params(
                    name=f"%{keyword}%"
                )
            elif search_by == UserSearchByEnum.STATUS:
                query = query.filter(User.status == keyword)

        if sort_by:
            if sort_by == UserSearchByEnum.EMAIL:
                query = query.order_by(
                    User.email.desc()
                    if sort_type == SORT_TYPE.DESC
                    else User.email.asc()
                )
            elif sort_by == UserSearchByEnum.NAME:
                query = query.order_by(
                    User.full_name.desc()
                    if sort_type == SORT_TYPE.DESC
                    else User.full_name.asc()
                )
            elif sort_by == UserSearchByEnum.STATUS:
                query = query.order_by(
                    User.status.desc()
                    if sort_type == SORT_TYPE.DESC
                    else User.status.asc()
                )
        else:
            query = query.order_by(User.created_at.desc())

        data = query.paginate(page=page, per_page=page_size)

        return data.total, data.items

    def add_new_user(self, data):
        user_exist = self.get_by_email(data.get("email"))
        if user_exist is not None:
            raise ApiException(ERROR_MESSSAGE.EMAIL_EXISTED)

        user_model = User(
            email=data.get("email").lower(),
            full_name=data.get("full_name"),
            password=data.get("password"),
            role=USER_ROLES.USER,
        )

        user_model.save()

        return user_model

    def update_user(self, id, data):
        user = User.query.filter_by(id=id).first()
        if user is None:
            raise ApiException(ERROR_MESSSAGE.USER_NOT_FOUND)

        user.update(**data)

        return {"success": True}

    def delete_user(self, id):
        user = User.query.filter_by(id=id).first()
        if user is None:
            raise ApiException(ERROR_MESSSAGE.USER_NOT_FOUND)

        list_assignee = User.query.filter_by(supervisor_id=id).all()
        if len(list_assignee) > 0:
            raise ApiException(ERROR_MESSSAGE.USER_HAS_ASSIGNEE)

        user.update(status=USER_STATUS.INACTIVE)

        return {"success": True}
