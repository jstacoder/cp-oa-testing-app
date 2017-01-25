import flask
from flask import views as flask_views

import os

app = flask.Flask(__name__,template_folder="templates")
app.config.SECRET_KEY = 'ccc'

class IndexView(flask_views.MethodView):
    def get(self,code=None,state=None):
        rtn_args = dict()
        rtn_args['code'] = code if code is not None else "no code"
        rtn_args['state'] = state if state is not None else "no state"
        return flask.render_template('index.html',**rtn_args)

    def post(self,code=None,state=None):
        return self.get(code,state)

app.add_url_rule('/','index',IndexView.as_view('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=os.environ.get('PORT',8000),debug=True)
