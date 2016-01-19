__author__ = 'tommipor'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, DECIMAL, Enum

Base = declarative_base()
class PatientInformationClass(Base):
        __tablename__ = 'PatientInformation'
        patientInformationID = Column(String(255), primary_key=True)
        allowedOrganizations = Column(Text)
        bodyWeight = Column(DECIMAL)
        bodyHeight = Column(DECIMAL)
        upperBodyDominantSide= Column(Enum("Right", "Left"))
        lowerbodyDominantSide= Column(Enum("Right", "Left"))
        birthYear = Column(Integer)
        gender = Column(Enum("Male", "Female", "Indeterminate"))

        def __init__(self, patientInformationID, allowedOrganizations, bodyWeight, bodyHeight, upperBodyDominantSide, lowerbodyDominantSide, birthYear, gender):
            self.patientInformationID = patientInformationID
            self.allowedOrganizations = allowedOrganizations
            self.bodyWeight = bodyWeight
            self.bodyHeight = bodyHeight
            self.upperBodyDominantSide= upperBodyDominantSide
            self.lowerbodyDominantSide= lowerbodyDominantSide
            self.birthYear = birthYear
            self.gender = gender

        def __repr__(self):
                return "<PatientInformation(%s, %s, %s, %s, %s, %s, %s, %s)>" % (self.patientInformationID, self.allowedOrganizations, self.bodyWeight, self.bodyHeight, self.bodyHeight, self.upperBodyDominantSide, self.lowerbodyDominantSide, self.birthYear, self.gender)

        @property
        def columns(self):
            return [ c.name for c in self.__table__.columns ]

        @property
        def columnitems(self):
            return dict([ (c, getattr(self, c)) for c in self.columns ])

        def tojson(self):
            return self.columnitems