import webapp2
import jinja2
import cgi
import os
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
    autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_string(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_string(template, **kw))

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.redirect("/rot13")

class Rot13Page(Handler):
    def __rot13_string(self, string):
        def rot13_char(char):
            if char.isalpha():
                output = ord(char) + 13

                if ( char.islower() and output > ord('z') ) or \
                ( char.isupper() and output > ord('Z') ):
                    output -= 26

                return chr(output)
            else:
                return char

        output = ""
        for s in string:
            output += rot13_char(s)

        return output

    def get(self):
        self.response.headers['Content-Type'] = 'text/HTML'
        self.render("rot13.html")

    def post(self):
        message = self.request.get("text")
        self.render("rot13.html", message = self.__rot13_string(message))

class LoginPage(Handler):
    username_regex = re.compile("^[a-zA-Z0-9_-]{3,20}$")
    password_regex = re.compile("^.{3,20}$")
    email_regex = re.compile("^[\S]+@[\S]+.[\S]+$")

    def check_passwords_match(self, pass1, pass2):
        if pass1 and pass2 and pass1 == pass2:
            return True
        else:
            return False

    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get("username")
        email = self.request.get("email")
        password = self.request.get("password")
        password_check = self.request.get("verify")

        if self.check_passwords_match(password, password_check) == True:
            error = False
        else:
            error = True

        if self.username_regex.match(username) and \
        self.password_regex.match(password) and \
        self.email_regex.match(email) and \
        error == False:
            self.redirect("/rot13")

        self.render("login.html", username = username, email = email, error = error)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rot13', Rot13Page),
    ('/login', LoginPage),
], debug=True)