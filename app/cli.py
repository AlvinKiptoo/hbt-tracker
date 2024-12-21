import click
from app.database import SessionLocal, engine
from app.models import Base, User, Habit

@click.group()
def cli():
    """Habit Tracker CLI"""
    pass

@cli.command()
def init_db():
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)
    click.echo("Database initialized!")

@cli.command()
@click.argument("name")
def add_user(name):
    """Add a new user."""
    session = SessionLocal()
    try:
        user = User(name=name)
        session.add(user)
        session.commit()
        click.echo(f"User '{name}' added!")
    finally:
        session.close()

@cli.command()
@click.argument("user_id", type=int)
@click.argument("name")
@click.argument("frequency")
@click.option("--description", default="", help="Optional description")
def add_habit(user_id, name, frequency, description):
    """Add a new habit."""
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            click.echo(f"User with ID {user_id} does not exist.")
            return
        habit = Habit(user_id=user_id, name=name, frequency=frequency, description=description)
        session.add(habit)
        session.commit()
        click.echo(f"Habit '{name}' added for user ID {user_id}.")
    finally:
        session.close()

@cli.command()
def list_users():
    """List all users."""
    session = SessionLocal()
    try:
        users = session.query(User).all()
        if not users:
            click.echo("No users found.")
        else:
            for user in users:
                click.echo(f"ID: {user.id}, Name: {user.name}")
    finally:
        session.close()

@cli.command()
@click.argument("user_id", type=int)
def view_habits(user_id):
    """View all habits for a user."""
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            click.echo(f"User with ID {user_id} does not exist.")
            return
        habits = session.query(Habit).filter(Habit.user_id == user_id).all()
        if not habits:
            click.echo(f"No habits found for user ID {user_id}.")
        else:
            for habit in habits:
                click.echo(f"ID: {habit.id}, Name: {habit.name}, Frequency: {habit.frequency}, Description: {habit.description}")
    finally:
        session.close()

@cli.command()
@click.argument("habit_id", type=int)
@click.argument("name")
@click.argument("frequency")
@click.option("--description", default="", help="Optional description")
def update_habit(habit_id, name, frequency, description):
    """Update a habit."""
    session = SessionLocal()
    try:
        habit = session.query(Habit).filter(Habit.id == habit_id).first()
        if not habit:
            click.echo(f"Habit with ID {habit_id} does not exist.")
            return
        habit.name = name
        habit.frequency = frequency
        habit.description = description
        session.commit()
        click.echo(f"Habit '{habit_id}' updated!")
    finally:
        session.close()

@cli.command()
@click.argument("habit_id", type=int)
def delete_habit(habit_id):
    """Delete a habit."""
    session = SessionLocal()
    try:
        habit = session.query(Habit).filter(Habit.id == habit_id).first()
        if not habit:
            click.echo(f"Habit with ID {habit_id} does not exist.")
            return
        session.delete(habit)
        session.commit()
        click.echo(f"Habit '{habit_id}' deleted!")
    finally:
        session.close()

@cli.command()
def analytics():
    """Show analytics of habits for all users."""
    session = SessionLocal()
    try:
        users = session.query(User).all()
        for user in users:
            habit_count = session.query(Habit).filter(Habit.user_id == user.id).count()
            click.echo(f"User: {user.name} (ID: {user.id}) has {habit_count} habit(s).")
    finally:
        session.close()
