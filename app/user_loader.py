from app import login_manager
from app.models import User
from app.database import get_db

@login_manager.user_loader
def load_user(user_id):
    db= get_db()
    return db.session.query(User).get(int(user_id))

