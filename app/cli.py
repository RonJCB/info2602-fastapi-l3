import typer
from app.database import create_db_and_tables, get_session, drop_all
from app.models import User, Todo, Category
from fastapi import Depends
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

cli = typer.Typer()


@cli.command()
def initialize():
    with get_session() as db: # Get a connection to the database
        drop_all() # delete all tables
        create_db_and_tables() #recreate all tables
        
        bob = User(username='bob', email='bob@mail.com') # Create a new user (in memory)
        bob.set_password("bobpass")

        db.add(bob) # Tell the database about this new data
        db.commit() # Tell the database persist the data
        db.refresh(bob) # Update the user (we use this to get the ID from the db)

        new_todo = Todo(text='Wash dishes', user_id=bob.id)

        db.add(new_todo) # Tell the database about this new data
        db.commit() # Tell the database persist the data
        db.refresh(new_todo) # Update the user (we use this to get the ID from the db)
       
        print("Database Initialized")

@cli.command()
#Output each todo's ID, text, username and done status.
def output_todo():#assuming no parameters and we want all the possible todos and not specifically a specific user
    with get_session() as db:
        todos = db.exec(select(Todo)).all()
        if not todos:
            print("Todos not found in database")
            return
        for todo in todos:
            print(f"Text: {todo.text}, Status:{todo.done}, TodoId:{todo.id}, username: {todo.user.username}")
@cli.command()
#Delete a todo by ID.
def delete_todo(todo_id:int):#delete a todo by ID assuming we dont haave the username
    with get_session() as db:
        todo = db.exec(select(Todo).where(Todo.id == todo_id)).one_or_none()
        if not todo:
            print("Todo not found in database")
            return
        #if not todo.user.username == username:
         #   print("Todo not found to that user")
          #  return
        db.delete(todo)
        db.commit()
        print("Todo deleted successfully")
@cli.command()
#Mark all of a user's todos as complete
def todo_completed(user_id:int):
    with get_session() as db:
        user = db.exec(select(User).where(User.id== user_id)).one_or_none()

        if not user:
            print("user not found")
            return
        
        todos = db.exec(select(Todo).where(Todo.user_id == user_id)).all()
       # print(todos)
        for todo in todos:
            todo.done = True#can set todo.done to True or toggle todo
            db.add(todo)#persis changes on database
            db.commit()
        
        print("All todos set to completed")
        
@cli.command()
def add_task(username:str, task:str):
    # Task 4.1 code here. Remove the line with "pass" below once completed
        with get_session() as db:
            user = db.exec(select(User).where(User.username == username)).first()#or one_or_none()
            if not user:
                print(f"{username} not found in database")
                return
            user.todos.append(Todo(text =task))#initialize relationship
            db.add(user)
            db.commit()#add user to db
            print("Task added for a user")

@cli.command()
def toggle_todo(todo_id:int, username:str):
    # Task 4.2 code here. Remove the line with "pass" below once completed
    with get_session() as db:
       todo = db.exec(select(Todo).where(Todo.id == todo_id)).one_or_none()#
       if not todo:
           print(f"Todo ID {todo_id} not found in db")
           return
       if (todo.user.username !=username):
          print(f"{username} does not have that todo or does not exist in db")
          return
       todo.toggle()
       db.add(todo)
       db.commit()
       print(f"Todo  task set to {todo.done} ")
        

@cli.command()
def list_todo_categories(todo_id:int, username:str):
    # Task 5.3 code here. Remove the line with "pass" below once completed
    with get_session() as db:
        todo = db.exec(select(Todo).where(Todo.id == todo_id)).one_or_none()
        if not todo:
            print(f"Todo ID{todo_id} not found in database")
            return
        elif not todo.user.username == username:
            print(f"{username} does not that have todo")
        else:
            print(f"{username} Todo Categories: {todo.categories}")

@cli.command()
def create_category(username:str, cat_text:str):        
    # Task 5.4 code here. Remove the line with "pass" below once completed
    with get_session() as db:
        user = db.exec(select(User).where(User.username == username)).one_or_none()
        if not user:
            print(f"{username} not found in db")
        category = db.exec(select(Category).where(Category.text == cat_text, Category.user.id == user.id )).one_or_none()
        #can compare string text along with userid to see if there exist a category tied to that user
        if  category:
            print(f"{username} have a todo of that category")
        
        category = Category(text = cat_text, user_id = user.id)
        db.add(category)
        db.commit()
        print("Category added for the user")
@cli.command()
def list_user_categories(username:str):
    # Task 5.5 code here. Remove the line with "pass" below once completed
    with get_session() as db:
        user = db.exec(select(User).where(User.username == username)).one_or_none()
        if not user:
            print("User do not exist")
            return
        print("Listing all categories....")
        allcategories = db.exec(select(Category).where(Category.user_id == username)).all()
        for category in allcategories:
            print(category.text)


@cli.command()
def assign_category_to_todo(username:str, todo_id:int, category_text:str):
    # Task 5.6 code here. Remove the line with "pass" below once completed
    with get_session() as db:
        user = db.exec(select(User).where(User.username == username)).one_or_none()
        if not user:
            print(f"{username} does not exist")
            return
       
        category = db.exec(select(Category).where(Category.user_id == user.id, 
                                                  Category.text == category_text))  
        if category:
            print("Category already created")
        newCategory = Category(user_id = username , text = category_text)
        db.add(newCategory)
        db.commit()

        todo = db.exec(select(Todo).where(Todo.id == todo_id)).one_or_none()
        if not todo:
            print(f"todo doesnt exist yet for {username}")
            return
        todo.categories.append(category)#add new catory to the todo list link
        db.add(todo)
        db.commit()
        print(f"Added category {category_text} to todo {todo.text}")
#11. Conclusion
#Thus concludes your introduction to flask-sqlalchemy. The usage of this library is at the very core of this course.

#You can view a completed version of this lab at the following link

if __name__ == "__main__":
    cli()
