import logging
import os

import jinja2
import sendgrid
from flask import Flask, request
from google.appengine.api import wrap_wsgi_app
from sendgrid.helpers.mail import Content, Email, Mail, To
from wtforms import Form, StringField, TextAreaField, validators

DEBUG = bool(os.environ.get("DEBUG", False))
ENABLE_MAIL = bool(os.environ.get("ENABLE_MAIL", True))
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDGRID_FROM = os.environ.get("SENDGRID_FROM")
SENDGRID_TO = os.environ.get("SENDGRID_TO")

app = Flask(
    __name__,
    static_folder="media",
    template_folder="template",
)
app.wsgi_app = wrap_wsgi_app(app.wsgi_app)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "template")),
    autoescape=True,
)


def default_render(template_name, *args, **kwargs):
    template_values = {"template_name": template_name}
    template = JINJA_ENVIRONMENT.get_template(template_name)
    return template.render(template_values, *args, **kwargs)


@app.route("/")
def index():
    return default_render("index.html")


@app.route("/en/")
def en_index():
    return default_render("en_index.html")


@app.route("/profile/")
def profile():
    return default_render("profile.html")


@app.route("/en/profile/")
def en_profile():
    return default_render("en_profile.html")


@app.route("/onlinecourse/")
def online_course():
    return default_render("online_course.html")


@app.route("/en/onlinecourse/")
def en_online_course():
    return default_render("en_online_course.html")


@app.route("/contact/")
def contact():
    return default_render("contact.html")


@app.route("/en/contact/")
def en_contact():
    return default_render("en_contact.html")


class InquiryForm(Form):
    """
    @see https://flask.palletsprojects.com/en/2.3.x/patterns/wtforms/
    """

    name = StringField("Name", [validators.Length(min=1, max=25)])
    email = StringField("Email Address", [validators.Length(min=6, max=35)])
    subject = StringField("Subject", [validators.Length(min=1, max=25)])
    message = TextAreaField("Message")


@app.route("/inquiry/", methods=["GET", "POST"])
def inquiry():
    form = InquiryForm(request.form)
    if request.method == "POST" and form.validate():
        body = (
            f"name: {form.name.data}\n\nemail: {form.email.data}\n\n{form.message.data}"
        )
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        content = Content("text/plain", body)
        mail = Mail(Email(SENDGRID_FROM), To(SENDGRID_TO), form.subject.data, content)
        if ENABLE_MAIL:
            response = sg.client.mail.send.post(request_body=mail.get())
            logging.debug(f"action=inquiry response={response}")
        return default_render("inquiry_sent.html")

    return default_render("inquiry.html", form=form)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=DEBUG)
