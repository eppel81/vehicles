from flask.ext.login import current_user
from functools import wraps
from flask import request, redirect, url_for, flash


def admin_required(func):
    """
    Decorator for checking admin permissions
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.admin:
            return func(*args, **kwargs)
        else:
            flash('You need administrator privilegies', 'warning')
            return redirect(request.referrer or url_for('index'))
    return decorated_view
