import pandas as pd
import datetime as d

names = pd.read_csv("input.csv")


# city = ['Dallas', 'Allen', 'McKinney', 'Celina', 'Aubrey', 'Little Elm', 'Arlington', 'Grand Prairie', 'Mansfield', 'Forney',
#         'Terrell', 'Rockwell', 'Garland', 'Grapevine', 'Flower mound', 'Lewisville', 'Irving', 'Carrollton', 'Prosper', 'Frisco',
#         'Plano', 'Houston', 'Katy ', 'Cypress', 'Humble', 'Sugar Land', 'The Woodland', 'Conroe', 'Spring', 'Missouri City',
#         'Richmond', 'Fresno', 'Aldine', 'Tomball', 'Cinco Ranch', 'Rosenberg', 'Kingwood', 'Memorial', 'Pearland', 'Friendswood',]
#

def to_csv(data_set, name: str):
    date_time = d.datetime.now()
    dt = date_time.strftime("%d_%m_%y_%H_%M")
    df = pd.DataFrame(data_set)
    df.to_csv(f'intelius_{name}_extraction_{dt}.csv', index=False)
