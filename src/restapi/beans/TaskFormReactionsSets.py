from wtforms import Form, StringField, DecimalField, SelectField, BooleanField, validators
from .OptimizationEnum import *
from .MediumEnum import *

class TaskFormReactionsSets(Form):
    objective = StringField('objective',
                            [validators.optional(), validators.Length(min=1, max=256)])
    fraction_of_optimum = DecimalField('fraction_of_optimum',
                                       [validators.optional(),
                                        validators.NumberRange(min=0.0, max=1.0, message='Fraction of optimum must be in the range [0, 1]')])
    medium = SelectField(u'Growth medium',
                         [validators.optional()],
                         choices=[name for name, member in MediumEnum.__members__.items()])
    optimization = SelectField(u'Growth Optimization',
                               [validators.optional()],
                               choices=[name for name, member in OptimizationEnum.__members__.items()])
    skip_knockout = BooleanField(u'Skip knock-out computation',
                                 [validators.optional()],
                                 default=True)
