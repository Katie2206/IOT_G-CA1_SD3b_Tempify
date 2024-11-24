from flask_mongoengine import MongoEngine

db = MongoEngine()

class User(db.Document):
    User_ID = db.IntField(required=True)
    Username = db.StringField(required=True)
    Password = db.StringField(required=True)
    Email_Address = db.StringField(required=True)
    Auth_Key = db.StringField(required=True)


def delete_all():
    try:
        User.objects({}).delete()
        print("Users Have Been Deleted")
    except Exception as e:
        print("Deletion Failed: " + str(e))


def get_user_row_if_exists(User_ID):
    get_user_row = User.objects(User_ID = User_ID).first()
    if get_user_row is not None:
        return get_user_row
    else:
        print("That User Does Not Exist")
        return False
    

def add_user_and_login(Username, User_ID, Password, Email_Address):
    row = get_user_row_if_exists(User_ID)
    if row is not False:
        print("User Already Exists")
    else:
        ("Creating User: " + Username)
        User(Username = Username, User_ID = User_ID, Password = Password, Email_Address = Email_Address).save()


def view_all_users():
    rows = User.objects.all()
    print_results(rows)


def print_results(rows):
    for row in rows:
        print(f"{row.User_ID} | {row.Username} | {row.Password} | {row.Email_Address}")
        

class Plant(db.Document):
    Plant_ID = db.IntField(required=True)
    Name = db.StringField(required=True)
    Plant_Type = db.StringField(required=True)
    Last_Updated = db.DateTimeField(default = datetime.utcnow)
    Current_Temperature = db.FloatField(required=True)
    Current_Humidity = db.FloatField(required=True)
    Current_Soil_Moisture = db.FloatField(required=True)
    User_ID = db.IntField(required=True)


def delete_all_plants():
    try:
        Plant.objects({}).delete()
        print("Plants Have Been Deleted")
    except Exception as e:
        print("Deletion Failed: " + str(e))


def get_plant_if_exists(Plant_ID):
    get_plant_row = Plant.objects(Plant_ID = Plant_ID).first()
    if get_plant_row is not None:
        return get_plant_row
    else:
        print("That Plant Does Not Exist")
        return False


def add_plant(Plant_ID, Name, Last_Updated, Current_Temperature, Current_Humidity, Current_Soil_Moisture, User_ID):
    row = get_plant_if_exists(Plant_ID)
    if row is not False:
        print("Plant Already Exists")
    else:
        ("Creating Plant: " + Name)
        Plant(Plant_ID, Name, Last_Updated, Current_Temperature, Current_Humidity, Current_Soil_Moisture, User_ID)
    print("Plant " + Name + " Added!")


def view_all_plants():
    rows = Plant.objects.all()
    print_plants(rows)


def print_plants(rows):
    for row in rows:
        print(f"{row.Plant_ID} | {row.Name} | {row.Last_Updated} | {row.Current_Temperature} | {row.Current_Humidity} | {row.Current_Soil_Moisture} | {row.User_ID}")


class Temperature(db.Document):
    Current_Temperature = db.FloatField(required=True)
    Max_Temp = db.FloatField(required=True)
    Min_Temp = db.FloatField(required=True)
    Ideal_Temp = db.FloatField(required=True)
    Error_Margin = db.FloatField(required=True)

    
def delete_all_temperatures():
    try:
        Temperature.objects({}).delete()
        print("Temperatures Have Been Deleted")
    except Exception as e:
        print("Deletion Failed: " + str(e))


def view_all_temperature():
    rows = Temperature.objects.all()
    print_temperature(rows)


def print_temperature(rows):
    for row in rows:
        print(f"{row.Current_Temperature} | {row.Max_Temp} | {row.Min_Temp} | {row.Ideal_Temp} | {row.Error_Margin}")


class Humidity(db.Document):
    Current_Humidity = db.FloatField(required=True)
    Max_Humidity = db.FloatField(required=True)
    Min_Humidity = db.FloatField(required=True)
    Ideal_Humidity = db.FloatField(required=True)
    Error_Margin = db.FloatField(required=True)


def delete_all_humidity():
    try:
        Humidity.objects({}).delete()
        print("Humidity Has Been Deleted")
    except Exception as e:
        print("Deletion Failed: " + str(e))

def view_all_humidity():
    rows = Humidity.objects.all()
    print_humidity(rows)


def print_humidity(rows):
    for row in rows:
        print(f"{row.Current_Humidity} | {row.Max_Humidity} | {row.Min_Humidity} | {row.Ideal_Humidity} | {row.Error_Margin}")


class Soil(db.Document):
    Current_Soil_Moisture = db.StringField(required=True)
    Above_Moisture = db.FloatField(required=True)
    Below_Moisture = db.FloatField(required=True)
    Soil_Moisture = db.IntField(required=True)
    Threshold = db.IntField(required=True)


def delete_all_soil():
    try:
        Soil.objects({}).delete()
        print("Soil Moisture Has Been Deleted")
    except Exception as e:
        print("Deletion Failed: " + str(e))

def view_all_soil():
    rows = Soil.objects.all()
    print_soil(rows)


def print_soil(rows):
    for row in rows:
        print(f"{row.Current_Soil_Moisture} | {row.Above_Moisture} | {row.Below_Moisture} | {row.Soil_Moisture} | {row.Threshold}")