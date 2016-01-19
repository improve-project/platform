__author__ = 'tommipor'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime

Base = declarative_base()
class DataClass(Base):
        __tablename__ = 'Data'
        dataID = Column(String(255), primary_key=True)
        deviceID = Column(String(255))
        allowedOrganizations = Column(Text)
        samples = Column(Text)

        def __init__(self, dataID, deviceID, allowedOrganizations, samples):
            self.dataID = dataID
            self.deviceID = deviceID
            self.allowedOrganizations = allowedOrganizations
            self.samples = samples


        def __repr__(self):
                return "<Data(%s, %s, %s, %s)>" % (self.dataID, self.deviceID, self.allowedOrganizations, self.samples)

        @property
        def columns(self):
            return [ c.name for c in self.__table__.columns ]

        @property
        def columnitems(self):
            return dict([ (c, getattr(self, c)) for c in self.columns ])

        def tojson(self):
            return self.columnitems