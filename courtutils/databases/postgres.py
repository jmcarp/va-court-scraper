import os
from datetime import datetime
from sqlalchemy import create_engine, Boolean, Column, Date, Integer, Float, String, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from geoalchemy2 import Geometry
from pprint import pprint

Base = declarative_base()

class Court():
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fips = Column(Integer)
    location = Column(Geometry('POINT'))

class CircuitCourt(Base, Court):
    __tablename__ = 'circuit_courts'

class DistrictCourt(Base, Court):
    __tablename__ = 'district_courts'


class DateTask():
    id = Column(Integer, primary_key=True)
    fips = Column(Integer)
    startdate = Column(Date)
    enddate = Column(Date)
    casetype = Column(String)

class CircuitCourtDateTask(Base, DateTask):
    __tablename__ = 'circuit_court_date_tasks'

class DistrictCourtDateTask(Base, DateTask):
    __tablename__ = 'district_court_date_tasks'


class DateSearch():
    id = Column(Integer, primary_key=True)
    fips = Column(Integer)
    date = Column(Date)
    casetype = Column(String)

class CircuitCourtDateSearch(Base, DateSearch):
    __tablename__ = 'circuit_court_dates_searched'

class DistrictCourtDateSearch(Base, DateSearch):
    __tablename__ = 'district_court_dates_searched'


CIRCUIT_CRIMINAL = 'CircuitCriminal'
CIRCUIT_CIVIL = 'CircuitCivil'
DISTRICT_CRIMINAL = 'DistrictCriminal'
DISTRICT_CIVIL = 'DistrictCivil'

#
# Case Tables
#
class Case():
    id = Column(Integer, primary_key=True)
    fips = Column(Integer)
    details_fetched_for_hearing_date = Column(Date)
    CaseNumber = Column(String)

class CircuitCriminalCase(Base, Case):
    prefix = CIRCUIT_CRIMINAL
    __tablename__ = prefix + 'Case'
    Hearings = relationship(prefix + 'Hearing', back_populates='case')
    Pleadings = relationship(prefix + 'Pleading', back_populates='case')
    Services = relationship(prefix + 'Service', back_populates='case')

    Filed = Column(Date)
    Commencedby = Column(String)
    Locality = Column(String)

    Defendant = Column(String)
    AKA = Column(String)
    Sex = Column(String)
    Race = Column(String)
    DOB = Column(Date)
    Address = Column(String)

    Charge = Column(String)
    CodeSection = Column(String)
    ChargeType = Column(String)
    Class = Column(String)
    OffenseDate = Column(Date)
    ArrestDate = Column(Date)

    DispositionCode = Column(String)
    DispositionDate = Column(Date)
    ConcludedBy = Column(String)
    AmendedCharge = Column(String)
    AmendedCodeSection = Column(String)
    AmendedChargeType = Column(String)

    JailPenitentiary = Column(String)
    ConcurrentConsecutive = Column(String)
    LifeDeath = Column(String)
    SentenceTime = Column(Integer)
    SentenceSuspended = Column(Integer)
    OperatorLicenseSuspensionTime = Column(Integer)
    FineAmount = Column(Float)
    Costs = Column(Float)
    FineCostsPaid = Column(Boolean)
    ProgramType = Column(String)
    ProbationType = Column(String)
    ProbationTime = Column(Integer)
    ProbationStarts = Column(String)
    CourtDMVSurrender = Column(String)
    DriverImprovementClinic = Column(Boolean)
    DrivingRestrictions = Column(Boolean)
    DrivingRestrictionEffectiveDate = Column(String)
    AlcoholSafetyAction = Column(Boolean)
    RestitutionPaid = Column(Boolean)
    RestitutionAmount = Column(String)
    Military = Column(String)
    TrafficFatality = Column(Boolean)

    AppealedDate = Column(Date)

    @staticmethod
    def create(case):
        details = case['details']
        hearings = []
        pleadings = []
        services = []

        if 'Hearings' in details:
            hearings = details['Hearings']
            del details['Hearings']
        if 'Pleadings' in details:
            pleadings = details['Pleadings']
            del details['Pleadings']
        if 'Services' in details:
            services = details['Services']
            del details['Services']

        db_case = CircuitCriminalCase(**details)
        db_case.fips = int(case['fips'])
        db_case.details_fetched_for_hearing_date = case['details_fetched_for_hearing_date']

        db_case.Hearings = [
            CircuitCriminalHearing(**hearing)
            for hearing in hearings
        ]
        db_case.Pleadings = [
            CircuitCriminalPleading(**pleading)
            for pleading in pleadings
        ]
        db_case.Services = [
            CircuitCriminalService(**service)
            for service in services
        ]
        return db_case

class CircuitCivilCase(Base, Case):
    prefix = CIRCUIT_CIVIL
    __tablename__ = prefix + 'Case'
    Hearings = relationship(prefix + 'Hearing', back_populates='case')
    Pleadings = relationship(prefix + 'Pleading', back_populates='case')
    Services = relationship(prefix + 'Service', back_populates='case')
    Plaintiffs = relationship(prefix + 'Plaintiff', back_populates='case')
    Defendants = relationship(prefix + 'Defendant', back_populates='case')

    Filed = Column(Date)
    FilingType = Column(String)
    FilingFeePaid = Column(Boolean)
    NumberofPlaintiffs = Column(Integer)
    NumberofDefendants = Column(Integer)
    CommencedBy = Column(String)
    Bond = Column(String)
    ComplexCase = Column(String)

    DateOrderedToMediation = Column(Date)

    Judgment = Column(String)
    FinalOrderDate = Column(Date)
    AppealedDate = Column(Date)
    ConcludedBy = Column(String)

    @staticmethod
    def create(case):
        details = case['details']
        hearings = []
        pleadings = []
        services = []
        plaintiffs = []
        defendants = []

        if 'Hearings' in details:
            hearings = details['Hearings']
            del details['Hearings']
        if 'Pleadings' in details:
            pleadings = details['Pleadings']
            del details['Pleadings']
        if 'Services' in details:
            services = details['Services']
            del details['Services']
        if 'Plaintiffs' in details:
            plaintiffs = details['Plaintiffs']
            del details['Plaintiffs']
        if 'Defendants' in details:
            defendants = details['Defendants']
            del details['Defendants']

        db_case = CircuitCivilCase(**details)
        db_case.fips = int(case['fips'])
        db_case.details_fetched_for_hearing_date = case['details_fetched_for_hearing_date']

        db_case.Hearings = [
            CircuitCivilHearing(**hearing)
            for hearing in hearings
        ]
        db_case.Pleadings = [
            CircuitCivilPleading(**pleading)
            for pleading in pleadings
        ]
        db_case.Services = [
            CircuitCivilService(**service)
            for service in services
        ]
        db_case.Plaintiffs = [
            CircuitCivilPlaintiff(**plaintiff)
            for plaintiff in plaintiffs
        ]
        db_case.Defendants = [
            CircuitCivilDefendant(**defendant)
            for defendant in defendants
        ]
        return db_case

class DistrictCriminalCase(Base, Case):
    prefix = DISTRICT_CRIMINAL
    __tablename__ = prefix + 'Case'
    Hearings = relationship(prefix + 'Hearing', back_populates='case')
    Services = relationship(prefix + 'Service', back_populates='case')

class DistrictCivilCase(Base, Case):
    prefix = DISTRICT_CIVIL
    __tablename__ = prefix + 'Case'
    Hearings = relationship(prefix + 'Hearing', back_populates='case')
    Services = relationship(prefix + 'Service', back_populates='case')
    Reports = relationship(prefix + 'Report', back_populates='case')
    Plaintiffs = relationship(prefix + 'Plaintiff', back_populates='case')
    Defendants = relationship(prefix + 'Defendant', back_populates='case')

#
# Hearing Tables
#
class Hearing():
    id = Column(Integer, primary_key=True)
    Date = Column(Date)
    Type = Column(String)
    Room = Column(String)
    Result = Column(String)

class CircuitCriminalHearing(Base, Hearing):
    prefix = CIRCUIT_CRIMINAL
    __tablename__ = prefix + 'Hearing'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Hearings')
    Duration = Column(String)
    Jury = Column(Boolean)
    Plea = Column(String)

class CircuitCivilHearing(Base, Hearing):
    prefix = CIRCUIT_CIVIL
    __tablename__ = prefix + 'Hearing'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Hearings')
    Duration = Column(String)
    Jury = Column(String)

class DistrictCriminalHearing(Base, Hearing):
    prefix = DISTRICT_CRIMINAL
    __tablename__ = prefix + 'Hearing'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Hearings')
    Plea = Column(String)
    ContinuanceCode = Column(String)

class DistrictCivilHearing(Base, Hearing):
    prefix = DISTRICT_CIVIL
    __tablename__ = prefix + 'Hearing'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Hearings')

#
# Pleading Tables
#
class Pleading():
    id = Column(Integer, primary_key=True)
    Filed = Column(Date)
    Type = Column(String)
    Party = Column(String)
    Judge = Column(String)
    Book = Column(String)
    Page = Column(String)
    Remarks = Column(String)

class CircuitCriminalPleading(Base, Pleading):
    prefix = CIRCUIT_CRIMINAL
    __tablename__ = prefix + 'Pleading'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Pleadings')

class CircuitCivilPleading(Base, Pleading):
    prefix = CIRCUIT_CIVIL
    __tablename__ = prefix + 'Pleading'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Pleadings')

#
# Service Tables
#
class Service():
    id = Column(Integer, primary_key=True)
    Name = Column(String)
    Type = Column(String)
    HowServed = Column(String)

class CircuitCriminalService(Base, Service):
    prefix = CIRCUIT_CRIMINAL
    __tablename__ = prefix + 'Service'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Services')
    HearDate = Column(Date)
    DateServed = Column(Date)

class CircuitCivilService(Base, Service):
    prefix = CIRCUIT_CIVIL
    __tablename__ = prefix + 'Service'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Services')
    HearDate = Column(Date)
    DateServed = Column(Date)

class DistrictCriminalService(Base, Service):
    prefix = DISTRICT_CRIMINAL
    __tablename__ = prefix + 'Service'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Services')
    DateIssued = Column(Date)
    DateReturned = Column(Date)
    Plaintiff = Column(String)

class DistrictCivilService(Base, Service):
    prefix = DISTRICT_CIVIL
    __tablename__ = prefix + 'Service'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Services')
    DateIssued = Column(Date)
    DateReturned = Column(Date)
    Plaintiff = Column(String)

#
# Report Tables
#
class Report():
    id = Column(Integer, primary_key=True)
    Type = Column(String)
    Agency = Column(String)
    Date_Ordered = Column(Date)
    Date_Due = Column(Date)
    Date_Received = Column(Date)

class DistrictCivilReport(Base, Report):
    prefix = DISTRICT_CIVIL
    __tablename__ = prefix + 'Report'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Reports')

#
# Party Tables
#
class CircuitCivilParty():
    id = Column(Integer, primary_key=True)
    Name = Column(String)
    TradingAs = Column(String)
    Attorney = Column(String)

class CircuitCivilPlaintiff(Base, CircuitCivilParty):
    prefix = CIRCUIT_CIVIL
    __tablename__ = prefix + 'Plaintiff'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Plaintiffs')

class CircuitCivilDefendant(Base, CircuitCivilParty):
    prefix = CIRCUIT_CIVIL
    __tablename__ = prefix + 'Defendant'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Defendants')

class DistrictCivilParty():
    id = Column(Integer, primary_key=True)
    Name = Column(String)
    dba = Column(String)
    Address = Column(String)
    Judgement = Column(String)
    Attorney = Column(String)

class DistrictCivilPlaintiff(Base, DistrictCivilParty):
    prefix = DISTRICT_CIVIL
    __tablename__ = prefix + 'Plaintiff'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Plaintiffs')

class DistrictCivilDefendant(Base, DistrictCivilParty):
    prefix = DISTRICT_CIVIL
    __tablename__ = prefix + 'Defendant'
    case_id = Column(Integer, ForeignKey(prefix + 'Case.id'))
    case = relationship(prefix + 'Case', back_populates='Defendants')


TABLES = [
    # Courts
    CircuitCourt,
    DistrictCourt,

    # Tasks
    CircuitCourtDateTask,
    DistrictCourtDateTask,

    # Searches
    CircuitCourtDateSearch,
    DistrictCourtDateSearch,

    # Cases
    CircuitCriminalCase,
    CircuitCivilCase,
    DistrictCriminalCase,
    DistrictCivilCase,

    # Hearings
    CircuitCriminalHearing,
    CircuitCivilHearing,
    DistrictCriminalHearing,
    DistrictCivilHearing,

    # Pleadings
    CircuitCriminalPleading,
    CircuitCivilPleading,

    # Services
    CircuitCriminalService,
    CircuitCivilService,
    DistrictCriminalService,
    DistrictCivilService,

    # Reports and Parties
    DistrictCivilReport,
    DistrictCivilPlaintiff,
    DistrictCivilDefendant,
    CircuitCivilPlaintiff,
    CircuitCivilDefendant
]

#
# Database class
#
class PostgresDatabase():
    def __init__(self, court_type):
        self.engine = create_engine("postgresql://" + os.environ['POSTGRES_DB'])
        self.session = sessionmaker(bind=self.engine)()

        for table in TABLES:
            table.__table__.create(self.engine, checkfirst=True) #pylint: disable=E1101

        self.court_type = court_type
        if court_type == 'circuit':
            self.court_builder = CircuitCourt
            self.date_task_builder = CircuitCourtDateTask
            self.date_search_builder = CircuitCourtDateSearch
        else:
            self.court_builder = DistrictCourt
            self.date_task_builder = DistrictCourtDateTask
            self.date_search_builder = DistrictCourtDateSearch

    def commit(self):
        self.session.commit()

    def add_court(self, name, fips, location):
        self.session.add( \
            self.court_builder( \
                name=name, \
                fips=int(fips), \
                location='POINT({} {})'.format( \
                    location.longitude, location.latitude)))

    def add_court_location_index(self):
        pass

    def drop_courts(self):
        self.court_builder.__table__.drop(self.engine, checkfirst=True)
        self.court_builder.__table__.create(self.engine, checkfirst=False)

    def get_courts(self):
        return [{
            'name': court.name,
            'fips': str(court.fips).zfill(3)
        } for court in self.session.query(self.court_builder)]

    def add_date_tasks(self, tasks):
        for task in tasks:
            self.session.add( \
                self.date_task_builder( \
                    fips=int(task['fips']),
                    startdate=task['start_date'],
                    enddate=task['end_date'],
                    casetype=task['case_type']))
        self.session.commit()

    def add_date_task(self, task):
        self.session.add( \
            self.date_task_builder( \
                fips=int(task['fips']),
                startdate=task['start_date'],
                enddate=task['end_date'],
                casetype=task['case_type']))
        self.session.commit()

    def get_and_delete_date_task(self):
        while True:
            try:
                task = self.session.query(self.date_task_builder).first()
                if task is None:
                    return None
                self.session.delete(task)
                self.session.commit()
                return {
                    'fips': str(task.fips).zfill(3),
                    'start_date': task.startdate,
                    'end_date': task.enddate,
                    'case_type': task.casetype
                }
            except IntegrityError:
                self.session.rollback()

    def add_date_search(self, search):
        self.session.add(
            self.date_search_builder(
                fips=int(search['fips']),
                date=search['date'],
                casetype=search['case_type']
            )
        )
        self.session.commit()

    def get_date_search(self, search):
        result = self.session.query(self.date_search_builder).filter_by(
            fips=int(search['fips']),
            date=search['date'],
            casetype=search['case_type']
        ).first()
        if result is None:
            return None
        return search

    def get_case_builder(self, case_type):
        if self.court_type == 'circuit':
            if case_type == 'criminal':
                return CircuitCriminalCase
            else:
                return CircuitCivilCase
        else:
            if case_type == 'criminal':
                return DistrictCriminalCase
            else:
                return DistrictCivilCase

    def get_more_recent_case_details(self, case, case_type, date):
        case_builder = self.get_case_builder(case_type)
        result = self.session.query(case_builder).filter(
            case_builder.fips == int(case['fips']),
            case_builder.CaseNumber == case['case_number'],
            case_builder.details_fetched_for_hearing_date >= date
        ).first()
        if result is None:
            return result
        return  {
            'details_fetched_for_hearing_date': result.details_fetched_for_hearing_date
        }

    def replace_case_details(self, case, case_type):
        #pprint(case)
        case_builder = self.get_case_builder(case_type)
        self.session.query(case_builder).filter_by(
            fips=int(case['fips']),
            CaseNumber=case['case_number']
        ).delete()
        self.session.add(case_builder.create(case))
        self.session.commit()

