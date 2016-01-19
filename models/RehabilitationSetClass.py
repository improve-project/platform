__author__ = 'tommipor'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime

Base = declarative_base()
class RehabilitationSetClass(Base):
        __tablename__ = 'RehabilitationSet'
        rehabilitationSetID = Column(String(255), primary_key=True)
        allowedOrganizations = Column(Text)
        exerciseResultIDs = Column(Text)
        patientConditionIDs = Column(Text)
        patientInformationID = Column(String(255))

        def __init__(self, rehabilitationSetID, allowedOrganizations,  exerciseResultIDs, patientConditionIDs, patientInformationID):
            self.rehabilitationSetID = rehabilitationSetID
            self.exerciseResultIDs = exerciseResultIDs
            self.patientConditionIDs = patientConditionIDs
            self.patientInformationID= patientInformationID
            self.allowedOrganizations = allowedOrganizations;

        def __repr__(self):
                return "<RehabilitationSet(%s, %s, %s, %s, %s)>" % (self.rehabilitationSetID, self.allowedOrganizations, self.exerciseResultIDs, self.patientConditionIDs, self.patientInformationID)

        @property
        def columns(self):
            return [ c.name for c in self.__table__.columns ]

        @property
        def columnitems(self):
            return dict([ (c, getattr(self, c)) for c in self.columns ])

        def tojson(self):
            return self.columnitems