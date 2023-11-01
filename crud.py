__version__=1.0
__author__='Ioannis Tsakmakis'
__date_created__='2023-10-31'

import mysql_app.schemas as schemas, mysql_app.models as models
from mysql_app.engine import engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import text, or_

# User Management

class User:
    
    @staticmethod
    def add(user: schemas.UsersTableCreate, db: Session=sessionmaker(bind=engine, expire_on_commit=True)()):
        new_user = models.Users(name=user.name, email=user.email, subscription_expires_in=user.subscription_expires_in)
        db.add(new_user)
        db.commit()

    @staticmethod
    def get_by_name(name: str, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        return db.query(models.Users).filter_by(name=name).first()
    
    @staticmethod
    def get_by_id(id: int, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        return db.query(models.Users).filter_by(id=id).first()
    
    @staticmethod
    def get_by_email(email: str, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        return db.query(models.Users).filter_by(email=email).first()
    
class Stations:

    @staticmethod
    def add(station: schemas.StationsCreate, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        new_station = models.Stations(brand=station.brand, model=station.model, code=station.code, date_created=station.date_created,
                                      longitude=station.longitude, latitude=station.latitude, elevation=station.elevation,
                                      access=station.access, name=station.name, icon_type=station.icon_type)
        db.add(new_station)
        db.commit()

    @staticmethod
    def get_by_code(code: str, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        return db.query(models.Stations).filter_by(code = code).first()
    
    @staticmethod
    def get_by_brand(brand: str, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        return db.query(models.Stations).filter_by(brand = brand).all()
    
    @staticmethod
    def get_by_access(user_id: int, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        result = db.query(models.Stations).filter(text("JSON_CONTAINS(JSON_UNQUOTE(JSON_EXTRACT(access, '$.users')), CAST(:user AS JSON), '$')").params(user=user_id)).all()
        return result
    
    @staticmethod
    def update_date_created(station_id: int, new_entry: str, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        station=db.query(models.Stations).filter_by(id=station_id).first()
        if station is not None:
            station.date_created=new_entry
            db.commit()
        else:
            db.close()
    
    @staticmethod
    def delete_by_code(code: str, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        result = db.query(models.Stations).filter_by(code = code).first()
        if result is not None:
            db.delete(result)
            db.commit()
        else: db.close()

    
class Gateways:

    @staticmethod
    def add(gateway: schemas.GatewaysCreate, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        new_gateway = models.GateWays(brand= gateway.brand, model=gateway.model, code=gateway.code,
                                      name = gateway.name, station_id=gateway.station_id)
        db.add(new_gateway)
        db.commit()

    @staticmethod
    def get_by_code(code: str, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        return db.query(models.GateWays).filter_by(code=code).first()
    
class RemoteTerminalUnits:

    @staticmethod
    def add(rtu: schemas.RemoteTerminalUnitsCreate, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        new_rtu = models.RemoteTerminalUnits(brand=rtu.brand, model=rtu.model, code=rtu.code, longitude=rtu.longitude,
                                             latitude=rtu.latitude, elevation=rtu.elevation,name=rtu.name, station_id=rtu.station_id)
        db.add(new_rtu)
        db.commit()

    @staticmethod
    def get_by_code(code: str, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        return db.query(models.RemoteTerminalUnits).filter_by(code = code).first()
    
    @staticmethod
    def get_by_station_id(station_id: int, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        return db.query(models.RemoteTerminalUnits).filter_by(station_id=station_id).first()
    
class SensorsMeters:

    @staticmethod
    def add(sensor_meter: schemas.SensorsMetersCreate, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        new_sensor_meter = models.SensorsMeters(type=sensor_meter.type, measurement=sensor_meter.measurement, unit=sensor_meter.unit,
                                                gauge_height=sensor_meter.gauge_height, name =sensor_meter.name,
                                                code=sensor_meter.code, station_id=sensor_meter.station_id, rtu_id=sensor_meter.rtu_id)
        db.add(new_sensor_meter)
        db.commit()

    @staticmethod
    def get_by_station_id(station_id: int, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        rtus = db.query(models.RemoteTerminalUnits).filter_by(station_id=station_id).first()
        if rtus is None:
            return db.query(models.SensorsMeters).filter_by(station_id=station_id).all()
        else:
            return db.query(models.SensorsMeters).filter(or_(models.SensorsMeters.station_id==station_id,
                                                            models.SensorsMeters.rtu_id.in_(rtus.id))).all()
    
    @staticmethod
    def get_by_rtu_id(rtu_id: int, db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        return db.query(models.SensorsMeters).filter_by(rtu_id=rtu_id).all()
    
    @staticmethod
    def get_by_station_id_and_rtu_id(station_id: int, rtu_id: int,db: Session=sessionmaker(bind=engine,expire_on_commit=True)()):
        return db.query(models.SensorsMeters).filter_by(station_id=station_id,rtu_id=rtu_id).all()
    
    @staticmethod
    def get_by_id(id: int, db: Session = sessionmaker(bind=engine,expire_on_commit=True)()):
        return db.query(models.SensorsMeters).filter_by(id = id).first()

class MeasurementsTranslations:

    @staticmethod
    def add(translation: schemas.MeasurementTranslationsCreate, db: Session=sessionmaker(bind=engine, expire_on_commit=True)()):
        new_translation = models.MeasurementTranslations(measurement=translation.measurement, el=translation.el, en=translation.en)
        db.add(new_translation)
        db.commit()
    
    @staticmethod
    def get_translation_by_measurement(measurement: str, db: Session=sessionmaker(bind=engine, expire_on_commit=True)()):
        return db.query(models.MeasurementTranslations).filter_by(measurement=measurement).first()


                  