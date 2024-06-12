from flask import current_app, render_template
from flask_mail import Message

from ...commons.constants.message import ERROR_MESSSAGE
from ...commons.extensions import Singleton
from ...commons.middlewares.exception import ApiException


class SendMailService(Singleton):
    @staticmethod
    def send_email_forgot_password(**kwargs):
        from src.app import mail

        try:
            msg = Message(
                sender=current_app.config.get("MAIL_FROM"),
                recipients=[kwargs["email"]],
                subject="Reset Password",
            )

            msg.html = render_template(
                template_name_or_list="forgot-password.html",
                new_password=kwargs["new_password"],
            )

            mail.send(msg)
        except Exception as e:
            current_app.logger.error(e)
            raise ApiException(ERROR_MESSSAGE.SEND_MAIL_ERROR, status_code=500)
