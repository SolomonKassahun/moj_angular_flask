from operator import mod
from flask_marshmallow import Marshmallow
from models import *

marsh = Marshmallow()

class UserSchema(marsh.Schema):
    class Meta:
        fields=("UserId","username","password","firstName","lastName","role")
        model = LoginInfo
class ReportSchema(marsh.Schema):
    class Meta:
        fields=("reportId","UserId","mesik","direcrotName","medibName","bureaueNo","dateS","fullName","sex","disability","itemType","systemType","reportedProblem","username")
        model = ReportInfo
class SolutionSchema(marsh.Schema):
    class Meta:
        fields=("solutionId","reportId","UserId","brand","model", "happenedProblem","sole","startDate","endDate","isProblemFixed","reasonProblemNotFixed","itTechName")
        model = SolutionInfo
class CommentSchema(marsh.Schema):
    class Meta:
        fields=("commentId","firstName","lastName", "subject","message")
        model = CommentInfo
class UserRatingSchema(marsh.Schema):
    class Meta:
        fields=("ratingId","solutionId","rating")
        model = UserRatingInfo

