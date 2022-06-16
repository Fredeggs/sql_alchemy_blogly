from models import User, Post, Tag, PostTag, db
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
p2 = Post(
    title="I love blubber nuggets",
    content="blubber nuggets are good cuz they're chewy",
    user_id=3,
)
p3 = Post(
    title="My name is Ian",
    content="This is the content",
    user_id=1,
)
p4 = Post(
    title="My (Michelle Obama) second post",
    content="My name is STILL Michelle Obama",
    user_id=2,
)

t1 = Tag(name="obama")
t2 = Tag(name="whales")
t3 = Tag(name="first")
t4 = Tag(name="blogly")
t5 = Tag(name="nuggets")

db.session.add_all([u1, u2, u3])
db.session.commit()

db.session.add_all([t1, t2, t3, t4, t5])
db.session.commit()

db.session.add_all([p1, p2, p3, p4])
db.session.commit()

p1.tags.append(t1)
p1.tags.append(t3)
p1.tags.append(t4)
p2.tags.append(t2)
p2.tags.append(t3)
p2.tags.append(t4)
p3.tags.append(t3)
p3.tags.append(t4)
p4.tags.append(t1)
p4.tags.append(t4)
db.session.commit()
