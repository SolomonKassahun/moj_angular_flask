from audioop import add
from datetime import date, datetime
from email import message
from email.policy import default
from sqlalchemy import Table, Column, Integer, String, Float, MetaData
import imp
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
#from app import db

db = SQLAlchemy()


class LoginInfo(db.Model):
      __tablename__ = 'user'
      UserId = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String,nullable=False, default='')
      password = db.Column(db.String,nullable=False,default='')
      firstName = db.Column(db.String,nullable=True,default='')
      lastName = db.Column(db.String,nullable=True,default='')
      role = db.Column(db.String,nullable=False,default='user')
      #reportInfo = db.relationship('ReportInfo', backref='loginInfo', lazy=True,primaryjoin="ReportInfo.UserId == LoginInfo.UserId")
      def __str__(self) -> str:
         return ",".join([str(self.UserId), str(self.username), str(self.password), str(self.firstName), str(self.firstName), str(self.lastName), str(self.role)])


class ReportInfo(db.Model):
      __tablename__ = 'reportInfo'
      reportId = db.Column(db.Integer, primary_key=True)
      UserId = db.Column(db.String,nullable=False)
      mesik = db.Column(db.String,nullable=False)
      direcrotName = db.Column(db.String,nullable=False)
      medibName = db.Column(db.String,nullable=False)
      bureaueNo = db.Column(db.String,nullable=False)
      dateS = db.Column(db.String,nullable=False)
      fullName = db.Column(db.String,nullable=False)
      sex = db.Column(db.String,nullable=False)
      disability = db.Column(db.String,nullable=False)
      itemType = db.Column(db.String,nullable=False)
      systemType = db.Column(db.String,nullable=False)
      reportedProblem = db.Column(db.String,nullable=False)
      username = db.Column(db.String,nullable=False)
class SolutionInfo(db.Model):
      __tablename__ = 'solution'
      solutionId = db.Column(db.Integer, primary_key=True,autoincrement=True)
      UserId = db.Column(db.String,nullable=False)
      reportId = db.Column(db.String,nullable=False)
      brand = db.Column(db.String,nullable=False)
      model = db.Column(db.String,nullable=False)
      happenedProblem = db.Column(db.String,nullable=False)
      sole = db.Column(db.String,nullable=False)
      startDate = db.Column(db.String,nullable=False)
      endDate = db.Column(db.String,nullable=False)
      isProblemFixed = db.Column(db.String,nullable=False)
      reasonProblemNotFixed = db.Column(db.String,nullable=False)
      itTechName = db.Column(db.String,nullable=False)
class CommentInfo(db.Model):
      __tablename__ = 'comment'
      commentId = db.Column(db.Integer, primary_key=True,autoincrement=True)
      firstName = db.Column(db.String,nullable=False)
      lastName = db.Column(db.String,nullable=False)
      subject = db.Column(db.String,nullable=False)
      message = db.Column(db.String,nullable=False)
class UserRatingInfo(db.Model):
      __tablename__ = 'userrating'
      ratingId = db.Column(db.Integer, primary_key=True,autoincrement=True)
      solutionId = db.Column(db.String,nullable=False)
      rating = db.Column(db.String,nullable=False)
      







   





     