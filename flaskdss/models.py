from datetime import datetime
from flask_login import UserMixin

from flaskdss import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.role}')"

    def has_role(self, level):
        user_role = db.session.query(Role).filter_by(id=self.role).first()
        user_level = user_role.level
        if user_level >= level:
            return True
        else:
            return False


class CCT(db.Model):
    __tablename__ = 'cct'

    id = db.Column(db.BigInteger, primary_key=True, index=True)
    name = db.Column(db.String(120), nullable=False)
    whitepaper = db.Column(db.String(120), nullable=True)
    docs = db.Column(db.String(120), nullable=True)
    github = db.Column(db.String(120), nullable=True)
    source_chain = db.Column(db.String(120), nullable=True)
    source_permissions = db.Column(db.String(120), nullable=True)
    target_chain = db.Column(db.String(120), nullable=True)
    target_permissions = db.Column(db.String(120), nullable=True)
    use_case = db.Column(db.String(120), nullable=True)
    technical_scheme = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"{self.name} (ID: '{self.id}')"


class Proposed(db.Model):
    __tablename__ = 'proposed'

    id = db.Column(db.BigInteger, primary_key=True, index=True)
    name = db.Column(db.String(120), nullable=False)
    whitepaper = db.Column(db.String(120), nullable=True)
    docs = db.Column(db.String(120), nullable=True)
    github = db.Column(db.String(120), nullable=True)
    source_chain = db.Column(db.String(120), nullable=True)
    source_permissions = db.Column(db.String(120), nullable=True)
    target_chain = db.Column(db.String(120), nullable=True)
    target_permissions = db.Column(db.String(120), nullable=True)
    use_case = db.Column(db.String(120), nullable=True)
    technical_scheme = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"{self.name} (ID: '{self.id}')"


class Attributes(db.Model):
    __tablename__ = 'attributes'

    id = db.Column(db.Integer, primary_key=True)
    cct = db.Column(db.BigInteger, db.ForeignKey('cct.id'), nullable=False, index=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cost = db.Column(db.Integer, nullable=True)
    compatibility = db.Column(db.Integer, nullable=True)
    relevancy = db.Column(db.Float, nullable=True)
    complexity = db.Column(db.Float, nullable=True)
    security = db.Column(db.Integer, nullable=True)
    dev_support = db.Column(db.Integer, nullable=True)

    aggregated = db.Column(db.Float, nullable=True)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    level = db.Column(db.Integer, nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    source_chain = db.Column(db.String(120), nullable=False)
    source_permissions = db.Column(db.String(120), nullable=False)
    target_chain = db.Column(db.String(120), nullable=False)
    target_permissions = db.Column(db.String(120), nullable=False)
    use_case = db.Column(db.NVARCHAR(4000), nullable=False)
    technical_scheme = db.Column(db.NVARCHAR(4000), nullable=False)

    team_size = db.Column(db.Integer, nullable=False)
    team_experience = db.Column(db.Integer, nullable=False)

    description = db.Column(db.Text(), nullable=False)


class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    decentralized = db.Column(db.Boolean, nullable=False)
