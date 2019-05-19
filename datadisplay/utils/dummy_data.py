from datadisplay.models import Students, Teams, Projects, NotForProfits
from random import randint

# Some constants to use
DEFAULT_DATA_LENGTH = 10

NAMES = ['Adam', 'Bella', 'Carl', 'Dmitri', 'Elena', 'Fabio', 'Ginny', 'Horace', 'Ivanka', 'Jim']
DISCIPLINES = ['Kinesiology', 'Linguistics', 'Mechanical Engineering', 'Nursing']
PROJECTS = ['Operation Collect Data', 'Python For The People', 'Questions?']
TEAMS = ['Rewards Team', 'Software Team', 'Training Team']
CLIENTS = ['Ursula', 'Vincent', 'Winston', 'Xavier', 'Yasmin', 'Zachary']


# These functions will generate a completely default dataset
def generate_default_students():
    for i in range(DEFAULT_DATA_LENGTH):
        name = NAMES[randint(0, len(NAMES)-1)]
        new_student = Students(
            student_id=randint(100000000, 9999999999),
            name=name,
            email=name.lower() + '@mail.utoronto.ca',
            discipline=DISCIPLINES[randint(0, len(DISCIPLINES)-1)],
            year=randint(1, 4),
            phone=randint(4160000000, 6479999999),
            interview_offer=randint(1, 2) % 2 == 0,
            project_name=PROJECTS[randint(0, len(PROJECTS)-1)]
        )
        new_student.save()


def generate_default_teams():
    pass


def generate_default_projects():
    pass


def generate_default_nfps():
    pass


# These functions will generate a dataset that contains a list of pre-defined data
def generate_w_partial_students(existing_students):
    pass


def generate_w_partial_teams(existing_teams):
    pass


def generate_w_partial_projects(existing_projects):
    pass


def generate_w_partial_nfps(existing_nfps):
    pass

