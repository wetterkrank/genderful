import os
import re
import argparse
import cherrypy
import usemodel
import preprocess as prep

class Root(object):
    @cherrypy.expose
    def index(self):
        return open('./public/index.html')

    @staticmethod
    def error_page(status, message, traceback, version):
        return """{"status": "KO", "message":"%s"}""" % message

    def __init__(self):
        # App config
        self._conf = {
                '/': {
                    'tools.staticdir.on': True,
                    'tools.staticdir.root': os.path.abspath(os.getcwd()),
                    'tools.staticdir.dir': './public',
                    'tools.secureheaders.on': True,
                },
                '/predict': {
                    'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
                    'tools.response_headers.on': True,
                    'tools.encode.on': True,
                    'tools.encode.encoding': 'utf-8',
                },
        }

    @staticmethod
    @cherrypy.tools.register('before_finalize', priority=60)
    def secureheaders():
        headers = cherrypy.response.headers
        headers['X-Frame-Options'] = 'DENY'
        headers['X-XSS-Protection'] = '1; mode=block'
        # headers['Content-Security-Policy'] = "default-src 'self';" # have to serve CSS locally

@cherrypy.expose
class PredictWS(object):
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.allow(methods=['GET'])
    @cherrypy.tools.accept(media='application/json')
    def GET(self, word):
        word_UNSAFE = word.lower() if word else 'Etwas'

        allowed_chars_re = '[^' + ''.join(list(prep.ALPHABET_DE.keys())[1:-1]).replace('-',r'\-') + ']'
        word = re.sub(allowed_chars_re, '\x1A', word_UNSAFE)

        result = genders_model.predict(word)
        result['probability'] = str(result['probability'])
        result['word'] = result['word'].replace('\x1A', '*').capitalize()
        return result

class Server(object):
    def __init__(self, port):
        # Global server config
        cherrypy.config.update({
            'server.socket_host': '0.0.0.0', # bind to all host's IPs, not only 127.0.0.1 (localhost)
            'server.socket_port': port,
            'error_page.default': Root.error_page,
            'server.thread_pool': 30,
        })

    def start(self):
        root = Root()
        root.predict = PredictWS()
        cherrypy.quickstart(root, '/', root._conf)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Genderful')
    parser.add_argument('--port', required=True, help="http port")
    cmd_args = parser.parse_args()
    port = int(cmd_args.port)

    genders_model = usemodel.Predictor()
    Server(port).start()