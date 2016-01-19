__author__ = 'tommipor'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, DECIMAL

Base = declarative_base()
class ExerciseClass(Base):
        __tablename__ = 'Exercise'
        exerciseID = Column(String(255), primary_key=True)
        allowedOrganizations = Column(Text)
        name = Column(Text)
        description = Column(Text)
        settings = Column(Text)

        def __init__(self, exerciseID, allowedOrganizations,  name, description, settings):
            self.exerciseID = exerciseID
            self.allowedOrganizations  = allowedOrganizations
            self.name = name
            self.description = description
            self.settings = settings


        def __repr__(self):
                return "<Exercise(%s, %s, %s, %s, %s)>" % ( self.exerciseID, self.allowedOrganizations,  self.name, self.description, self.settings )

        @property
        def columns(self):
            return [ c.name for c in self.__table__.columns ]

        @property
        def columnitems(self):
            return dict([ (c, getattr(self, c)) for c in self.columns ])

        def tojson(self):
            return self.columnitems