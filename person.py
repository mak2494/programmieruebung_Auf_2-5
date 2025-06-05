import json
from datetime import datetime

class Person:

    def __init__(self, person_dict) -> None:
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]
        self.gender = person_dict["gender"]

 #Berechnet das Alter der Person
    def calculate_age(self):
        return datetime.today().year - int(self.date_of_birth)
    
#Berchnet die maximale Herzfrequenz der Person basierend auf Alter und Geschlecht
    def calculate_max_heart_rate(self):
        age = self.calculate_age()
        gender = self.gender.lower()

        if gender == "female":
            return round(206 - 0.88 * age) #wird gerundet 
        elif gender == "male":
            return round(208 - 0.7 * age)
        else:
            raise ValueError("Ungültiges Geschlecht – muss 'male' oder 'female' sein.")
#Pfad zum Bild der Person zurückgeben    
    def get_picture_path(self):
        """Gibt den Bildpfad der Person zurück"""
        return self.picture_path
    
        
    @staticmethod
    def load_by_id(person_id):
        """A Function that loads a person by id"""
        person_data = Person.load_person_data()
        for person in person_data:
            if person["id"] == person_id:
                return Person(person)
        return None
           
    @staticmethod
    def load_person_data():
        """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
        file = open("data/person_db.json")
        person_data = json.load(file)
        return person_data

    @staticmethod
    def get_person_list(person_data):
        """A Function that takes the persons-dictionary and returns a list auf all person names"""
        list_of_names = []

        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names
    
    @staticmethod
    def find_person_data_by_name(suchstring):
        """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
        und die die Person als Dictionary zurück gibt"""

        person_data = Person.load_person_data()
        #print(suchstring)
        if suchstring == "None":
            return {}

        two_names = suchstring.split(", ")
        vorname = two_names[1]
        nachname = two_names[0]

        for eintrag in person_data:
            print(eintrag)
            if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
                print()

                return eintrag
        else:
            return {}
        

if __name__ == "__main__":
    #print("This is a module with some functions to read the person data")
    persons = Person.load_person_data()
    person_names = Person.get_person_list(persons)
    #print(person_names)
    #print(Person.find_person_data_by_name("Huber, Julian"))

#Ergänzung 
    person_dict = Person.find_person_data_by_name("Huber, Julian")
    print(person_dict)
    if person_dict:
        person_obj = Person(person_dict)

        age = person_obj.calculate_age()
        print(f"Alter von {person_obj.firstname} {person_obj.lastname}: {age} Jahre")

        max_hf = person_obj.calculate_max_heart_rate()
        print(f"Maximale Herzfrequenz: {max_hf} bpm")
    else:
        print("Person nicht gefunden.")