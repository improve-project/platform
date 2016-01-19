__author__ = 'tommipor'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, DECIMAL

Base = declarative_base()
class UserGroupClass(Base):
        __tablename__ = 'UserGroup'
        userGroupID = Column(String(255), primary_key=True)
        name = Column(Text())
        permissionLevel = Column(DECIMAL)
        organizationID = Column(Text())
        userIDs = Column(Text())

        def __init__(self, userGroupID, name, permissionLevel, organizationID, userIDs):
            self.userGroupID = userGroupID
            self.name = name
            self.permissionLevel = permissionLevel
            self.organizationID = organizationID
            self.userIDs = userIDs


        def __repr__(self):
                return "<UserGroup(%s, %s, %s, %s, %s)>" % ( self.userGroupID, self.name, self.permissionLevel, self.organizationID, self.userIDs )
        @property
        def columns(self):
            return [ c.name for c in self.__table__.columns ]

        @property
        def columnitems(self):
            return dict([ (c, getattr(self, c)) for c in self.columns ])

        def tojson(self):
            return self.columnitems