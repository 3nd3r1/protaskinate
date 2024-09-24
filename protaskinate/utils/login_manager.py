""" protaskinate/utils/login_manager.py """
from flask_login import LoginManager

lm = LoginManager()
lm.login_view = "login.login_route" #type: ignore
