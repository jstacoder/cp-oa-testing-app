import flask
from flask import views as flask_views, request, session as flask_session, redirect, url_for

import json
from uuid import uuid4
from requests import Session as RequestSession

import os
from calendar_data_tools import get_calenders_by_provider
from my_forms import CodeForm, scopes, CreateEventForm

os.environ['PYTHONUNBUFFERED'] = '1'
CLIENT_ID = os.environ.get("CRONOFY_CLIENT_ID")
REDIRECT_URI = os.environ.get("CRONOFY_REDIRECT_URI")

app = flask.Flask(__name__,template_folder="templates")
app.config.SECRET_KEY = 'ccc'
app.secret_key = 'ccc'

def load_session():
    rsession = RequestSession()
    try:
        rsession.headers['Authorization'] = "Bearer {}".format(
            flask_session['access_token']
    )
    except KeyError:
        return flask.redirect('/')
    else:
        return rsession
    
get_id = lambda prefix=None: "{}-{}".format(prefix or "testid", uuid4())

class EventView(flask_views.MethodView):
    def get(self,cal_id=None):
        cal_name = None
        for cal in load_session().get("https://api.cronofy.com/v1/calendars").json().get('calendars'):
            if cal.get('calendar_id') == cal_id:
                cal_name = cal.get('calendar_name')
        form = CreateEventForm(cal_id=cal_id)
        return flask.render_template("add_event.html",form=form,calendar_name=cal_name)
  
    def post(self,cal_id=None):
        new_event_id = get_id("newevent")
        form = CreateEventForm(request.args)

        event_args = dict(
            event_id=new_event_id,
            summary=form.summary.data,
            description=form.description.data,
            start=form.start.data,
            end=form.end.data,
            tzid=form.tzid.data,
            location=dict(description=form.location.data),
        )
        response = load_session().post("https://api.cronofy.com/v1/calendars/{}/events".format(cal_id),json=event_args)
        res_json = json.dumps(response)
        return flask.jsonify(res_json)


app.add_url_rule("/event/add/<cal_id>","add_event",view_func=EventView.as_view('add_event'))

class ListCalendarView(flask_views.MethodView):
    def get(self):
        rsession = load_session()
        response = rsession.get("https://api.cronofy.com/v1/calendars")

        calendars_by_profile = dict()

        extract_cal = lambda cal:\
         dict(name=cal.get('calendar_name'),id=cal.get('calendar_id'))
        calendars = response.json().get('calendars')
        for cal in calendars:
            profile_name = cal.get('profile_name')
            if calendars_by_profile.get(profile_name) is None:
                calendars_by_profile[profile_name] = []
            calendars_by_profile[profile_name].append(extract_cal(cal))

        calendar_profiles = calendars_by_profile.keys()

        rtn_template = app.jinja_env.from_string("{{ response|safe }}")
        template_context = dict(
            response=json.dumps(response.json()),
            token=flask_session['access_token']
        )
        res = flask.make_response(rtn_template.render(template_context))
        res.headers['Content-Type'] = 'application/json'
        return flask.render_template(
            "list_calendars.html",
            calendars_by_provider=get_calenders_by_provider(calendars),
            calendars=calendars,
            calendar_profiles=calendar_profiles,
            calendars_by_profile=calendars_by_profile,
        )

app.add_url_rule('/list_calendars','calendars',ListCalendarView.as_view('calendars'))

class FormHandlerView(flask_views.MethodView):
    def get(self):
	form = CodeForm(request.args)
	url = "https://app.cronofy.com/oauth/authorize?response_type=code&client_id={}&redirect_uri={}&scope={}&state=".format(
            form.client_id.data,
            form.redirect_uri.data,
            form.scope.data
        )
        return flask.redirect(url)

app.add_url_rule('/submit','submit',FormHandlerView.as_view('submit'))

class IndexView(flask_views.MethodView):
    def get(self):
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
            form_args = {'scope':scopes.keys()}
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
