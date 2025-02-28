from extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__='users'
    id=db.Column(db.String(),primary_key=True,default=str(uuid4()))
    username=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(),nullable=False)
    password=db.Column(db.Text())

    def __repr__(self):
        return f"<user {self.username}>"
    
    def set_password(self,password):
        self.password=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    @classmethod
    def get_user_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class TokenBlocklist(db.Model):
    __tablename__='token_blocklist'
    id=db.Column(db.String(),primary_key=True,default=str(uuid4()))
    jti=db.Column(db.String(),nullable=False)
    created_at=db.Column(db.DateTime(),default=lambda: datetime.now())
    


    def __repr__(self):
        return f"<token : {self.jti}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
