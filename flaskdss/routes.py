from flask import render_template, url_for, flash, redirect, request

from analysis.complexity import get_git_repos, clear_dir, compute_complexity
from flaskdss import application, db
from flaskdss.forms import RegistrationForm, LoginForm, InputForm, NewGoalForm, NewCCTForm, \
    DeveloperInputForm, WizardScenarioForm1, WizardScenarioFormCho1, WizardCompatibilityForm, \
    WizardCostForm, WizardRelevancyForm, AttributeWeightForm, CuratorForm, UserManagementForm, DecentralizedForm
from flaskdss.models import CCT, System
from flaskdss import util
from flaskdss import route_manager
from flaskdss.models import User, Role, Proposed
from flaskdss import access_manager
from flask_login import current_user, logout_user, login_required
from analysis.analysis import compute_attributes, get_output_table, sort_output_table, compute_aggregated_score

from get_database import get_database
from search.search import download_pdf

@application.route("/")
@application.route("/home")
def home():
    return render_template('home.html')


@application.route("/about")
def about():
    return render_template('about.html', title='About')


@application.route("/update")
def update():
    return render_template('home.html', title='About')


@application.route("/dev-input", methods=['GET', 'POST'])
def developer_input():
    # # form = DeveloperInputForm()
    # # if form.validate_on_submit():
    # #     content = form.content.data
    # #     calibration = form.calibration.data
    # #     search_limit = form.search_limit.data
    # #     flash('Success', 'success')
    # #     print(content)
    # #     print(calibration)
    # #     print(search_limit)
    # #     search_results = search.keyword_search_handler('search/kb-input.xlsx', 'search/kb3', search_limit, calibration,
    # #                                                    content)
    #     return render_template('output.html', title='Results', items=search_results)
    # return render_template('input.html', title='Add input', form=form)
    pass


@application.route("/results", methods=['GET', 'POST'])
def results():
    results = [['Rootstock', 5], ['Polkadot', 6]]
    return render_template('output.html', title='Results', items=results)


@application.route("/404", methods=['GET', 'POST'])
def error():
    pass


@application.route("/system", methods=['GET', 'POST'])
@application.route("/system/step/<int:step>", methods=['GET', 'POST'])
@access_manager.requires_access(0)
def system(step=0):
    if step == -1:
        return redirect(url_for('404'))
    if step == 0:
        form = WizardScenarioForm1()
        if form.validate_on_submit():
            next_step = route_manager.handle_scenario(form, step)
            return redirect(url_for('system', step=next_step))
        else:
            print(form.errors.items())
        return render_template('wizard.html', title='Decision support system', form=form)
    if step == 1:
        form = WizardScenarioFormCho1()
        if form.validate_on_submit():
            next_step = route_manager.handle_compatibility(form, step)
            return redirect(url_for('system', step=next_step))
        return render_template('wizard.html', title='Decision support system - step 1', form=form)
    if step == 2:
        form = WizardCostForm()
        if form.validate_on_submit():
            next_step = route_manager.handle_cost(form, step)
            return redirect(url_for('system', step=next_step))
        return render_template('wizard.html', title='Decision support system - step 2', form=form)
    if step == 3:
        form = WizardRelevancyForm()
        if form.validate_on_submit():
            next_step = route_manager.handle_relevancy(form, step)
            return redirect(url_for('system', step=next_step))
        return render_template('wizard.html', title='Decision support system - step 3', form=form)
    if step == 4:
        form = AttributeWeightForm()
        if form.validate_on_submit():
            compute_attributes(form)
            return redirect(url_for('output'))
        return render_template('wizard.html', title='Decision support system - step 3', form=form)


@application.route("/output", methods=['GET', 'POST'])
@application.route("/output/sort-<string:sort>", methods=['GET', 'POST'])
@access_manager.requires_access(0)
def output(sort="aggregated"):
    output = sort_output_table(get_output_table(), sort)
    return render_template('output.html', title='Output', items=output)


@application.route("/curator", methods=['GET', 'POST'])
@access_manager.requires_access(1)
def curator():
    form = CuratorForm()
    if form.validate_on_submit():

        if form.approve_all.data:
            route_manager.approve_all_cct()
        else:
            cct_id = form.approve_id.data
            success = route_manager.approve_cct(cct_id)
            if not success:
                flash('Wrong cct id!', 'danger')
                return redirect(url_for('curator'))
        flash('Approval success!', 'success')
        return redirect(url_for('curator'))
    proposed_ccts = Proposed.query.all()
    return render_template('curator.html', title='Curator panel', form=form, table=proposed_ccts)


@application.route("/add-to-database", methods=['GET', 'POST'])
@access_manager.requires_access(0)
def add_cct():
    form = NewCCTForm()
    if form.validate_on_submit():
        success = route_manager.propose_cct(form)
        if success:
            flash('Proposed CCT!', 'success')
        else:
            flash('Something went wrong!', 'danger')
        return redirect(url_for('add_cct'))
    return render_template('wizard.html', title='Propose new CCT', form=form)


@application.route("/admin-panel", methods=['GET', 'POST'])
@access_manager.requires_access(2)
def admin_panel():
    system_row = System.query.filter_by(id=1).first()
    decentralized_db = system_row.decentralized

    form = UserManagementForm()
    decentralized_form = DecentralizedForm()

    if form.data:
        if form.validate_on_submit():
            success = route_manager.manage_user(form)
            if success:
                flash('Success!', 'success')
            else:
                flash('Something went wrong!', 'danger')
            return redirect(url_for('admin_panel'))

    if decentralized_form.data:
        if decentralized_form.validate_on_submit():
            decentralized_db = route_manager.set_decentralized(decentralized_form)
            if decentralized_db:
                flash('Switched db to decentralized!', 'success')
            return redirect(url_for('admin_panel'))

    users = User.query.all()
    return render_template('admin.html', title='Admin panel', form=form, table=users,
                           decentralized_form=decentralized_form, decentralized=decentralized_db)


@application.route("/register", methods=['GET', 'POST'])
def register():
    reg_json = request.get_json()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if reg_json:
        form = RegistrationForm.from_json(reg_json, skip_unknown_keys=True)
        formCheck = request.method == 'POST'
    else:
        form = RegistrationForm()
        formCheck = form.validate_on_submit()

    user_role = db.session.query(Role).filter_by(name='User').first().id
    if formCheck:
        user = User(username=form.username.data, email=form.email.data, password=form.password.data,
                    role=user_role)
        register_success = access_manager.register(user)

        if register_success:
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Something went wrong!', 'danger')
            return render_template('register.html', title='Register', form=form), 403

    return render_template('register.html', title='Register', form=form)


@application.route("/login", methods=['GET', 'POST'])
def login():
    reg_json = request.get_json()

    if reg_json:
        form = LoginForm.from_json(reg_json, skip_unknown_keys=True)
        formCheck = request.method == 'POST'
    else:
        form = LoginForm()
        formCheck = form.validate_on_submit()

    if formCheck:
        user_info = User(email=form.email.data, password=form.password.data)
        login_success = access_manager.login(user_info, form.remember.data)

        if login_success:
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return render_template('login.html', title='Login', form=form), 403

    if request.method == 'POST':
        print("No")

    return render_template('login.html', title='Login', form=form)


@application.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))


# @app.route("/ids")
# def set_id():
#
#     df = get_database()
#
#     for index, row in df.iloc[1:].iterrows():
#
#         entry = ""
#         for value in row:
#             entry += str(value)
#
#         print(hash(entry))
#         cct = CCT(
#             id=hash(entry),
#             name=row[0],
#             whitepaper=row[1],
#             docs=row[2],
#             github=row[3],
#             source_chain=row[4],
#             source_permissions=row[5],
#             target_chain=row[6],
#             target_permissions=row[7],
#             use_case=row[8],
#             technical_scheme=row[9]
#         )
#         db.session.add(cct)
#         db.session.commit()
#
#     return render_template('home.html', title='Home')

@application.route('/testing')
def testing():
    # download_pdf('https://www.wanlianzhijia.com/Uploads/Project/2018-03-30/5abdfb12241d3.pdf', '/')
    # download_pdf('https://arxiv.org/pdf/1810.02174.pdf', ROOT_DIR + '/test')
    # repos = get_git_repos('https://github.com/comit-network')
    # clear_dir(ROOT_DIR + '/' + str(current_user.id))
    # previous_most_starred = []
    # most_starred_repo = get_most_starred(repos, previous_most_starred)
    compute_complexity('https://github.com/comit-network', current_user.id)
    return render_template('home.html', title='test')
