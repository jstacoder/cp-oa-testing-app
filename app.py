import flask
from flask import views as flask_views, request

import os

from my_forms import CodeForm

os.environ['PYTHONUNBUFFERED'] = '1'

app = flask.Flask(__name__,template_folder="templates")
app.config.SECRET_KEY = 'ccc'


class FormHandlerView(flask_views.MethodView):
    def get(self):
        print request.args#,request.params,request.json,request.form,request.data
	form = CodeForm(request.args)
        return flask.render_template_string("{{ args }}<br />scope: {{ data }}",**dict(args=request.args,data=form.scope.data))

app.add_url_rule('/submit','submit',FormHandlerView.as_view('submit'))

class IndexView(flask_views.MethodView):
    def get(self):
        #print flask.request.params
        rtn_args = flask.request.args.copy()
        if len(rtn_args):
            template = 'code.html'
            args = rtn_args
        else:
            template = 'index.html'
            args = {'form':CodeForm()}
        #rtn_args['code'] = code if code is not None and rtn_args.get("code",None) is None else "no code"
        #rtn_args['state'] = state if state is not None else "no state"
        return flask.render_template(template,**args)


app.add_url_rule('/','index',IndexView.as_view('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get('PORT',8000)),debug=True)
