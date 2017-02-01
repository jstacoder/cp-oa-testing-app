import flask
from flask import views as flask_views, request, session as flask_session, redirect, url_for


import json
from requests import Session as RequestSession

import os

from my_forms import CodeForm

os.environ['PYTHONUNBUFFERED'] = '1'
CLIENT_ID = os.environ.get("CRONOFY_CLIENT_ID")
REDIRECT_URI = os.environ.get("CRONOFY_REDIRECT_URI")

app = flask.Flask(__name__,template_folder="templates")
app.config.SECRET_KEY = 'ccc'
app.secret_key = 'ccc'

rsession = RequestSession()


class ListCalendarView(flask_views.MethodView):
    def get(self):
        try:
            rsession.headers['Authorization'] = "Bearer: {}".format(
                flask_session['access_token']
            )
        except KeyError:
            return flask.redirect('/')
        response = rsession.get("https://api.cronofy.com/v1/calendars")
        return flask.render_template_string("{{ response }}",response=response.reason,token=flask_session['access_token'])

app.add_url_rule('/list_calendars','calendars',ListCalendarView.as_view('calendars'))

class FormHandlerView(flask_views.MethodView):
    def get(self):
        print request.args#,request.params,request.json,request.form,request.data
	form = CodeForm(request.args)
	url = "https://app.cronofy.com/oauth/authorize?response_type=code&client_id={}&redirect_uri={}&scope={}&state=".format(
            form.client_id.data,
            form.redirect_uri.data,
            form.scope.data
        )
        
        return flask.render_template_string("{{ args }}<br />authenticate:<a href='{{ url }}'>go</a>",**dict(args=request.args,data=form.scope.data,url=url))

app.add_url_rule('/submit','submit',FormHandlerView.as_view('submit'))

class IndexView(flask_views.MethodView):
    def get(self):
        #print flask.request.params
        rtn_args = flask.request.args.copy()
        if len(rtn_args):
            template = 'code.html'
            GRANT_TYPE = "authorization_code"
            code = rtn_args['code']
            client_secret = os.environ.get("CRONOFY_CLIENT_SECRET")
            oauth_args = dict(
                client_id = CLIENT_ID,
                client_secret = client_secret,
                grant_type = GRANT_TYPE,
                code = code,
                redirect_uri = REDIRECT_URI,
            )
            response = rsession.post("https://api.cronofy.com/oauth/token",json=oauth_args)
            rtn = response.json() if response.ok else response.reason
            args = dict(response=rtn)
            flask_session['access_token'] = rtn.get('access_token')
            flask_session['refresh_token'] = rtn.get('refresh_token')
            return_response = redirect(url_for("calendars"))
        else:
            template = 'index.html'
            form_args = {}
            if CLIENT_ID is not None:
                form_args['client_id'] = CLIENT_ID
            if REDIRECT_URI is not None:
                form_args['redirect_uri'] = REDIRECT_URI
            form = CodeForm(**form_args)
            args = {'form':form}        
            return_response = flask.render_template(template,**args)
        return return_response


app.add_url_rule('/','index',IndexView.as_view('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get('PORT',8000)),debug=True)
