__author__ = 'tommipor'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime

Base = declarative_base()

class PatientClass(Base):
        __tablename__ = 'Patient'
        patientID = Column(String(255), primary_key=True)
        allowedOrganizations = Column(Text())
        rehabilitationSets = Column(Text())
        extID = Column(Integer)

        def __init__(self, patientID, allowedOrganizations, rehabilitationSets):
            self.patientID = patientID
            self.allowedOrganizations = allowedOrganizations
            self.rehabilitationSets = rehabilitationSets
            #self.extID = extID



        def __repr__(self):
                return "<Patient(%s, %s, %s, %s, %s)>" % (self.patientID, self.allowedOrganizations, self.rehabilitationSets, self.extID)

        @property
        def columns(self):
            return [ c.name for c in self.__table__.columns ]

        @property
        def columnitems(self):
            return dict([ (c, getattr(self, c)) for c in self.columns ])

        def tojson(self):
            return self.columnitems