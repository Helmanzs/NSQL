from poll import Poll
from user import User
from databaseClient import Database

users_data = [
    ("kaja", "kaja", "kaja@kaja.cz"),
    ("pepa", "pepa", "pepa@pepa.cz"),
    ("franta", "franta", "franta@franta.cz")
]

polls_data = [
    ("What is your favorite color?", ["Red", "Blue", "Green"], "kaja"),
    ("Which programming language do you prefer?", ["Python", "JavaScript", "Java", "C++"], "pepa"),
    ("What is your favorite food?", ["Pizza", "Burger", "Sushi", "Tacos"], "franta")
]

def populate_db(db: Database):
    for user_data in users_data:
        username, password, email = user_data
        db.register(username, password, email)
    
    users = db.get_users()
    for user in users:
        print(user)

    for poll_data in polls_data:
        question, options, username = poll_data
        db.submit_poll(question, options, username)

    polls = db.get_polls()
    for poll in polls:
        print(poll)