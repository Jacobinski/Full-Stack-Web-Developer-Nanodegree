import webapp2
import cgi

form = '''
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

def rot13_string(string):
    def rot13_char_lower(char):
        output = ord(char) + 13

        if output > ord('z'):
            output -= 26

        return chr(output)

    #TODO: Increase code reuse... Remove a function
    def rot13_char_upper(char):
        output = ord(char) + 13

        if output > ord('Z'):
            output -= 26

        return chr(output)

    output = ""
    for s in string:
        if s.islower():
            output += rot13_char_lower(s)
        elif s.isupper():
            output += rot13_char_upper(s)
        else:
            output += s

    return output

class MainPage(webapp2.RequestHandler):
    def write_form(self, message=''):
        self.response.write(form %{"message":message})

    def get(self, message=''):
        self.response.headers['Content-Type'] = 'text/HTML'
        self.write_form()

    def post(self):
        message = self.request.get("text")
        self.write_form(cgi.escape(rot13_string(message)))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)