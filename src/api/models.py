from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Patient(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    id_card= db.Column(db.Interger, unique=True, nullable=False)
    name= db.Column(db.String(120), unique=False, nullable=False)
    phone= db.Column(db.String(15), unique=False, nullable=False)
    age= db.Column(db.Interger, unique=False, nullable=False)
    address=db.Column(db.String(50), unique=False, nullable=False)
    echo=db.relationship("Echo", backref="patient", lazy=True)

    def __repr__(self):
        return f'<Patient {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "id_car": self.id_card,
            "name": self.name,
            "phone": self.phone,
            "age": self.age,
            "address": self.address,
        }
    

    class Echo(db.Model):
        id= db.Column(db.Interger, primary_key=True)
        type=db.Column(db.String(50), unique=True, nullable=False)
        date=db.Column(db.Date, unique=True, nullable=False)
        pay=db.Column(db.Interger, unique=True, nullable=False)
        id_patient=db.Column(db.Interger, db.ForeignKey("patient.id"), nullable=False)
       
        def __repr__(self):
            return f'<Type {self.type}>'
        
        def serialize(self):
            return{
                "id": self.id,
                "type": self.type,
                "date": self.date,
                "day": self.pay,
            }