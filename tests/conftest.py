import pytest
from website import db, create_app
from website.models import User


@pytest.fixture
def app():
    """Create a test application."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the application."""
    return app.test_client()


@pytest.fixture
def create_user(app):
    """Create a test user."""
    def _create_user(email, username, password):
        with app.app_context():
            user = User(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return user
    return _create_user
