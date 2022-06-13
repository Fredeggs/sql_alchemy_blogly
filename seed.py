from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

u1 = User(first_name="Bobins", last_name="Dauphinais")
u2 = User(
    first_name="Michelle",
    last_name="Obama",
    image_url="https://www.biography.com/.image/t_share/MTczNjEwODI2NTg5MDg3MTI0/michelle-obama-gettyimages-85246899.jpg",
)
u3 = User(
    first_name="Doug",
    last_name="Dimadome",
    image_url="https://m.media-amazon.com/images/I/61VoRhtW9lL._AC_SL1000_.jpg",
)

p1 = Post(
    title="My (Michelle Obama) first post",
    content="Hello my name is Michelle Obama",
    user_id=2,
)

db.session.add_all([u1, u2, u3])
db.session.commit()

db.session.add(p1)
db.session.commit()
