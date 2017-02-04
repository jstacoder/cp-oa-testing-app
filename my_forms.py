import wtforms as wtf
from wtforms import fields, validators, form
from wtforms.fields import html5

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
        super(MySelectField,self).process_formdata(valuelist)
        if valuelist:
            try: 
                print 'VALUES!!! ', valuelist
                self.data = ""
                for item in valuelist:
                    self.data += " {}".format(item)
            except:
                pass
    def process_data(self,value):
        super(MySelectField,self).process_data(value)
        try:           
            values = value.split(',') 
            self.data = values if len(values) else value
        except:
            pass

class CodeForm(form.Form):
    client_id = fields.StringField("client id",validators=[validators.InputRequired()])
    redirect_uri = fields.StringField("redirect uri",validators=[validators.InputRequired()])
    scope = MySelectField('scopes',validators=None,choices=zip(scopes.keys(),scopes.keys()))
    response_type = fields.HiddenField(default='code')
    submit = fields.SubmitField("submit")

class CreateEventForm(form.Form):
    event_id = fields.HiddenField()
    cal_id = fields.HiddenField()
    summary = fields.StringField('Summary',validators=[validators.InputRequired()])
    description = fields.TextAreaField("description")
    start = html5.DateTimeField("start",format="%m-%d-%Y")
    end = html5.DateTimeField("end",format="%m-%d-%Y")
    tzid = fields.HiddenField(default="America/Los_Angeles")
    location = fields.StringField("location")
    submit = fields.SubmitField()

