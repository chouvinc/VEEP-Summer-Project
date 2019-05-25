from data_display.models import Students, Teams, Projects, NotForProfits
from random import randint, uniform

# Some constants to use
DEFAULT_DATA_LENGTH = 10

NAMES = ['Adam', 'Bella', 'Carl', 'Dmitri', 'Elena', 'Fabio', 'Ginny', 'Horace', 'Ivanka', 'Jim']
DISCIPLINES = ['Kinesiology', 'Linguistics', 'Mechanical Engineering', 'Nursing']
PROJECTS = ['Operation Collect Data', 'Python For The People', 'Questions?']
TEAMS = ['Rewards Team', 'Software Team', 'Training Team']
CLIENTS = ['Ursula', 'Vincent', 'Winston', 'Xavier', 'Yasmin', 'Zachary']
PROJECT_TYPES = ['Software', 'Mechanical', 'Hardware', 'Consulting', 'Operations', 'Energy', 'Other']


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
    for i in range(DEFAULT_DATA_LENGTH):
        num_members = randint(3, 6)

        sum_years = 0
        for j in range(num_members):
            sum_years += randint(1, 4)

        avg_yos = sum_years/4

        new_team = Teams(
            team_name=TEAMS[randint(0, len(TEAMS)-1)],
            num_members=num_members,
            avg_yos=avg_yos,
            most_common_discipline=DISCIPLINES[randint(0, len(DISCIPLINES)-1)]
        )

        new_team.save()


def generate_default_projects():
    for i in range(DEFAULT_DATA_LENGTH):
        new_project = Projects(
            project_name=PROJECTS[randint(0, len(PROJECTS)-1)],
            client_name=CLIENTS[randint(0, len(CLIENTS)-1)],
            completion_rate=uniform(0, 100),
            project_type=PROJECT_TYPES[randint(0, len(PROJECT_TYPES)-1)]
        )

        new_project.save()


def generate_default_nfps():
    for i in range(DEFAULT_DATA_LENGTH):
        num_projects = randint(1, 3)
        nfp_name = CLIENTS[randint(0, len(CLIENTS)-1)]
        new_nfp = NotForProfits(
            nfp_name=nfp_name,
            years_w_veep=randint(0, 6),
            num_projects=num_projects,
            num_projects_completed=randint(0, num_projects),
            primary_email=nfp_name.lower() + '@gmail.com'
        )

        new_nfp.save()


# These functions will generate a dataset that contains a list of pre-defined data
def generate_w_partial_students(existing_students):
    pass


def generate_w_partial_teams(existing_teams):
    pass


def generate_w_partial_projects(existing_projects):
    pass


def generate_w_partial_nfps(existing_nfps):
    pass


# Generate dummy data
def generate_dummy_data():
    for i in range(10):
        generate_default_nfps()
        generate_default_projects()
        generate_default_teams()
