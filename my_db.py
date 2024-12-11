from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "UserInformation"
    ID = db.Column(db.Integer, primary_key = True)
    User_ID = db.Column(db.Integer)
    Username = db.Column(db.String(255), nullable=False)
    Email_Address = db.Column(db.String(255), nullable=False)
    Token = db.Column(db.String(255))
    Read_Access = db.Column(db.Integer)
    Write_Access = db.Column(db.Integer)

    def __init__(self, User_ID, Username, Email_Address, Token, Read_Access, Write_Access):
        self.User_ID = User_ID
        self.Username = Username
        self.Email_Address = Email_Address
        self.Token = Token
        self.Read_Access = Read_Access
        self.Write_Access = Write_Access


def delete_all():
    try:
        db.session.query(User).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()


def get_user_row_if_exists(Email_Address):
    get_user_row = User.query.filter_by(Email_Address = Email_Address).first()
    if get_user_row is not None:
        return get_user_row
    else:
        print("That User Does Not Exist")
        return False
    

def add_user_and_login(Username, User_ID, Email_Address):
    row = get_user_row_if_exists(Email_Address)
    if row is not False:
        db.session.commit()
    else:
        new_user = User(Username, User_ID, Email_Address, None, 0, 0)
        db.session.add(new_user)
        db.session.commit()


def add_token(Email_Address, Token):
    row = get_user_row_if_exists(Email_Address)
    if row is not False:
        row.Token = Token
        db.session.commit()


def get_token(Email_Address):
    row = get_user_row_if_exists(Email_Address)
    if row is not False:
        return row.Token
    else:
        print("User With ID: " + Email_Address + " Doesn't Exist")


def delete_revoked_token(Email_Address):
    row = get_user_row_if_exists(Email_Address)
    if row is not False:
        row.Token = None
        db.session.commit()


def view_all_users():
    rows = User.query.all()
    print_results(rows)


def user_logout(Email_Address):
    row = get_user_row_if_exists(Email_Address)
    if row is not False:
        row.login = 0
        db.session.commit()


def print_results(rows):
    for row in rows:
        print(f"{row.User_ID} | {row.Username} | {row.Email_Address}")


def get_all_users():
    rows = User.query.all()
    records = {"User" : []}
    for row in rows:
        records["User"].append([row.User_ID, row.Username, row.Email_Address])
    return records
        

def add_user_permission(Email_Address, Read, Write):
    row = get_user_row_if_exists(Email_Address)
    if row is not False:
        if Read == "true":
            row.Read_Access = 1
        else:
            row.Read_Access = 0
        if Write == "true":
            row.Write_Access = 1
        else:
            row.Write_Access = 0
        db.session.commit()


class Plant(db.Model):
    __tablename__ = "PlantInformation"
    Plant_ID = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(255), nullable=False)
    Plant_Type = db.Column(db.String(255), nullable=False)
    Last_Updated = db.Column(db.DateTime, nullable=False)
    Current_Temperature = db.Column(db.Float, nullable=False)
    Current_Humidity = db.Column(db.Float, nullable=False)
    Current_Soil_Moisture = db.Column(db.Float, nullable=False)
    User_ID = db.Column(db.Integer, nullable=False)

    def __init__(self, Plant_ID, Name, Plant_Type, Last_Updated, Current_Temperature, Current_Humidity, Current_Soil_Moisture, User_ID):
        self.Plant_ID = Plant_ID
        self.Name = Name
        self.Plant_Type = Plant_Type
        self.Last_Updated = Last_Updated
        self.Current_Temperature = Current_Temperature
        self.Current_Humidity = Current_Humidity
        self.Current_Soil_Moisture = Current_Soil_Moisture
        self.User_ID = User_ID

def delete_all_plants():
    try:
        db.session.query(Plant).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()


def get_plant_if_exists(Plant_ID):
    get_plant_row = Plant.query.filter_by(Plant_ID = Plant_ID).first()
    if get_plant_row is not None:
        return get_plant_row
    else:
        print("That Plant Does Not Exist")
        return False


def add_plant(Plant_ID, Name, Last_Updated, Current_Temperature, Current_Humidity, Current_Soil_Moisture, User_ID):
    row = get_plant_if_exists(Plant_ID)
    if row is not False:
        db.session.commit()
    else:
        new_plant = User(Plant_ID, Name, Last_Updated, Current_Temperature, Current_Humidity, Current_Soil_Moisture, User_ID)
        db.session.add(new_plant)
        db.session.commit()


def view_all_plants():
    rows = Plant.query.all()
    print_plants(rows)


def print_plants(rows):
    for row in rows:
        print(f"{row.Plant_ID} | {row.Name} | {row.Last_Updated} | {row.Current_Temperature} | {row.Current_Humidity} | {row.Current_Soil_Moisture} | {row.User_ID}")


class Temperature(db.Model):
    __tablename__ = "TemperatureInformation"
    Current_Temperature = db.Column(db.Float, nullable=False, primary_key = True)
    Max_Temp = db.Column(db.Float, nullable=False)
    Min_Temp = db.Column(db.Float, nullable=False)
    Ideal_Temp = db.Column(db.Float, nullable=False)
    Error_Margin = db.Column(db.Float, nullable=False)

    def __init__(self, Current_Temperature, Max_Temp, Min_Temp, Ideal_Temp, Error_Margin):
        self.Current_Temperature = Current_Temperature
        self.Max_Temp = Max_Temp
        self.Min_Temp = Min_Temp
        self.Ideal_Temp = Ideal_Temp
        self.Error_Margin = Error_Margin
    

def delete_all_temperatures():
    try:
        db.session.query(Temperature).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()


def view_all_temperature():
    rows = Temperature.query.all()
    print_temperature(rows)


def print_temperature(rows):
    for row in rows:
        print(f"{row.Current_Temperature} | {row.Max_Temp} | {row.Min_Temp} | {row.Ideal_Temp} | {row.Error_Margin}")


class Humidity(db.Model):
    __tablename__ = "HumidityInformation"
    Current_Humidity = db.Column(db.Float, nullable=False, primary_key = True)
    Max_Humidity = db.Column(db.Float, nullable=False)
    Min_Humidity = db.Column(db.Float, nullable=False)
    Ideal_Humidity = db.Column(db.Float, nullable=False)
    Error_Margin = db.Column(db.Float, nullable=False)

    def __init__(self, Current_Humidity, Max_Humidity, Min_Humidity, Ideal_Humidity, Error_Margin):
        self.Current_Humidity = Current_Humidity
        self.Max_Humidity = Max_Humidity
        self.Min_Humidity = Min_Humidity
        self.Ideal_Humidity = Ideal_Humidity
        self.Error_Margin = Error_Margin


def delete_all_humidity():
    try:
        db.session.query(Humidity).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()

def view_all_humidity():
    rows = Humidity.query.all()
    print_humidity(rows)


def print_humidity(rows):
    for row in rows:
        print(f"{row.Current_Humidity} | {row.Max_Humidity} | {row.Min_Humidity} | {row.Ideal_Humidity} | {row.Error_Margin}")


class Soil(db.Model):
    __tablename__ = "SoilMoistureInformation"
    Current_Soil_Moisture = db.Column(db.String(255), nullable=False, primary_key = True)
    Above_Moisture = db.Column(db.String(255), nullable=False)
    Below_Moisture = db.Column(db.String(255), nullable=False)
    Soil_Moisture = db.Column(db.Integer, nullable=False)
    Threshold = db.Column(db.Integer, nullable=False)

    def __init__(self, Current_Soil_Moisture, Above_Moisture, Below_Moisture, Soil_Moisture, Threshold):
        self.Current_Soil_Moisture = Current_Soil_Moisture
        self.Above_Moisture = Above_Moisture
        self.Min_Below_MoistureTemp = Below_Moisture
        self.Soil_Moisture = Soil_Moisture
        self.Threshold = Threshold  


def delete_all_soil():
    try:
        db.session.query(Soil).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()

def view_all_humidity():
    rows = Soil.query.all()
    print_soil(rows)


def print_soil(rows):
    for row in rows:
        print(f"{row.Current_Soil_Moisture} | {row.Above_Moisture} | {row.Below_Moisture} | {row.Soil_Moisture} | {row.Threshold}")
