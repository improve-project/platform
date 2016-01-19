__author__ = 'tommipor'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from json import dumps
Base = declarative_base()
class UserClass(Base):
        __tablename__ = 'User'
        userID = Column(String(255), primary_key=True)
        organizationID = Column(Text())
        firstName = Column(Text())
        lastName = Column(Text())
        userName = Column(Text())
        password = Column(Text())
        accessToken = Column(Text())
        jobTitle = Column(Text())
        patientIDs = Column(Text())

        def __init__(self, userID, organizationID, firstName, lastName, userName, password, accessToken, jobTitle, patientIDs ):
            self.userID = userID
            self.organizationID = organizationID
            self.firstName = firstName
            self.lastName = lastName
            self.userName = userName
            self.password = password
            self.accessToken = accessToken
            self.jobTitle = jobTitle
            self.patientIDs = patientIDs

        def __repr__(self):
                return "<User(%s, %s, %s, %s, %s, %s, %s, %s, %s)>" % (self.userID, self.organizationID, self.firstName, self.lastName, self.userName, self.password, self.accessToken, self.jobTitle, self.patientIDs)

        @property
        def columns(self):
            return [ c.name for c in self.__table__.columns ]

        @property
        def columnitems(self):
            return dict([ (c, getattr(self, c)) for c in self.columns ])

        def tojson(self):
            return self.columnitems