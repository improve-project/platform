__author__ = 'tommipor'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime

Base = declarative_base()
class AnalysisClass(Base):
        __tablename__ = 'Analyses'
        analysistaskID = Column(String(255), primary_key=True)
        allowedOrganizations = Column(Text)
        userName = Column(Text)
        taskName = Column(Text)
        analysisModule = Column(Text)
        analysisResult = Column(Text)
        status = Column(Text)
        notification = Column(Text)
        configurationParameters = Column(Text)
        started = Column(Integer)
        ended = Column(Integer)


        def __init__(self, analysistaskID, allowedOrganizations, userName, taskName, analysisModule, analysisResult, status, notification, configurationParameters, started, ended  ):
            self.analysistaskID = analysistaskID
            self.allowedOrganizations = allowedOrganizations
            self.userName = userName
            self.taskName = taskName
            self.analysisModule = analysisModule
            self.analysisResult = analysisResult
            self.status = status
            self.notification = notification
            self.configurationParameters = configurationParameters
            self.started = started
            self.ended = ended

        def __repr__(self):
                return "<Analyses(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)>" % (self.analysistaskID, self.allowedOrganizations, self.userName, self.taskName, self.analysisModule, self.analysisResult, self.status, self.notification, self.configurationParameters, self.started, self.ended )

        @property
        def columns(self):
            return [ c.name for c in self.__table__.columns ]

        @property
        def columnitems(self):
            return dict([ (c, getattr(self, c)) for c in self.columns ])

        def tojson(self):
            return self.columnitems