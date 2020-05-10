import cherrypy
import re
import ml2

class PredictionWebApp(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
            <body>
              <form method="get" action="predict">
                <input type="text" value="Messer" name="user_input" />
                <button type="submit">Determine the gender</button>
              </form>
            </body>
        </html>"""

    @cherrypy.expose
    def predict(self, user_input):
        if not user_input: 
            user_input = "Etwas"
        word_mod = user_input.lower()
        #TODO: use prep.ALPHABET_DE
        word_mod = re.sub(
            r'[^abcdefghijklmnopqrstuvwxyzäöüß\-]', '\x1A', word_mod)
        result = word_mod + ": " + ml2.predict(model, word_mod)
        return result


if __name__ == '__main__':
    model = ml2.load_model(ml2.MODEL_FILE)

cherrypy.config.update(
    {'server.socket_host': '0.0.0.0'})  # bind to all host's IPs, not only 127.0.0.1/localhost

cherrypy.quickstart(PredictionWebApp())
