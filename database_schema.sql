CREATE DATABASE Tempify;
USE Tempify;

DROP TABLE IF EXISTS PlantInformation;

CREATE TABLE PlantInformation(
	Plant_ID int NOT NULL AUTO_INCREMENT,
	Name varchar(255),
	Plant_Type varchar(255),
	Last_Updated datetime NOT NULL,
	Current_Temperature float,
	Current_Humidity float,
	Current_Soil_Moisture varchar(255),
	User_ID int,
	PRIMARY KEY(Plant_ID),
	FOREIGN KEY(User_ID) REFERENCES UserInformation,
	FOREIGN KEY(Current_Temperature) REFERENCES TemperatureInformation,
	FOREIGN KEY(Current_Humidity) REFERENCES HumidityInformation,
	FOREIGN KEY(Current_Soil_Moisture) REFERENCES SoilMoistureInformation
);

DROP TABLE IF EXISTS UserInformation;

CREATE TABLE UserInformation(
	User_ID int NOT NULL AUTO_INCREMENT,
	Username varchar(255),
	Password varchar(255),
	Email_Address varchar(255),
	PRIMARY KEY(User_ID)
);

DROP TABLE IF EXISTS TemperatureInformation;

CREATE TABLE TemperatureInformation(
	Current_Temperature float,
	Max_Temp float,
	Min_Temp float,
	Ideal_Temp float,
	Error_Margin float,
	PRIMARY KEY(Current_Temperature),
	FOREIGN KEY(Plant_ID) REFERENCES PlantInformation
);

DROP TABLE IF EXISTS HumidityInformation;

CREATE TABLE HumidityInformation(
	Current_Humidity float,
	Max_Humidity float,
	Min_Humidity float,
	Ideal_Humidity float,
	Error_Margin float,
	PRIMARY KEY(Current_Humidity),
	FOREIGN KEY(Plant_ID) REFERENCES PlantInformation
);

DROP TABLE IF EXISTS SoilMoistureInformation;

CREATE TABLE SoilMoistureInformation(
	Current_Soil_Moisture varchar(255),
	Above_Moisture varchar(255),
	Below_Moisture varchar(255),
	Soil_Moisture int,
	Threshold int,
	PRIMARY KEY(Current_Soil_Moisture),
	FOREIGN KEY(Plant_ID) REFERENCES PlantInformation
);
