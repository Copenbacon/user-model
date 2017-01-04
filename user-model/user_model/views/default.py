from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from ..models import User
from pyramid.httpexceptions import HTTPFound
from user_model.security import check_credentials
from pyramid.security import remember, forget


@view_config(
    route_name='home',
    renderer='../templates/home.jinja2',
    require_csrf=False)
def home_view(request):
    """Home view."""
    try:
        query = request.dbsession.query(User)
        usernames = query.get(User.username).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'usernames': usernames, 'project': 'user-model'}


@view_config(route_name="profile",
             renderer="../templates/profile.jinja2")
def profile_view(request):
    """show the user their profile."""
    the_id = int(request.matchdict["id"])
    user_stuff = request.dbsession.query(User).get(the_id)
    return {"user": user_stuff}


@view_config(route_name="registration",
             renderer="../templates/registration.jinja2",
             require_csrf=False)
def registration_view(request):
    """Register a new user."""
    if request.POST:
        user = User(
            request.POST["username"],
            request.POST["password"],
            request.POST["email"],
            request.POST["First Name"],
            request.POST["Surname"],
            request.POST["Favorite Food"]
        )
        request.dbsession.add(user)
        return HTTPFound(request.route_url('profile'))

    return {}


@view_config(route_name="login",
             renderer="../templates/login.jinja2",
             require_csrf=False)
def login_view(request):
    """Authenticate the incoming user."""
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password, request):
            auth_head = remember(request, username)
            return HTTPFound(
                request.route_url("home"),
                headers=auth_head
            )

    return {}


@view_config(route_name="logout")
def logout_view(request):
    """Remove authentication from the user."""
    auth_head = forget(request)
    return HTTPFound(request.route_url("home"), headers=auth_head)


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_user-model_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
