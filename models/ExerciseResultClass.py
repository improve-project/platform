__author__ = 'tommipor'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime

Base = declarative_base()
class ExerciseResultClass(Base):
        __tablename__ = 'ExerciseResult'
        exerciseResultID = Column(String(255), primary_key=True)
        exerciseID = Column(String(255))
        dataIDs = Column(Text)
        allowedOrganizations = Column(Text)
        started= Column(Integer)
        ended= Column(Integer)
        settings = Column(Text)
        values = Column(Text)
        progress = Column(Text)

        def __init__(self, exerciseResultID, exerciseID, dataIDs, allowedOrganizations, started, ended, settings, values, progress):
            self.exerciseResultID = exerciseResultID
            self.exerciseID = exerciseID
            self.dataIDs = dataIDs
            self.allowedOrganizations = allowedOrganizations
            self.started= started
            self.ended= ended
            self.settings = settings
            self.values = values
            self.progress = progress

        def __repr__(self):
                return "<ExerciseResult(%s, %s, %s, %s, %s, %s, %s,%s,%s)>" % (self.exerciseResultID, self.exerciseID, self.dataIDs, self.allowedOrganizations, self.started, self.ended, self.settings, self.values, self.progress)

        @property
        def columns(self):
            return [ c.name for c in self.__table__.columns ]

        @property
        def columnitems(self):
            return dict([ (c, getattr(self, c)) for c in self.columns ])

        def tojson(self):
            return self.columnitems