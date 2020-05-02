

from app import app
from app import db
from app import ma
from flask import render_template,redirect, url_for,request, session,flash,jsonify
from flask_mail import Mail, Message
import os




mail = Mail(app)

#Model/Class = users
class users(db.Model):
    _id = db.Column("id",db.Integer, primary_key=True)
    email = db.Column(db.String(120)) 

    name = db.Column(db.String(80))
    score = db.Column(db.Integer())
    
    def __init__(self,name, email,score):
        self.name = name
        self.email = email
        self.score = score

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email', 'score')

##################################################################

# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

##################################################################

# Get all products 
@app.route('/product', methods=['GET']) 
def get_products():
    all_products = users.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)  

##################################################################

#create table
@app.before_first_request
def create_tables():
    db.create_all()

################################################################

# Email_Send
@app.route("/email")   
def email_send():
	return render_template('email_send.html') 

################################################################

# Wash hand page
@app.route("/handwash")
def wash():
    return render_template("washing hands properly.html")

###################################################################

# Send-Mail
@app.route("/send-mail", methods=["POST", "GET"])
def send_mail():
    if request.method == "POST":
        admin = request.form["admin"]
        
        
        if admin == '': # secret code for my project to access this webpage

            try:
                data = users.query.all()
                totalemail = []
                for user in data:
                    totalemail.append(user.email)


                msg = Message("NOTIFICATION FOR HAND WASH !",
                  sender="", # Enter email_id from which you want to send mail to others.
                  recipients=totalemail)
                msg.body = "" 
                msg.html = render_template('email_send.html')          
                mail.send(msg)
                return render_template("mail.html")

            except Exception as e:
                return str(e)
        else:
            flash("Invalid Administrator username")
            return render_template("AdminEmail.html")       

    else:
        return render_template("AdminEmail.html")

####################################################################

# Home
@app.route("/")
def home():
    return render_template("index2.html")

#####################################################################



##################################################################

# Delete
@app.route("/delete", methods=["POST", "GET"])
def delete():
    if request.method == "POST":
        deleter = request.form["del"]
        found_user = users.query.filter_by(name=deleter).first()

        if found_user:
        	db.session.delete(found_user)
        	db.session.commit()
        	flash("Deleted Successfully!")
        	return render_template("deletebase.html", hello=deleter)
        
        else:
        	flash("Invalid Username")
        	return render_template("deletebase.html", hello=deleter)
        
        
         
    else:
        return render_template("deletebase.html")    

####################################################################

# UserScore
@app.route("/userscore", methods=["POST", "GET"])
def userscore():
    if request.method == "POST":
        scori = request.form["username"]
        session["special"] = scori

        userfound = users.query.filter_by(name = scori).first()

        if userfound:
            
            newscored = userfound.score
            newscored = newscored + 1
            userfound.score = newscored
            db.session.commit()
            return render_template("datascore.html", person = scori, var =newscored)

        else:
            flash("Invalid Username")
            variab = session["special"]
            return render_template("user_score.html", var =variab)
                

    else:
        flash("Welcome")
        
        return render_template("user_score.html") 

#################################################################
                    
@app.route("/verifyemail")
def verify_mail():
    user = session["user"]
    email = session["email"]
    usr = users(user, email,0)
    db.session.add(usr)
    db.session.commit()
    return render_template("verified.html")

#######################################################################3
# Login    
@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        
        email = request.form["emai"]
        session["verifyemail"] = email
        session["user"] = user
        session["email"] = email
        verifyemail = session["verifyemail"]
        
        
        
        found_user = users.query.filter_by(name=user).first()

        if user == '' or email == '':
            flash("Incomplete Details !")
            return render_template("loginsession.html")

            

                                                                                            

        if found_user:
            flash("Already Ragistered!!")
            
            return render_template("loginsession.html")
            

        else:
            email_1 = email.split("@")
            email_2 = email_1[0]

            check = ["{}@gmail.com".format(email_2), "{}@Yahoo.com".format(email_2), "{}@aol.com".format(email_2), "{}@Outlook.com".format(email_2), "{}@iCloud.com".format(email_2), "{}@rediffmail.com".format(email_2)]
            for item in check:
                if email == item:
                    try:
                        msg = Message("NOTIFICATION FOR HAND WASH !",
                          sender="", # Enter email_id from which you want to send mail to others.
                          recipients=[verifyemail])
                        msg.body = ""
                        msg.html = render_template('email_for_verify.html')          
                        mail.send(msg)
                        

                    except Exception as e:
                        return str(e)
                        
                    
                    #usr = users(user, email,0)
                    #db.session.add(usr)
                    #db.session.commit()
                    return render_template("email_reg.html")

                else:
                    flash("Enter Valid Email !!")
                    return render_template("loginsession.html")
            
    else:
        flash("Enter name and a valid Email Id:-")
        return render_template("loginsession.html") 

##################################################################
  

# Logout
@app.route("/logout")
def logout():

    
    flash("You have been logged out!", "info")
    session.pop("user", None)
    session.pop("email", None)
    session.pop("score", None)
    return redirect(url_for("login"))
       
###################################################################
