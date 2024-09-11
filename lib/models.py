from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)
    
    # One-to-many relationship with Audition
    auditions = relationship('Audition', backref=backref('role'))

    def __repr__(self):
        return f'<Role {self.character_name}>'
    
    def actors(self):
        return [audition.actor for audition in self.auditions]
    
    def locations(self):
        return [audition.location for audition in self.auditions]
    
    def lead(self):
        # Get the first hired audition for this role
        hired_auditions = [audition for audition in self.auditions if audition.hired == 1]
        if hired_auditions:
            return hired_auditions[0]
        return 'no actor has been hired for this role'
    
    def understudy(self):
        # Get the second hired audition for this role
        hired_auditions = [audition for audition in self.auditions if audition.hired == 1]
        if len(hired_auditions) > 1:
            return hired_auditions[1]
        return 'no actor has been hired for understudy for this role'

class Audition(Base):
    __tablename__ = 'auditions'
    
    id = Column(Integer, primary_key=True)
    actor = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(Integer, nullable=False)
    hired = Column(Integer, default=0)  # Use 0 for False, 1 for True
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    
    role = relationship('Role', backref=backref('auditions'))

    def __repr__(self):
        return f'Audition(id={self.id}, actor={self.actor}, location={self.location}, phone={self.phone}, hired={self.hired}, role_id={self.role_id})'
    
    def call_back(self):
        self.hired = 1  # Set to 1 to indicate hired

# Database setup
engine = create_engine('sqlite:///example.db')  # Change to your actual database URL
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
