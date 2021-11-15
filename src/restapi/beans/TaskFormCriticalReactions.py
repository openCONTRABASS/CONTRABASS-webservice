from wtforms import Form, StringField, DecimalField, validators

class TaskFormCriticalReactions(Form):
    objective = StringField('objective',
                            [validators.optional(), validators.Length(min=1, max=256)])
    fraction_of_optimum = DecimalField('fraction_of_optimum',
                                       [validators.optional(),
                                        validators.NumberRange(min=0.0, max=1.0, message='Fraction of optimum must be in the range [0, 1]')])
