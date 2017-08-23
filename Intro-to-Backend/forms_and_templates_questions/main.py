import webapp2
import cgi

rot13_form = '''
<!DOCTYPE html>
<html>
<head>
    <title>ROT13 Cipher</title>
</head>
<body>
    <h1>Enter some text to ROT13:</h1>

    <form action="/" method="post">
        <textarea name="text" rows="4" cols="50">%(message)s</textarea>
        <br>
        <input type="submit">
    </form>
</body>
</html>
'''

class MainPage(webapp2.RequestHandler):
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

    def write_form(self, message=''):
        self.response.write(rot13_form %{"message":message})

    def get(self, message=''):
        self.response.headers['Content-Type'] = 'text/HTML'
        self.write_form()

    def post(self):
        message = self.request.get("text")
        self.write_form(cgi.escape(self.__rot13_string(message)))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)