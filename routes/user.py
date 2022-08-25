from fastapi import APIRouter, Response, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from starlette.status import HTTP_204_NO_CONTENT


from config.db import get_db
from models.user import users
from schemas.user import User


key = Fernet.generate_key()  # cifrado de claves únicos
f = Fernet(key)
user = APIRouter()

# Endpoint---> Get
@user.get("/users", response_model=list[User], tags=["users"])
def get_all(db: Session = Depends(get_db)):
    return db.execute(users.select()).fetchall()  # consulta toda la tabla

# Endpoint ---> Post
@user.post("/users", response_model=User, tags=["users"])
def create_user(user: User, db: Session = Depends(get_db)):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = f.encrypt(
        user.password.encode("utf-8"))  # cifra el password
    # inserto los datos en la tabla "users"
    result = db.execute(users.insert().values(new_user))
    db.commit()
    return db.execute(users.select().where(users.c.id == result.lastrowid)).first()

#Endpoint ---> Get OnlyOne
@user.get("/users/{id}", response_model=User, tags=["users"])
def get_user(id: str, db: Session = Depends(get_db)):
    return db.execute(users.select().where(users.c.id == id)).first()

#Endpoint ---> Delete
@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str, db: Session = Depends(get_db)):
    db.execute(users.delete().where(users.c.id == id))
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)

#Endpoint ---> Update
@user.put("/users/{id}", response_model=User, tags=["users"])
def update_id(id: str, user: User, db: Session = Depends(get_db)):
    db.execute(users.update().values(name=user.name,
               email=user.email, 
               password=f.encrypt(user.password.encode("utf-8"))).where(users.c.id == id))
    db.commit()
    return db.execute(users.select().where(users.c.id == id)).first()
