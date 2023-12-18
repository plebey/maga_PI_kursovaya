from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, DECIMAL, Table, ForeignKey, Time
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Client(Base):
    __tablename__ = 'Клиенты'
    id = Column('Код', Integer, primary_key=True)
    login = Column('Логин', String)
    pswd = Column('Пароль', String)
    name = Column('Имя', String)
    ph_num = Column('НомерТелефона', String)
    card_num = Column('СерияНомерКарты', String)
    orders = relationship('Order', back_populates='client')


StreetsDistricts = Table('УлицыРайоны', Base.metadata,
    Column('КодУлицы', Integer(), ForeignKey('Улицы.КодУлицы')),
    Column('КодРайона', Integer(), ForeignKey('Районы.КодРайона'))
                         )


class Street(Base):
    __tablename__ = 'Улицы'
    id = Column('КодУлицы', Integer, primary_key=True)
    name = Column('Наименование', String)
    districts = relationship('District', secondary=StreetsDistricts, back_populates='streets')
    # orders1 = relationship('Order', back_populates='boarding_st')
    # orders2 = relationship('Order', back_populates='drop_st')


class District(Base):
    __tablename__ = 'Районы'
    id = Column('КодРайона', Integer, primary_key=True)
    name = Column('Наименование', String)
    streets = relationship('Street', secondary=StreetsDistricts, back_populates='districts')
    # orders1 = relationship('Order', back_populates='boarding_dist')
    # orders2 = relationship('Order', back_populates='drop_dist')


class Order(Base):
    __tablename__ = 'Заявки'
    id = Column('Код', Integer, primary_key=True, autoincrement=False)
    name = Column('КодКлиента', Integer, ForeignKey('Клиенты.Код'))
    client = relationship('Client', back_populates='orders')
    order_time = Column('ВремяЗаявки', DateTime)
    boarding_st_id = Column('УлицаПосадки', Integer, ForeignKey('Улицы.КодУлицы'))
    boarding_st = relationship('Street', foreign_keys=[boarding_st_id], backref='boarding_orders_st')
    boarding_dist_id = Column('РайонПосадки', Integer, ForeignKey('Районы.КодРайона'))
    boarding_dist = relationship('District', foreign_keys=[boarding_dist_id], backref='boarding_orders_dist')
    boarding_house = Column('ДомПосадки', String)
    drop_st_id = Column('УлицаОкПосадки', Integer, ForeignKey('Улицы.КодУлицы'))
    drop_st = relationship('Street', foreign_keys=[drop_st_id], backref='drop_orders_st')
    drop_dist_id = Column('РайонОкПосадки', Integer, ForeignKey('Районы.КодРайона'))
    drop_dist = relationship('District',  foreign_keys=[drop_dist_id], backref='drop_orders_dist')
    drop_house = Column('ДомОкПосадки', String)
    status = Column('Статус', String)


class Car(Base):
    __tablename__ = 'Машины'
    id = Column('ГосНомер', String, primary_key=True)
    name = Column('Марка', String)
    color = Column('Цвет', String)
    year = Column('ГодВыпуска', Integer)


class Driver(Base):
    __tablename__ = 'Водители'
    id = Column('Код', Integer, primary_key=True)
    surname = Column('Фамилия', String)
    name = Column('Имя', String)
    p_name = Column('Отчество', String)
    birth_date = Column('ДатаРождения', Date)
    work_exp = Column('СтажРаботы', Integer)
    car_id = Column('ГосНомер', String, ForeignKey('Машины.ГосНомер'))
    car = relationship('Car', backref='driver')
    ph_num = Column('НомерТелефона', String)
    district_now = Column('РайонПоложения', ForeignKey('Районы.КодРайона'))
    district = relationship('District', backref='driver')
    status = Column('Статус', String)


class OrderService(Base):
    __tablename__ = 'ОбслуживаниеЗаявок'
    id = Column('Код', Integer, ForeignKey('Заявки.Код'), primary_key=True)
    order = relationship('Order', backref='order_service', uselist=False)
    driver_id = Column('Водитель', Integer, ForeignKey('Водители.Код'))
    driver = relationship('Driver', backref='order_service')
    start_datetime = Column('ДатаВремяНач', DateTime)
    end_datetime = Column('ДатаВремяОк', DateTime)



class TaximetrTariff(Base):
    __tablename__ = 'ТарифыТаксометра'
    id = Column('Код', Integer, primary_key=True)
    name = Column('НаименованиеПараметра', String)
    units = Column('ЕдИзм', String)
    price = Column('Цена', DECIMAL(precision=10, scale=2))


class Taximetr(Base):
    __tablename__ = 'Таксометр'
    order_id = Column('КодЗаявки', Integer, ForeignKey('Заявки.Код'), primary_key=True)
    order = relationship('Order', backref='taximetr')
    param_id = Column('КодПараметра', Integer, ForeignKey('ТарифыТаксометра.Код'), primary_key=True)
    param = relationship('TaximetrTariff', backref='taximetr')
    value = Column('Значение', DECIMAL(precision=10, scale=2))




