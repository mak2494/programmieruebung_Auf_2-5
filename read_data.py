import json

def load_person_data():
    """A Function that knows where the person database is and returns a dictionary with the persons"""
    file = open("data/person_db.json")
    person_data = json.load(file)
    return person_data


def get_person_list():
    """A Function that returns a list of persons"""
    person_data = load_person_data()
    person_list = []
    for i in person_data:
        person_list.append(i["firstname"] + " " +i["lastname"])
    return person_list


#Bilder 
def find_person_data_by_name(suchstring):

    person_data = load_person_data()
   
    if suchstring == "None":
        return {}
#Teil den Namen in Vorname und Nachname auf
    two_names = suchstring.split(" ")
    vorname = two_names[0]
    nachname = two_names[1]

    for eintrag in person_data:
        #print(eintrag)
        if (eintrag["firstname"] == vorname and eintrag["lastname"] == nachname):
            #print()

            return eintrag
    else:
        return {}

# Test
# Finden der Person - den String haben wir im Session state
current_person = find_person_data_by_name("Julian Huber")
# Auslesen des Pfades aus dem zurückgegebenen Dictionary
current_picture_path = current_person["picture_path"]
print(current_picture_path)