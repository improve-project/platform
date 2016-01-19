__author__ = 'tommipor'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime

Base = declarative_base()
class PatientConditionClass(Base):
        __tablename__ = 'PatientCondition'
        patientConditionID = Column(String(255), primary_key=True)
        allowedOrganizations = Column(Text)
        label = Column(Text)
        description = Column(Text)
        officialMedicalCode = Column(Text)

        def __init__(self, patientConditionID, allowedOrganizations, label, description, officialMedicalCode):
            self.patientConditionID = patientConditionID
            self.allowedOrganizations = allowedOrganizations
            self.label = label
            self.description = description
            self.officialMedicalCode = officialMedicalCode


        def __repr__(self):
                return "<PatientCondition(%s, %s, %s, %s, %s)>" % (self.patientConditionID, self.allowedOrganizations, self.label, self.description, self.officialMedicalCode)

        @property
        def columns(self):
            return [ c.name for c in self.__table__.columns ]

        @property
        def columnitems(self):
            return dict([ (c, getattr(self, c)) for c in self.columns ])

        def tojson(self):
            return self.columnitems