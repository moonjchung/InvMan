import typer
from app.db.session import SessionLocal
from app.crud import create_user_by_admin
from app.schemas.user import UserCreateByAdmin

app = typer.Typer()

@app.command()
def create_user(email: str, password: str, role: str = "staff"):
    """
    Create a new user.
    """
    db = SessionLocal()
    user_in = UserCreateByAdmin(email=email, password=password, role=role)
    user = create_user_by_admin(db, user=user_in)
    db.close()
    print(f"User {user.email} created with role {user.role}")

if __name__ == "__main__":
    app()
