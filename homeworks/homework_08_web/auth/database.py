from auth.models import User


def fill_database(db):
    db.drop_all()
    db.create_all()

    user = User(
        email='email@service.com',
        login='simple_user'
    )
    user.set_password('pass')

    db.session.add(user)
    db.session.commit()
