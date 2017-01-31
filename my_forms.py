import wtforms as wtf
from wtforms import fields, validators, form

scopes = dict(
    create_calendar='create_calendar',
    read_events='read_events',
    create_event='create_event',
    event_reminders='event_reminders',
    delete_event='delete_event',
    read_free_busy='read_free_busy',
    change_participation_status='change_participation_status',
)

class MySelectField(fields.SelectMultipleField):
    def process_formdata(self,valuelist):
        if valuelist:
            try: 
                print 'VALUES!!! ', valuelist
                self.data = ""
                for item in valuelist:
                    self.data += " {}".format(item[1])
            except:
                pass

class CodeForm(form.Form):
    client_id = fields.StringField("client id",validators=[validators.InputRequired()])
    redirect_uri = fields.StringField("redirect uri",validators=[validators.InputRequired()])
    scope = MySelectField('scopes',validators=None,choices=zip(scopes.keys(),scopes.keys()))
    response_type = fields.HiddenField(default='code')
    submit = fields.SubmitField("submit")


