import re

import unicodedata
from flask import Flask ,render_template, url_for, flash, redirect, request, jsonify
from flask_marshmallow import Marshmallow
from flask_restplus import Resource,Api,fields,Namespace, namespace
from sqlalchemy import Table, Column, Integer, String, Float, MetaData, null
from sqlalchemy import true
from werkzeug.utils import cached_property
from flask_cors import CORS
from datetime import datetime
#from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_jwt_extended import JWTManager, jwt_required, create_access_token




from setting import *
from models import *
from marsh import *

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = "Alaways Store Hashed Value"
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
CORS(app,resources={"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['content-Type'] =  'application/json'


db.init_app(app) # initialize
with app.app_context():
  db.create_all()

marsh = Marshmallow(app)

user_schema = UserSchema()
users_schema = UserSchema(many = true)

report_schema = ReportSchema()
reports_schema = ReportSchema(many = true)


solution_schema = SolutionSchema()
solutions_schema = SolutionSchema(many = true)

comment_schema = CommentSchema()
comments_schema = CommentSchema(many = true)


user_rating_schema = UserRatingSchema()
user_ratings_schema = UserRatingSchema(many = true)



api = Api(app,version="1",title="App Database",description="Vehicle Information")
list_of_names = {}

User = api.model("User",{
    'username':fields.String("username"),
    'password':fields.String("password"),
    'firstName':fields.String("firstName"),
    'lastName':fields.String("lastName"),
    'role':fields.String("role"),
   
})
Report = api.model("Report",{
    'UserId': fields.String("UserId"),
     'mesik':fields.String("mesik"),
    'direcrotName':fields.String("direcrotName"),
    'medibName':fields.String("medibName"),
    'bureaueNo':fields.String("bureaueNo"),
    'dateS':fields.String("dateS"),
    'fullName':fields.String("fullName"),
    'sex':fields.String("sex"),
    'disability':fields.String("disability"),
    'itemType':fields.String("itemType"),
    'systemType':fields.String("systemType"),
    'reportedProblem':fields.String("reportedProblem"),
    'username':fields.String("username"),
    
}

)

Solutions = api.model("Solution",{
    
    'reportId':fields.String('reportId'),
    'UserId':fields.String('UserId'),
     'brand':fields.String("brand"),
    'model':fields.String("model"),
    'happenedProblem':fields.String("happenedProblem"),
     'sole':fields.String("sole"),
     'startDate':fields.String("startDate"),
    'endDate':fields.String("endDate"),
    'isProblemFixed':fields.String("isProblemFixed"),
     'reasonProblemNotFixed':fields.String("reasonProblemNotFixed"),
     'itTechName':fields.String("itTechName"),
   
}
)
Comment = api.model("Comment",{
     'firstName':fields.String("firstName"),
    'lastName':fields.String("lastName"),
    'subject':fields.String("subject"),
    'message':fields.String("message"),

}
)

Rating = api.model("Rating",{
     'solutionId':fields.String("solutionId"),
    'rating':fields.String("rating"),
   

}
)



@api.route("/api/LoginInfo")
class LoginResource(Resource):
    def get(self):
        user = LoginInfo.query.all()
        return users_schema.dump(user)
    
    @api.expect(User)
    @api.response(201,"Successfuly created new logedin!")
    def post(self):
        user = LoginInfo()
        user.username = request.json['username']
        user.password = request.json['password']
        user.firstName = request.json['firstName']
        user.lastName = request.json['lastName']
        user.role = request.json['role']
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201


@api.route("/api/LoginInfo/<int:id>")
class LoginResource(Resource):
    def get(self,id):
        user = LoginInfo.query.filter_by(UserId=id).first()
        return user_schema.dump(user)
    
    @api.expect(User)
    @api.response(204,"Successfuly created new logedin!")
    def put(self,id):
        user = LoginInfo.query.filter_by(UserId=id).first()
        user.username = request.json['username']
        user.password = request.json['password']
        user.firstName = request.json['firstName']
        user.lastName = request.json['lastName']
        user.role = request.json['role']
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
    @api.response(204, 'User Deleted Successfully.')
    def delete(self, id):
        user = LoginInfo.query.filter_by(UserId=id).first()
        if user is None:
            return None, 404
        db.session.delete(user)
        db.session.commit()
        return None, 204


#login authentication
@api.route("/api/LoginInfo/login")
class LoginResource(Resource):
    @api.expect(User)
    @api.response(201,"Successfuly created new logedin!")
    def post(self):
        if request.is_json:
           username = request.json['username']
           password = request.json['password']
           #role = request.json['role']
        else:
            username = request.form['username']
            password = request.form['password']
            #role = request.json['role']
        test=LoginInfo.query.filter_by(username=username, password=password).first()
        if test:
            access_token = create_access_token(identity=username)
            currentUser={"username":test.username , "UserId":test.UserId, "role": test.role, "password":test.password, "firstName":test.firstName, "lastName": test.lastName}
            # access_token = create_access_token(identity=email)
            # , access_token=access_token
            #return jsonify(message= test.role)
            return jsonify(message="login successful",username = currentUser, access_token=access_token)
        else:
            return "Wrong email and/or password ",300
        # user.username = request.json['username']
        # user.password = request.json['password']
        # user.firstName = request.json['firstName']
        # user.lastName = request.json['lastName']
        # user.role = request.json['role']
        # db.session.add(user)
        # db.session.commit()
        # return user_schema.dump(user), 201


@api.route("/api/ReportInfo")
class ReportResource(Resource):
    def get(self):
        report = ReportInfo.query.all()
        return reports_schema.dump(report)
    
    @api.expect(Report)
    @api.response(201,"Successfuly created new Report!")
    def post(self):
        report = ReportInfo()
        report.UserId = request.json['UserId']
        report.mesik = request.json['mesik']
        report.direcrotName = request.json['direcrotName']
        report.medibName = request.json['medibName']
        report.bureaueNo = request.json['bureaueNo']
        report.dateS = request.json['dateS']
        report.fullName = request.json['fullName']
        report.sex = request.json['sex']
        report.disability = request.json['disability']
        report.itemType = request.json['itemType']
        report.systemType = request.json['systemType']
        report.reportedProblem = request.json['reportedProblem']
        report.username = request.json['username']
        db.session.add(report)
        db.session.commit()
       
        return report_schema.dump(report), 201



@api.route("/api/Report/<int:id>",methods=["GET","POST","PUT","DELETE"])
class Solution(Resource):
    def get(self,id):
        report = ReportInfo.query.filter_by(reportId=id).first()
        return report_schema.dump(report)
    
    @api.expect(Report)
    @api.response(204,"Successfuly updated the Report!")
    def put(self,id):
        report = ReportInfo.query.filter_by(reportId=id).first()
        report.UserId = request.json['UserId']
        report.mesik = request.json['mesik']
        report.direcrotName = request.json['direcrotName']
        report.medibName = request.json['medibName']
        report.bureaueNo = request.json['bureaueNo']
        report.dateS = request.json['dateS']
        report.fullName = request.json['fullName']
        report.sex = request.json['sex']
        report.disability = request.json['disability']
        report.itemType = request.json['itemType']
        report.systemType = request.json['systemType']
        report.reportedProblem = request.json['reportedProblem']
        report.username = request.json['username']
       
        db.session.add(report)
        db.session.commit()
        return report_schema.dump(report), 201
    @api.response(204, 'report deleted.')
    def delete(self, id):
        report = ReportInfo.query.filter_by(reportId=id).first()
        if report is None:
            return None, 404
        db.session.delete(report)
        db.session.commit()
        return None, 204



@api.route("/api/users/<int:UserId>/reports/<int:id>",methods=["GET","POST","PUT","DELETE"])
class ReportResource(Resource):
    def get(self,id, UserId):
        report = ReportInfo.query.filter_by(reportId=id, UserId=UserId).first()
        return report_schema.dump(report)
    
    @api.expect(Report)
    @api.response(204,"Successfuly Updated")
    def put(self,id):
        report = ReportInfo.query.filter_by(reportId=id).first()
        report.mesik = request.json['username']
        report.direcrotName = request.json['direcrotName']
        report.medibName = request.json['medibName']
        report.bureaueNo = request.json['bureaueNo']
        report.dateS = request.json['dateS']
        report.fullName = request.json['fullName']
        report.sex = request.json['sex']
        report.disability = request.json['disability']
        report.itemType = request.json['itemType']
        report.systemType = request.json['systemType']
        report.reportedProblem = request.json['reportedProblem']
        report.assignedItTech = request.json['assignedItTech']
        db.session.add(report)
        db.session.commit()
        return report_schema.dump(report), 201
    @api.response(204, 'report deleted.')
    def delete(self,id,UserId):
        report = ReportInfo.query.filter_by(reportId=id, UserId=UserId).first()
        if report is None:
            return None, 404
        db.session.delete(report)
        db.session.commit()
        return None, 204





@api.route("/api/Solution",methods=["GET","POST"])
class Solution(Resource):
    def get(self):
        solution = SolutionInfo.query.all()
        return solutions_schema.dump(solution)
    
    @api.expect(Solutions)
    @api.response(201,"Successfuly created the Solution!")
    def post(self):
        solution = SolutionInfo()
        solution.UserId = request.json['UserId']
        solution.reportId = request.json['reportId']
        solution.brand = request.json['brand']
        solution.model = request.json['model']
        solution.happenedProblem = request.json['happenedProblem']
        solution.sole = request.json['sole']
        solution.startDate = request.json['startDate']
        solution.endDate = request.json['endDate']
        solution.isProblemFixed = request.json['isProblemFixed']
        solution.reasonProblemNotFixed = request.json['reasonProblemNotFixed']
        solution.itTechName = request.json['itTechName']
        
        
        db.session.add(solution)
        db.session.commit()
        return solution_schema.dump(solution), 201


@api.route("/api/Solution/<int:id>",methods=["GET","POST","PUT","DELETE"])
class Solution(Resource):
    def get(self,id):
        solution = SolutionInfo.query.filter_by(solutionId=id).first()
        return solution_schema.dump(solution)
    
    @api.expect(Solution)
    @api.response(204,"Successfuly updated the Solution!")
    def put(self,id):
        solution = SolutionInfo.query.filter_by(solutionId=id).first()
        solution.UserId = request.json['UserId']
        solution.reportId = request.json['reportId']
        solution.brand = request.json['brand']
        solution.model = request.json['model']
        solution.happenedProblem = request.json['happenedProblem']
        solution.startDate = request.json['startDate']
        solution.endDate = request.json['endDate']
        solution.isProblemFixed = request.json['isProblemFixed']
        solution.reasonProblemNotFixed = request.json['reasonProblemNotFixed']
        solution.itTechName = request.json['itTechName']
      
        db.session.add(solution)
        db.session.commit()
        return solution_schema.dump(solution), 201
    @api.response(204, 'Solution deleted.')
    def delete(self, id):
        solution = SolutionInfo.query.filter_by(solutionId=id).first()
        if solution is None:
            return None, 404
        db.session.delete(solution)
        db.session.commit()
        return None, 204

#query solution based on reportId
@api.route("/api/Solution/<int:reportId>",methods=["GET","POST","PUT","DELETE"])
class Solution(Resource):
    def get(self,reportId):
        solution = SolutionInfo.query.filter_by(reportId=reportId).first()
        return solution_schema.dump(solution)
    
    @api.expect(Solution)
    @api.response(204,"Successfuly updated the Solution!")
    def put(self,reportId):
        solution = SolutionInfo.query.filter_by(reportId=reportId).first()
        solution.UserId = request.json['UserId']
        solution.reportId = request.json['reportId']
        solution.brand = request.json['brand']
        solution.model = request.json['model']
        solution.happenedProblem = request.json['happenedProblem']
        solution.startDate = request.json['startDate']
        solution.endDate = request.json['endDate']
        solution.isProblemFixed = request.json['isProblemFixed']
        solution.reasonProblemNotFixed = request.json['reasonProblemNotFixed']
        solution.itTechName = request.json['itTechName']
         
       
        db.session.add(solution)
        db.session.commit()
        return solution_schema.dump(solution), 201
    @api.response(204, 'Solution deleted.')
    def delete(self, id):
        solution = SolutionInfo.query.filter_by(solutionId=id).first()
        if solution is None:
            return None, 404
        db.session.delete(solution)
        db.session.commit()
        return None, 204





@api.route("/api/solution/<int:UserId>/reports/<int:id>",methods=["GET","POST","PUT","DELETE"])
class Solution(Resource):
    def get(self,id, UserId):
        solution = SolutionInfo.query.filter_by(solutionId=id, UserId=UserId).first()
        return solution_schema.dump(solution)
    
    @api.expect(Solution)
    @api.response(204,"Successfuly updated the Solution!")
    def put(self,id, UserId):
        solution = SolutionInfo.query.filter_by(solutionId=id, UserId=UserId).first()
        solution.UserId = request.json['UserId']
        solution.reportId = request.json['reportId']
        solution.brand = request.json['brand']
        solution.model = request.json['model']
        solution.happenedProblem = request.json['happenedProblem']
        solution.startDate = request.json['startDate']
        solution.endDate = request.json['endDate']
        solution.isProblemFixed = request.json['isProblemFixed']
        solution.reasonProblemNotFixed = request.json['reasonProblemNotFixed']
        solution.itTechName = request.json['itTechName']
       
        db.session.add(solution)
        db.session.commit()
        return solution_schema.dump(solution), 201
    @api.response(204, 'Solution deleted.')
    def delete(self,id, UserId):
        solution = SolutionInfo.query.filter_by(solutionId=id, UserId=UserId).first()
        if solution is None:
            return None, 404
        db.session.delete(solution)
        db.session.commit()
        return None, 204

@api.route("/api/solution/<int:UserId>/reports/",methods=["GET","POST","PUT","DELETE"])
class Solution(Resource):
    def get(self, UserId):
        solution = SolutionInfo.query.filter_by(UserId=UserId).all()
        print(solution)
        return solutions_schema.dump(solution)
    
    @api.expect(Solution)
    @api.response(204,"Successfuly updated the Solution!")
    def put(self,id, UserId):
        solution = SolutionInfo.query.filter_by(solutionId=id, UserId=UserId).first()
        solution.UserId = request.json['UserId']
        solution.reportId = request.json['reportId']
        solution.brand = request.json['brand']
        solution.model = request.json['model']
        solution.happenedProblem = request.json['happenedProblem']
        solution.startDate = request.json['startDate']
        solution.endDate = request.json['endDate']
        solution.isProblemFixed = request.json['isProblemFixed']
        solution.reasonProblemNotFixed = request.json['reasonProblemNotFixed']
        solution.itTechName = request.json['itTechName']
       
        db.session.add(solution)
        db.session.commit()
        return solution_schema.dump(solution), 201
    @api.response(204, 'Solution deleted.')
    def delete(self,id, UserId):
        solution = SolutionInfo.query.filter_by(solutionId=id, UserId=UserId).first()
        if solution is None:
            return None, 404
        db.session.delete(solution)
        db.session.commit()
        return None, 204



#query based on report Id
@api.route("/api/solution/<int:reportId>/solution/",methods=["GET","POST","PUT","DELETE"])
class Solution(Resource):
    def get(self, reportId):
        solution = SolutionInfo.query.filter_by(reportId=reportId).all()
        print(solution)
        return solutions_schema.dump(solution)
    
    @api.expect(Solution)
    @api.response(204,"Successfuly updated the Solution!")
    def put(self,id, reportId):
        solution = SolutionInfo.query.filter_by(solutionId=id, reportId=reportId).first()
        solution.UserId = request.json['UserId']
        solution.reportId = request.json['reportId']
        solution.brand = request.json['brand']
        solution.model = request.json['model']
        solution.happenedProblem = request.json['happenedProblem']
        solution.startDate = request.json['startDate']
        solution.endDate = request.json['endDate']
        solution.isProblemFixed = request.json['isProblemFixed']
        solution.reasonProblemNotFixed = request.json['reasonProblemNotFixed']
        solution.itTechName = request.json['itTechName']
       
        db.session.add(solution)
        db.session.commit()
        return solution_schema.dump(solution), 201
    @api.response(204, 'Solution deleted.')
    def delete(self,id, reportId):
        solution = SolutionInfo.query.filter_by(solutionId=id, reportId=reportId).first()
        if solution is None:
            return None, 404
        db.session.delete(solution)
        db.session.commit()
        return None, 204
#comment 
@api.route("/api/Comment",methods=["GET","POST"])
class CommentResource(Resource):
    def get(self):
        comment = CommentInfo.query.all()
        return comments_schema.dump(comment)
    
    @api.expect(Comment)
    @api.response(201,"Successfuly created new Comment!")
    def post(self):
        comment = CommentInfo()
        comment.firstName = request.json['firstName']
        comment.lastName = request.json['lastName']
        comment.subject = request.json['subject']
        comment.message = request.json['message']
        db.session.add(comment)
        db.session.commit()
        return comment_schema.dump(comment), 201


@api.route("/api/Comment/<int:id>",methods=["GET","POST","PUT","DELETE"])
class CommentResource(Resource):
    def get(self,id):
        comment = CommentInfo.query.filter_by(commentId=id).first()
        return comment_schema.dump(comment)
    
    @api.expect(Comment)
    @api.response(204,"Successfuly created Comment!")
    def put(self,id):
        comment = CommentInfo.query.filter_by(commentId=id).first()
        comment.firstName = request.json['firstName']
        comment.lastName = request.json['lastName']
        comment.subject = request.json['subject']
        comment.message = request.json['message']
        
        db.session.add(comment)
        db.session.commit()
        return comment_schema.dump(comment), 201
    @api.response(204, 'Comment.')
    def delete(self, id):
        comment = CommentInfo.query.filter_by(commentId=id).first()
        if comment is None:
            return None, 404
        db.session.delete(comment)
        db.session.commit()
        return None, 204

#user rating
@api.route("/api/UserRating")
class UserRatingResource(Resource):
    def get(self):
        rating = UserRatingInfo.query.all()
        return user_ratings_schema.dump(rating)
    
    @api.expect(Rating)
    @api.response(201,"Successfuly created new rating")
    def post(self):
        rating = UserRatingInfo()
        rating.solutionId = request.json['solutionId']
        rating.rating = request.json['rating']
        
        db.session.add(rating)
        db.session.commit()
        return user_rating_schema.dump(rating), 201


@api.route("/api/UserRating/<int:id>")
class LoginResource(Resource):
    def get(self,id):
        rating = UserRatingInfo.query.filter_by(ratingId=id).first()
        return user_rating_schema.dump(rating)
    
    @api.expect(Rating)
    @api.response(204,"Successfuly created new logedin!")
    def put(self,id):
        rating = UserRatingInfo.query.filter_by(ratingId=id).first()
        rating.solutionId = request.json['solutionId']
        rating.rating = request.json['rating']
        db.session.add(rating)
        db.session.commit()
        return user_rating_schema.dump(rating), 201
    @api.response(204, 'Rating Deleted Successfully.')
    def delete(self, id):
        rating = UserRatingInfo.query.filter_by(ratingId=id).first()
        if rating is None:
            return None, 404
        db.session.delete(rating)
        db.session.commit()
        return None, 204

@api.route("/api/<int:solutionId>/UserRating")
class LoginResource(Resource):
    def get(self,solutionId):
        rating = UserRatingInfo.query.filter_by(solutionId=solutionId).first()
        return user_rating_schema.dump(rating)
    
    @api.expect(Rating)
    @api.response(204,"Successfuly created new logedin!")
    def put(self,id):
        rating = UserRatingInfo.query.filter_by(solutionId=id).first()
        rating.solutionId = request.json['solutionId']
        rating.rating = request.json['rating']
        db.session.add(rating)
        db.session.commit()
        return user_rating_schema.dump(rating), 201
    @api.response(204, 'Rating Deleted Successfully.')
    def delete(self, id):
        rating = UserRatingInfo.query.filter_by(solutionId=id).first()
        if rating is None:
            return None, 404
        db.session.delete(rating)
        db.session.commit()
        return None, 204

#assign question
@api.route("/api/reports/<string:username>/reports/",methods=["GET","POST","PUT","DELETE"])
class ReportResource(Resource):
    def get(self, username):
        report = ReportInfo.query.filter_by(username = username).all()
        return reports_schema.dump(report)
    
    @api.expect(Report)
    @api.response(204,"Successfuly Updated")
    def put(self,username):
        report = ReportInfo.query.filter_by(username=username).first()
        report.mesik = request.json['username']
        report.direcrotName = request.json['direcrotName']
        report.medibName = request.json['medibName']
        report.bureaueNo = request.json['bureaueNo']
        report.dateS = request.json['dateS']
        report.fullName = request.json['fullName']
        report.sex = request.json['sex']
        report.disability = request.json['disability']
        report.itemType = request.json['itemType']
        report.systemType = request.json['systemType']
        report.reportedProblem = request.json['reportedProblem']
        report.assignedItTech = request.json['assignedItTech']
        db.session.add(report)
        db.session.commit()
        return report_schema.dump(report), 201
    @api.response(204, 'report deleted.')
    def delete(self, username):
        report = ReportInfo.query.filter_by(username = username).first()
        if report is None:
            return None, 404
        db.session.delete(report)
        db.session.commit()
        return None, 204



