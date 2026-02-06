from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class User(SQLModel, table=True):
    id: Optional[int] =  Field(default=None, primary_key=True)
    username:str = Field(index=True, unique=True)
    email:str = Field(index=True, unique=True)
    password:str

    todos: list['Todo'] = Relationship(back_populates = "user")
    #can access todo atrributes from user object with line above
    #defines a list of todo tasks that models to the Todo object
    ## Task 3.1 code should go here (special care should go into the indentation)

    ## End of task 3.1 code

    def set_password(self, plaintext_password):
        self.password = password_hash.hash(plaintext_password)

    def __str__(self) -> str:
        return f"(User id={self.id}, username={self.username} ,email={self.email})"



class TodoCategory(SQLModel, table=True):
    # Implementation of the TodoCategory model from task 5.1 here
    todo_id: int|None = Field(primary_key=True, foreign_key = "todo.id")
    category_id: int|None = Field(primary_key = True, foreign_key = 'category.id')
   
class Todo(SQLModel, table=True):
    ## Task 2.1 implementation here. Remove the line below that says "pass" once completed
    id:Optional[int] = Field(default = None, primary_key= True)
    user_id:int = Field(default = None, foreign_key= 'user.id')
    text:str = Field(max_length =255)
    done:bool = Field(default =False)
    #user:User#takes a userobject

    
    
    ## Task 3.2 implementation should go here as well. Modify the class like you did for 3.1 above
    user: User = Relationship(back_populates = "todos")
  #can access other attributes in user object with line above
   
    #line establishes a relationship between a single instance of a todo and its user
    ## Task 3.4 implementation should go here as well
    def toggle(self):
        self.done = not self.done #define instance of toggle object sets it to true when function is called
 # Task 5.2 code should go here
    categories: list['Category'] = Relationship(back_populates ="todos", link_model = TodoCategory)
    #gets a list of todo categories link to that user
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default = None, primary_key = True)
    user_id: int = Field(foreign_key = 'user.id')
    text: str = Field(max_length = 255)

    todos :list['Todo'] = Relationship(back_populates="categories", link_model=TodoCategory)
    # Implementation of the Category model from task 5.1 here
 


    
