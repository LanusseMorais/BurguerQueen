from app.models.db import db
from datetime import datetime
from validate_docbr import CPF


class Customer(db.Model):
    __tablename__ = 'customers'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    registration_date = db.Column(
        db.String(20), default=datetime.now().strftime('%Y-%m-%d'))

    orders = db.relationship('Order', back_populates='customer')

    def __init__(self, cpf, name, email, registration_date=datetime.now().strftime('%Y-%m-%d')):
        self.cpf = self.clean_cpf(cpf)
        self.name = name
        self.email = email
        self.registration_date = registration_date

    def clean_cpf(self, cpf):
        cpf_validator = CPF()
        cleaned_cpf = ''.join(filter(str.isdigit, cpf))
        if not cpf_validator.validate(cleaned_cpf):
            raise ValueError("CPF inválido")

        return cleaned_cpf
