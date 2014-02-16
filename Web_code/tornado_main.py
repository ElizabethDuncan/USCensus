# Access this webpage from a browser at url: http://127.0.0.1:8888/

import tornado.ioloop
import tornado.web

class IndexHandler(tornado.web.RequestHandler):
    ''' index http normal handler'''
    def get(self):
        self.render("index.html")

application = tornado.web.Application([
    (r"/", IndexHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()