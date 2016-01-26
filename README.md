# Improve platform
The Improve platform has been designed to collect, store and analyse data from sensor based rehabilitation system, so as to provide insights into how treatments could be improved, with benefits for both patients as well as healthcare organisations. The Improve-platform is a web-service to which users and sensors connect via REST-endpoints.

The Improve platform has been developed within the Generic Platform for Movement Training project, funded by EIT Digital (Health & Wellbeing action line) 2015.

# Getting started

## Prerequisites

### REST API
- [ Python 2.7 ](https://www.python.org/download/releases/2.7/)
- [ Flask microframework ](http://flask.pocoo.org/)

### Data storage
- [ Python 2.7 ](https://www.python.org/download/releases/2.7/)
- [ SQLAlchemy ](http://www.sqlalchemy.org/)
- SQL-database

### Analysis
- [ Python 2.7 ](https://www.python.org/download/releases/2.7/)
- [ SciPy ](http://www.scipy.org)
- [ NumPy ](http://www.numpy.org/)
- [ Matplotlib ](http://matplotlib.org/)
- [ scikit-learn ](http://scikit-learn.org/stable/)

## Deployment
- [ Developer one-liners ](/doc/developer_oneliners.md)

## Documentation
- [ Documentation ](/doc/)
- [ Developer one-liners ](/doc/developer_oneliners.md)
- [ API documentation ](/doc/api/)
- [ Database-handler documentation ](/doc/database_handler/)
- [ Analysis framework documentation ](/doc/analysis/)

# Repository structure
    .
    |--- AnalysisPackage
    |     |--- __init__.py
    |     |--- AnalysisClass.py
    |     |--- analysismodule.py
    |     |--- moduleUtilities.py
    |--- doc
    |     |--- api
    |     |     |--- api.yaml
    |     |--- data_storage
    |     |     |--- db_init.sql
    |     |--- developer_oneliners
    |     |--- README
    |--- models
    |     |--- __init__.py
    |     |--- AnalysisClass.py
    |     |--- DataClass.py
    |     |--- DeviceClass.py
    |     |--- ExerciseClass.py
    |     |--- ExerciseResultClass.py
    |     |--- OAuth.py
    |     |--- OrganizationClass.py
    |     |--- PatientClass.py
    |     |--- PatientConditionClass.py
    |     |--- PatientInformationClass.py
    |     |--- UserClass.py
    |     |--- UserGroupClass.py
    |--- modules
    |     |--- __init__.py
    |     |--- analysismodule_A.py
    |     |--- group_analysis.py
    |     |--- scatter_analysis.py
    |     |--- peakerror_analysis.py
    |--- __init__.py
    |--- api_logger.py
    |--- api_specifications.py
    |--- database_handler.py
    |--- databases.conf

# Contact / Contribution
Please contact <improveproj@gmail.com>

# License
Licensed under the BSD 3-Clause license. More in [ LICENSE.md ](/LICENSE.md). 
