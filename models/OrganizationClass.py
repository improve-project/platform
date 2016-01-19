__author__ = 'tommipor'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime

Base = declarative_base()
class OrganizationClass(Base): 
        __tablename__ = 'Organization'
        organizationID = Column(String(255), primary_key=True)
        name = Column(Text())
        userIDs = Column(Text())
        userGroupIDs = Column(Text())


        def __init__(self, organizationID, name, userIDs, userGroupIDs):
            self.organizationID = organizationID
            self.name = name
            self.userIDs = userIDs
            self.userGroupIDs = userGroupIDs



        def __repr__(self):
                return "<Organization(%s, %s, %s, %s)>" % (self.organizationID, self.name, self.userIDs, self.userGroupIDs)

        @property
        def columns(self):
            return [ c.name for c in self.__table__.columns ]

        @property
        def columnitems(self):
            return dict([ (c, getattr(self, c)) for c in self.columns ])

        def tojson(self):
            return self.columnitems