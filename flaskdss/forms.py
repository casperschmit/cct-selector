from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, \
    SelectMultipleField, widgets, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL
from wtforms.widgets import TextArea


class DeveloperInputForm(FlaskForm):
    content = TextAreaField('Name', validators=[DataRequired()])
    calibration = BooleanField('Re-calibrate')
    search_limit = IntegerField('Search limit', validators=[DataRequired()])
    submit = SubmitField('Search')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class NewCCTForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    technical_scheme = SelectField('Technical scheme',
                                   choices=['Sidechain', 'Notary', 'Hashed time-lock contract', 'Hybrid'],
                                   validators=[DataRequired()])
    use_case = SelectField('Technical scheme',
                           choices=['Asset transfer', 'Asset exchange', 'Cross-chain smart contract',
                                    'Cross-chain oracle'], validators=[DataRequired()])
    source = StringField('Source blockchain', validators=[DataRequired()])
    target = StringField('Target blockchain', validators=[DataRequired()])
    source_permissions = SelectField('Source blockchain permissions',
                                     choices=['Permissioned private', 'Permissioned public', 'Permissionless public'],
                                     validators=[DataRequired()])
    target_permissions = SelectField('Target blockchain permissions',
                                     choices=['Permissioned private', 'Permissioned public', 'Permissionless public'],
                                     validators=[DataRequired()])
    github = StringField('Link to Github organization', validators=[DataRequired(), URL(message='Enter valid URL')])
    docs = StringField('Link to developer documentation', validators=[DataRequired(), URL(message='Enter valid URL')])
    whitepaper = StringField('Either enter pdf download link to whitepaper or link to webpage',
                             validators=[DataRequired(), URL(message='Enter valid URL')])

    submit = SubmitField('Propose')


class NewGoalForm(FlaskForm):
    goal = StringField('Goal', validators=[DataRequired()])
    cct = SelectField('Cross-chain technology', choices=[], validators=[DataRequired()])
    submit = SubmitField('Add')


class InputForm(FlaskForm):
    goal = MultiCheckboxField('Goal', choices=[], coerce=int)
    submit = SubmitField('Next')


class WizardScenarioForm1(FlaskForm):
    scenario = SelectField('Situation', choices=[('cho_1', 'Connecting two defined blockchain systems'),
                                                 ('cho_2', 'Connecting one blockchain system to an undefined second'),
                                                 ('cho_3', 'Connecting two yet to define blockchain systems')],
                           validators=[DataRequired()])
    submit = SubmitField('Next')


class WizardScenarioFormCho1(FlaskForm):
    source = StringField('Source blockchain', validators=[DataRequired()])
    target = StringField('Target blockchain', validators=[DataRequired()])
    source_permissions = SelectField('Source blockchain permissions',
                                     choices=['Permissioned private', 'Permissionless private',
                                              'Permissioned public', 'Permissionless public'],
                                     validators=[DataRequired()])
    target_permissions = SelectField('Target blockchain permissions',
                                     choices=['Permissioned private', 'Permissionless private',
                                              'Permissioned public', 'Permissionless public'],
                                     validators=[DataRequired()])

    decentralization = SelectField('Must the project be completely decentralized?', choices=['yes', 'no'],
                                   validators=[DataRequired()])

    scalability = SelectField('Should the project be scalable?',
                              choices=['yes', 'no'],
                              validators=[DataRequired()])

    development = SelectField('Are development costs relatively limited?', choices=['yes', 'no'],
                              validators=[DataRequired()])

    efficiency = SelectField('Is efficiency of great importance for the final system?', choices=['yes', 'no'],
                             validators=[DataRequired()])

    tokens = SelectField('Does the aim of this project involve blockchain token interoperability?',
                         choices=['yes', 'no'],
                         validators=[DataRequired()])

    crypto = SelectField('Does this project revolve around the exchange of cryptocurrency?',
                         choices=['yes', 'no'],
                         validators=[DataRequired()])

    oracle = SelectField('Is this project\'s aim to access information on the target chain from the source chain?',
                         choices=['yes', 'no'],
                         validators=[DataRequired()])

    smart_contract = SelectField(
        'Is this project\'s aim to execute smart contracts on the target chain from the source chain?',
        choices=['yes', 'no'],
        validators=[DataRequired()])

    transfer = SelectField(
        'Does the project require the assets on the source chain to be transferred to the target chain and back?',
        choices=['yes', 'no'],
        validators=[DataRequired()])

    submit = SubmitField('Next')


class WizardCostForm(FlaskForm):
    team_size = IntegerField('What is the project\'s team size?',
                             validators=[DataRequired(message='Please fill an integer here.')])
    team_experience = SelectField('What is the project team\'s experience?', choices=[(0, 'Inexperienced'),
                                                                                      (1, 'Somewhat experienced'),
                                                                                      (2, 'Experienced'),
                                                                                      (3, 'Very experienced')],
                                  validators=[DataRequired()])
    submit = SubmitField('Next')


class WizardCompatibilityForm(FlaskForm):
    decentralization = SelectField('Must the project be completely decentralized?', choices=['yes', 'no'],
                                   validators=[DataRequired()])

    scalability = SelectField('Should the project be scalable?',
                              choices=['yes', 'no'],
                              validators=[DataRequired()])

    development = SelectField('Are development costs relatively limited?', choices=['yes', 'no'],
                              validators=[DataRequired()])

    efficiency = SelectField('Is efficiency of great importance for the final system?', choices=['yes', 'no'],
                             validators=[DataRequired()])

    tokens = SelectField('Does this project involve blockchain token interoperability?',
                         choices=['yes', 'no'],
                         validators=[DataRequired()])

    crypto = SelectField('Does this project revolve around the exchange of cryptocurrency?',
                         choices=['yes', 'no'],
                         validators=[DataRequired()])

    oracle = SelectField('Is this project\'s aim to access information on the target chain from the source chain?',
                         choices=['yes', 'no'],
                         validators=[DataRequired()])

    smart_contract = SelectField(
        'Is this project\'s aim to execute smart contracts on the target chain from the source chain?',
        choices=['yes', 'no'],
        validators=[DataRequired()])

    transfer = SelectField(
        'Does the project require the assets on the source chain to be transferred to the target chain and back?',
        choices=['yes', 'no'],
        validators=[DataRequired()])

    submit = SubmitField('Next')


class WizardRelevancyForm(FlaskForm):
    project_description = StringField('Provide a short description of the project (max 10 lines)', widget=TextArea(),
                                      validators=[DataRequired()])

    submit = SubmitField('Next')


class WizardScenarioForm1Def(FlaskForm):
    pass


class WizardScenarioForm0Def(FlaskForm):
    pass


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AttributeWeightForm(FlaskForm):
    cost_weight = IntegerField('What weight would you give to the \"Cost\" attribute?',
                               validators=[DataRequired(message='Please fill an integer here.')])
    compatibility_weight = IntegerField('What weight would you give to the \"Compatibility\" attribute?',
                                        validators=[DataRequired(message='Please fill an integer here.')])
    relevancy_weight = IntegerField('What weight would you give to the \"Relevancy\" attribute?',
                                    validators=[DataRequired(message='Please fill an integer here.')])
    complexity_weight = IntegerField('What weight would you give to the \"Complexity\" attribute?',
                                     validators=[DataRequired(message='Please fill an integer here.')])
    security_weight = IntegerField('What weight would you give to the \"Security\" attribute?',
                                   validators=[DataRequired(message='Please fill an integer here.')])
    devsupport_weight = IntegerField('What weight would you give to the \"Developer support\" attribute?',
                                     validators=[DataRequired(message='Please fill an integer here.')])

    submit = SubmitField('Calculate')


# For system operator
class UserManagementForm(FlaskForm):
    user_id = IntegerField('Enter user ID',
                           validators=[DataRequired(message='Enter valid integer here.')])

    new_role = SelectField('Assign new role', choices=['User', 'Curator', 'Admin'],
                           validators=[Length(min=2, max=20)])

    delete_user = BooleanField('Delete user')

    submit = SubmitField('Submit')


class DecentralizedForm(FlaskForm):
    decentralized = BooleanField('Decentralized')
    submit2 = SubmitField('Set database state')


# For CCT curators
class CuratorForm(FlaskForm):
    approve_id = IntegerField('Enter the ID of the CCT you would like to approve below.')
    approve_all = BooleanField('Approve all proposed CCTs')

    submit = SubmitField('Approve')
