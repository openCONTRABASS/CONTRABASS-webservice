from wtforms import Form, StringField, DecimalField, validators


class SubmitURL(Form):
    model_url = StringField(
        "url", [validators.required(), validators.Length(min=5, max=2048)]
    )
