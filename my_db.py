from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Plant(db.Model):
    __tablename__ = "PlantInformation"
    Plant_ID = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(255), nullable=False)
    Plant_Type = db.Column(db.String(255), nullable=False)
    Last_Updated = db.Column(db.String(255), nullable=False)
    Current_Temperature = db.Column(db.Float, nullable=False)
    Current_Humidity = db.Column(db.Float, nullable=False)
    Current_Soil_Moisture = db.Column(db.String, nullable=False)
    # Token = db.Column(db.String(255))

    def __init__(self, Plant_ID, Name, Plant_Type, Last_Updated, Current_Temperature, Current_Humidity, Current_Soil_Moisture):
        self.Plant_ID = Plant_ID
        self.Name = Name
        self.Plant_Type = Plant_Type
        self.Last_Updated = Last_Updated
        self.Current_Temperature = Current_Temperature
        self.Current_Humidity = Current_Humidity
        self.Current_Soil_Moisture = Current_Soil_Moisture
        # self.Token = Token

def delete_all_plants():
    try:
        db.session.query(Plant).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()


def get_plant_id(Plant_ID):
    get_plant = Plant.query.filter_by(Plant_ID = Plant_ID).first()
    if get_plant is not None:
        return get_plant.Plant_ID
    else:
        print("No Plant ID")
        return False


def get_plant_if_exists(Plant_ID):
    get_plant_row = Plant.query.filter_by(Plant_ID = Plant_ID).first()
    if get_plant_row is not None:
        return get_plant_row
    else:
        print("That Plant Does Not Exist")
        return False


def add_plant(Plant_ID, Name, Last_Updated, Current_Temperature, Current_Humidity, Current_Soil_Moisture):
    row = get_plant_if_exists(Plant_ID)
    if row is not False:
        db.session.commit()
    else:
        new_plant = Plant(Plant_ID, Name, Last_Updated, Current_Temperature, Current_Humidity, Current_Soil_Moisture)
        db.session.add(new_plant)
        db.session.commit()


def update_plant(Plant_ID, Last_Updated, Current_Temperature, Current_Humidity, Current_Soil_Moisture):
    row = get_plant_if_exists(Plant_ID)
    if row is not False:
        updated_plant = Plant(Plant_ID, Last_Updated, Current_Temperature, Current_Humidity, Current_Soil_Moisture)
        db.session.update(updated_plant)
        db.session.commit()
    else:
        print("That Plant Does Not Exist To Update")
        return False


def view_all_plants():
    rows = Plant.query.all()
    print_plants(rows)


def print_plants(rows):
    for row in rows:
        print(f"{row.Plant_ID} | {row.Name} | {row.Last_Updated} | {row.Current_Temperature} | {row.Current_Humidity} | {row.Current_Soil_Moisture}")


def add_token(Plant_ID, Token):
    row = get_plant_if_exists(Plant_ID)
    if row is not False:
        row.Token = Token
        db.session.commit()


def get_token(Plant_ID):
    row = get_plant_if_exists(Plant_ID)
    if row is not False:
        return row.Token
    else:
        print("Plant With ID: " + Plant_ID + " Doesn't Exist")


def delete_revoked_token(Plant_ID):
    row = get_plant_if_exists(Plant_ID)
    if row is not False:
        row.Token = None
        db.session.commit()


class Temperature(db.Model):
    __tablename__ = "TemperatureInformation"
    Temperature_ID = db.Column(db.Integer, primary_key = True)
    Current_Temperature = db.Column(db.Float, nullable=False, primary_key = True)
    Max_Temp = db.Column(db.Float, nullable=False)
    Min_Temp = db.Column(db.Float, nullable=False)
    Ideal_Temp = db.Column(db.Float, nullable=False)
    Error_Margin = db.Column(db.Float, nullable=False)

    def __init__(self, Temperature_ID, Current_Temperature, Max_Temp, Min_Temp, Ideal_Temp, Error_Margin):
        self.Temperature_ID = Temperature_ID
        self.Current_Temperature = Current_Temperature
        self.Max_Temp = Max_Temp
        self.Min_Temp = Min_Temp
        self.Ideal_Temp = Ideal_Temp
        self.Error_Margin = Error_Margin
    

def get_temp_if_exists(Temperature_ID):
    get_temp_row = Temperature.query.filter_by(Temperature_ID = Temperature_ID).first()
    if get_temp_row is not None:
        return get_temp_row
    else:
        print("That Temperature Does Not Exist")
        return False


def update_temp(Temperature_ID, Current_Temperature):
    row = get_temp_if_exists(Temperature_ID)
    if row is not False:
        row.Current_Temperature = Current_Temperature
        db.session.commit()
    else:
        print("That Temperature Does Not Exist To Update")
        return False

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
    Humidity_ID = db.Column(db.Integer, primary_key = True)
    Current_Humidity = db.Column(db.Float, nullable=False, primary_key = True)
    Max_Humidity = db.Column(db.Float, nullable=False)
    Min_Humidity = db.Column(db.Float, nullable=False)
    Ideal_Humidity = db.Column(db.Float, nullable=False)
    Error_Margin = db.Column(db.Float, nullable=False)

    def __init__(self, Humidity_ID, Current_Humidity, Max_Humidity, Min_Humidity, Ideal_Humidity, Error_Margin):
        self.Humidity_ID = Humidity_ID
        self.Current_Humidity = Current_Humidity
        self.Max_Humidity = Max_Humidity
        self.Min_Humidity = Min_Humidity
        self.Ideal_Humidity = Ideal_Humidity
        self.Error_Margin = Error_Margin


def get_humidity_if_exists(Humidity_ID):
    get_humidity_row = Humidity.query.filter_by(Humidity_ID = Humidity_ID).first()
    if get_humidity_row is not None:
        return get_humidity_row
    else:
        print("That Humidity Does Not Exist")
        return False


def update_humidity(Humidity_ID, Current_Humidity):
    row = get_plant_if_exists(Humidity_ID)
    if row is not False:
        updated_humidity = Humidity(Current_Humidity)
        db.session.update(updated_humidity)
        db.session.commit()
    else:
        print("That Plant Does Not Exist To Update")
        return False


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
    Soil_ID = db.Column(db.Integer, primary_key = True)
    Current_Soil_Moisture = db.Column(db.String(255), nullable=False, primary_key = True)
    Ideal_Moisture_Level = db.Column(db.String(255), nullable=False)

    def __init__(self, Soil_ID, Current_Soil_Moisture, Ideal_Moisture_Level):
        self.Soil_ID = Soil_ID
        self.Current_Soil_Moisture = Current_Soil_Moisture
        self.Ideal_Moisture_Level = Ideal_Moisture_Level


def get_soil_if_exists(Soil_ID):
    get_soil_row = Soil.query.filter_by(Soil_ID = Soil_ID).first()
    if get_soil_row is not None:
        return get_soil_row
    else:
        print("That Soil Moisture Does Not Exist")
        return False


def delete_all_soil():
    try:
        db.session.query(Soil).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()

def view_all_soil():
    rows = Soil.query.all()
    print_soil(rows)


def print_soil(rows):
    for row in rows:
        print(f"{row.Current_Soil_Moisture} | {row.Ideal_Moisture_Level}")


def update_soil(Soil_ID, Current_Soil_Moisture):
    row = get_soil_if_exists(Soil_ID)
    if row is not False:
        updated_soil = Soil(Current_Soil_Moisture)
        db.session.update(updated_soil)
        db.session.commit()
    else:
        print("That Soil Moisture Does Not Exist To Update")
        return False
