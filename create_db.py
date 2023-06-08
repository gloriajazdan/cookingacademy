from website import db , create_app
app=create_app()
from website.models import User, Classes, Tickets, Comments
ctx=app.app_context()
ctx.push()
db.create_all()
quit()
