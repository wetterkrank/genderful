import os
import re
import cherrypy
import usemodel
import preprocess as prep

class Root(object):
    @cherrypy.expose
    def index(self):
        return open('./public/index.html')

class PredictWS(object):
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.allow(methods=['GET'])
    @cherrypy.tools.accept(media='application/json')
    @cherrypy.expose
    def index(self, word):
        word_UNSAFE = word.lower() if word else 'Etwas'

        allowed_chars_re = '[^' + ''.join(list(prep.ALPHABET_DE.keys())[1:-1]).replace('-',r'\-') + ']'
        word = re.sub(allowed_chars_re, '\x1A', word_UNSAFE)

        result = genders_model.predict(word)
        result['probability'] = str(result['probability'])
        result['word'] = result['word'].replace('\x1A', '*').capitalize()
        return result

    @staticmethod
    def error_page(status, message, traceback, version):
        return """{"status": "KO", "message":"%s"}""" % message

#TODO: Move into class configuration
@cherrypy.tools.register('before_finalize', priority=60)
def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    # headers['Content-Security-Policy'] = "default-src 'self';" # have to serve CSS locally

if __name__ == '__main__':
    genders_model = usemodel.Predictor()

    # Global server config
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0', # bind to all host's IPs, not only 127.0.0.1/localhost
        'server.socket_port': 8081, #TODO: make configurable
        'error_page.default': PredictWS.error_page,
        'error_page.404': PredictWS.error_page,
        'error_page.400': PredictWS.error_page,
        'error_page.500': PredictWS.error_page,     
        'server.thread_pool': 30,
    })

    # App config
    current_dir = os.path.abspath(os.getcwd())
    ws_conf = {
            '/': {
                'tools.staticdir.root': current_dir,
                'tools.staticdir.on': True,
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

    cherrypy.tree.mount(Root(), '/', ws_conf)
    cherrypy.tree.mount(PredictWS(), '/predict', ws_conf)

    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()