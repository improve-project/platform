__author__ = 'tommipor'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime

Base = declarative_base()
class DeviceClass(Base):
        __tablename__ = 'Device'
        deviceID = Column(String(255), primary_key=True)
        allowedOrganizations = Column(Text)
        name = Column(Text)
        type = Column(Text)
        description = Column(Text)
        axisCount = Column(Integer)
        valueUnit = Column(Text)
        valueUnitAbbreviation = Column(Text)
        defaultValue = Column(Text)
        maximumValue = Column(Text)
        minimumValue = Column(Text)

        def __init__(self, deviceID, allowedOrganizations, name, type, description, axisCount, valueUnit, valueUnitAbbreviation, defaultValue, maximumValue, minimumValue ):
            self.deviceID = deviceID
            self.allowedOrganizations = allowedOrganizations
            self.name = name
            self.type = type
            self.description = description
            self.axisCount = axisCount
            self.valueUnit = valueUnit
            self.valueUnitAbbreviation = valueUnitAbbreviation
            self.defaultValue = defaultValue
            self.maximumValue = maximumValue
            self.minimumValue = minimumValue


        def __repr__(self):
                return "<Device(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)>" % (self.deviceID, self.allowedOrganizations, self.name, self.type, self.description, self.axisCount, self.valueUnit, self.valueUnitAbbreviation, self.defaultValue, self.maximumValue, self.minimumValue)

        @property
        def columns(self):
            return [ c.name for c in self.__table__.columns ]

        @property
        def columnitems(self):
            return dict([ (c, getattr(self, c)) for c in self.columns ])

        def tojson(self):
            return self.columnitems