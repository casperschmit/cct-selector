from flaskdss import application, db
import pandas as pd
from flaskdss.models import Project, User, Proposed, CCT, Role, System
from flask_login import current_user
from flask import flash
import json
import hashlib


def handle_scenario(form, step):
    scenario = form.scenario.data
    if scenario == 'cho_1':
        return step + 1
    else:
        flash('Not implemented yet!', 'info')
        return step


def assign_relative_ranking(results):
    sorted_results = dict(sorted(results.items(), key=lambda item: item[1]))

    prev = 0
    bonus = 0
    for key in sorted_results:
        if sorted_results[key] == prev:
            sorted_results[key] = bonus
        else:
            prev = sorted_results[key]
            sorted_results[key] = bonus
            bonus += 1

    return sorted_results


def handle_compatibility(form, step):
    df = pd.read_sql_table('user', db.engine)
    print(df)

    technical_scheme = {'HTLC': 0, 'Notary': 0, 'Sidechain': 0, 'Hybrid': 0}

    if form.decentralization.data == 'yes':
        technical_scheme['HTLC'] += 3
        technical_scheme['Notary'] += 0
        technical_scheme['Sidechain'] += 2
        technical_scheme['Hybrid'] += 1
    else:
        technical_scheme['HTLC'] += 0
        technical_scheme['Notary'] += 3
        technical_scheme['Sidechain'] += 1
        technical_scheme['Hybrid'] += 2

    if form.scalability.data == 'yes':
        technical_scheme['HTLC'] += 0
        technical_scheme['Notary'] += 1
        technical_scheme['Sidechain'] += 2
        technical_scheme['Hybrid'] += 3
    else:
        technical_scheme['HTLC'] += 3
        technical_scheme['Notary'] += 2
        technical_scheme['Sidechain'] += 1
        technical_scheme['Hybrid'] += 0

    if form.development.data == 'yes':
        technical_scheme['HTLC'] += 3
        technical_scheme['Notary'] += 2
        technical_scheme['Sidechain'] += 1
        technical_scheme['Hybrid'] += 0
    else:
        technical_scheme['HTLC'] += 0
        technical_scheme['Notary'] += 1
        technical_scheme['Sidechain'] += 2
        technical_scheme['Hybrid'] += 3

    if form.efficiency.data == 'yes':
        technical_scheme['HTLC'] += 0
        technical_scheme['Notary'] += 3
        technical_scheme['Sidechain'] += 2
        technical_scheme['Hybrid'] += 1
    else:
        technical_scheme['HTLC'] += 3
        technical_scheme['Notary'] += 0
        technical_scheme['Sidechain'] += 1
        technical_scheme['Hybrid'] += 2

    use_case = {'Asset exchange': 0, 'Asset transfer': 0, 'Cross-chain smart-contract': 0, 'Cross-chain oracle': 0}

    if form.tokens.data == 'yes':
        use_case['Asset exchange'] += 1
        use_case['Asset transfer'] += 1

    if form.crypto.data == 'yes':
        use_case['Asset exchange'] += 1

    if form.oracle.data == 'yes':
        use_case['Cross-chain oracle'] += 1

    if form.smart_contract.data == 'yes':
        use_case['Cross-chain smart-contract'] += 1

    if form.transfer.data == 'yes':
        use_case['Asset transfer'] += 1

    technical_scheme = assign_relative_ranking(technical_scheme)
    # use_case = sorted(use_case.items(), key=lambda item: item[1])[-1][0]  # Get name of use case with highest score
    # print(use_case[1])

    project = Project.query.filter_by(user=current_user.id).first()

    if project:
        project.user = current_user.id
        project.source_chain = form.source.data
        project.source_permissions = form.source_permissions.data
        project.target_chain = form.target.data
        project.target_permissions = form.target_permissions.data
        project.use_case = json.dumps(use_case)
        project.technical_scheme = json.dumps(technical_scheme)
        db.session.commit()
    else:
        project = Project(
            user=current_user.id,
            source_chain=form.source.data,
            source_permissions=form.source_permissions.data,
            target_chain=form.target.data,
            target_permissions=form.target_permissions.data,
            use_case=json.dumps(use_case),
            technical_scheme=json.dumps(technical_scheme),
            team_size=0,
            team_experience=0,
            description=""
        )

        db.session.add(project)
        db.session.commit()

    return step + 1


def approve_all_cct():
    proposed_ccts = Proposed.query.all()

    for proposed_cct in proposed_ccts:
        cct = CCT(
            id=proposed_cct.id,
            name=proposed_cct.name,
            whitepaper=proposed_cct.whitepaper,
            docs=proposed_cct.docs,
            github=proposed_cct.github,
            source_chain=proposed_cct.source_chain,
            source_permissions=proposed_cct.source_permissions,
            target_chain=proposed_cct.target_chain,
            target_permissions=proposed_cct.target_permissions,
            use_case=proposed_cct.use_case,
            technical_scheme=proposed_cct.technical_scheme
        )
        db.session.add(cct)

    db.session.commit()


def propose_cct(form):
    row = form.name.data + form.technical_scheme.data + form.use_case.data + form.source.data + form.target.data + \
          form.source_permissions.data + form.target_permissions.data + form.github.data + form.docs.data + \
          form.whitepaper.data

    print(row)

    cct = Proposed(
        id=hash(row),
        name=form.name.data,
        whitepaper=form.whitepaper.data,
        docs=form.docs.data,
        github=form.github.data,
        source_chain=form.source.data,
        source_permissions=form.source_permissions.data,
        target_chain=form.target.data,
        target_permissions=form.target_permissions.data,
        use_case=form.use_case.data,
        technical_scheme=form.technical_scheme.data
    )

    check = Proposed.query.filter_by(id=hash(row)).first()
    if check:
        return False

    db.session.add(cct)
    db.session.commit()

    return True


def approve_cct(id):
    proposed_cct = Proposed.query.filter_by(id=id).first()

    if not proposed_cct:
        return False

    # Copy proposed to main cct table
    cct = CCT(
        id=proposed_cct.id,
        name=proposed_cct.name,
        whitepaper=proposed_cct.whitepaper,
        docs=proposed_cct.docs,
        github=proposed_cct.github,
        source_chain=proposed_cct.source_chain,
        source_permissions=proposed_cct.source_permissions,
        target_chain=proposed_cct.target_chain,
        target_permissions=proposed_cct.target_permissions,
        use_case=proposed_cct.use_case,
        technical_scheme=proposed_cct.technical_scheme
    )

    # Delete proposed cct from proposition list
    Proposed.query.filter_by(id=id).delete()

    # Db handling
    db.session.add(cct)
    db.session.commit()

    return True


def handle_cost(form, step):
    project = Project.query.filter_by(user=current_user.id).first()
    project.team_size = form.team_size.data
    project.team_experience = form.team_experience.data
    db.session.commit()
    return step + 1


def handle_security(data, step):
    pass


def handle_relevancy(form, step):
    project = Project.query.filter_by(user=current_user.id).first()
    project.description = form.project_description.data
    db.session.commit()
    return step + 1


def manage_user(form):
    if form.delete_user.data:
        return delete_user(form.user_id.data)
    else:
        return change_user_role(form.user_id.data, form.new_role.data)


def delete_user(user_id):
    user = User.query.filter_by(user=user_id).first()
    if not user:
        return False
    user.delete()
    db.session.commit()
    return True


def change_user_role(user_id, new_role):
    user = User.query.filter_by(id=user_id).first()

    if user_id is current_user.id:
        return False
    if not user:
        return False
    role = Role.query.filter_by(name=new_role).first()
    user.role = role.id
    db.session.commit()
    return True


def set_decentralized(decentralized_form):

    system_row = System.query.filter_by(id=1).first()

    if decentralized_form.decentralized.data:
        decentralized_db = True
        system_row.decentralized = True
    else:
        system_row.decentralized = False
        decentralized_db = False

    db.session.commit()

    return decentralized_db
