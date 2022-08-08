#from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
#from crypt import methods
from email.mime import message
import imp
from flask import Flask, jsonify, abort, request, json
from flask_cors import CORS,cross_origin
from flask_restful import Api, Resource, reqparse
from sqlalchemy import desc, func
from sqlalchemy.sql import text
from sqlalchemy.orm.exc import NoResultFound
from db.Cmodels import db
from pytz import timezone
import pytz, datetime
import json
import datetime
import time
#import emoji
import requests
import re
import gzip
import uuid
import re
#from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from io import BytesIO
import urllib.request
#from skimage import io
#import cv2
import os




##########################################################

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import Schema, fields, ValidationError, pre_load

#####################################################################



db_name = "test"
db_host = "localhost"
db_port = "5432"
db_user = "bcdev1"
user_password = "bcDev1!@#"







###########################################
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'abcdefghijklmnllpqrst'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['Access-Control-Allow-Origin'] = '*'
app.config['Access-Control-Request-Headers'] = '*'
app.config['Access-Control-Allow-Credentials'] = True
app.config['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT'
parser = reqparse.RequestParser()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'  + db_user + ':' + user_password + '@' + db_host + '/' + db_name 

#app.config.from_pyfile('conf/psql-config-server.py')














#class voucher_code(db):
#    __tablename__ = 'voucher_code'
#    id = db.Column(db.Integer)
#    campaign_id  = db.Column(db.String(50))
#    voucher = db.Column(db.String(50))
#    created_date = db.Column(db.Date)
#    status = db.Column(db.Integer)
#
#    def __init__(self, campaign_id, voucher, created_date, status):
#        self.campaign_id = campaign_id
#        self.voucher = voucher
#        self.usedon = created_date
#        self.status = status
#
#    def save(self):
#        db.session.add(self)
#        db.session.commit()
#
#    def voucher_validaiton_by_code(voucher):
#        try:
#            data = voucher_code.query.filter_by(voucher=voucher,status=0).one()
#            return True
#        except NoResultFound:
#            return False
#
class lays_customer(db.Model):
    __tablename__ = 'lays_customer'
    id = db.Column(db.Integer,primary_key=True)
    customer_name = db.Column(db.String(255))
    customer_number = db.Column(db.Integer)
    created_date = db.Column(db.Date)
    status = db.Column(db.Integer)
   
    def __init__(self, customer_name,customer_number, created_date, status):
        self.customer_name = customer_name
        self.custoemer_number = customer_number
        self.usedon = created_date
        self.status = status

    def save(self):
        db.session.add(self)
        db.session.commit()
#
##class lays_users(db):
##    __tablename__ = 'lays_users'
#    id = db.Column(db.Integer)
#    user_id = db.Column(db.Integer)
#    voucher_code = db.Column(db.String(50))
#    created_date = db.Column(db.Date)
#    status = db.Column(db.Integer)
#   
#    def __init__(self, user_id,voucher_code, created_date,status):
#        self.user_id = user_id
#        self.voucher_code = voucher_code
#        self.usedon = created_date
#        self.status = status
#
#    def save(self):
#        db.session.add(self)
#        db.session.commit()
#
#
#class message_content(db):
#    __tablename__ = 'message_content'
#    id = db.Column(db.Integer)
#    customer_number = db.Column(db.Integer)
#    incoming_message = db.Column(db.String(50))
#    outgoing_message = db.Column(db.String(50))
#    incoming_message_time = db.Column(db.Date)
#    outgoing_message_time = db.Column(db.Date)
#   
#    def __init__(self,customer_number,incoming_message,outgoing_message,incoming_message_time,outgoing_message_time):
#        self.customer_number = customer_number
#        self.incoming_message = incoming_message
#        self.incoming_message_time = incoming_message_time
#        self.outgoing_message = outgoing_message
#        self.outgoing_message_time = outgoing_message_time
#
#    def save(self):
#        db.session.add(self)
#        db.session.commit()
#        
        
        
db.init_app(app)
        
        
db=SQLAlchemy()        
        
now=datetime.datetime.utcnow()
def sendmessage(message_pro,customer_number):
    from_no		= '918971189711' 
    headers         = {"api-key":"A714af0a570cf003da623225d34558f78"}
    claimcashbackarray = {
            "from"          : from_no,
            "to"            : customer_number,
            "type"          : 'text',
            "channel"       : 'whatsapp',
            "body"          : message_pro,
            "callback_url"  : '',
            
	}
    url_send = "https://api.kaleyra.io/v1/HXAP1689843537IN/messages"
    r 			        = requests.post(url=url_send,headers=headers,data=claimcashbackarray)
    #data = lays_customer.query.filter_by(customer_number=customer_number).first()
    #if not data:
    #    ins_sql             = "INSERT INTO  lays_user(user_id,voucher_code,created_date) VALUES ('"+str(customer_number)+"',now())"
    #    print(ins_sql)
    #    sel_res				=  db.engine.execute(ins_sql)
 
@cross_origin()
@app.route('/api/v1/skdemo',methods=['GET','POST'])
def start():
    if request.method == 'GET':
        request_data = request.args['message']
        json_data	 = json.loads(request_data)
        
        for row in json_data:
            customer_number = row['from'].strip()
            message_content	=	row['text']['body']
            customer_name	=	row['profile']['name']
        
        #message_content= message_content.replace("'","")
        
        sel_sql = "select id from voucher_code where voucher = '"+str(message_content)+"'"
        sel_res = db.engine.execute(sel_sql).fetchone()
        if (not sel_res):
            message_pro 	=	"Thank you for message, but voucher is not match to your database sorry "#emoji.emojize(":face with medical mask:")
            sendmessage(message_pro,customer_number)
        else:
            sel_sql = "SELECT status,id FROM voucher_code WHERE voucher = '"+str(message_content)+"'"
            sel_res = db.engine.execute(sel_sql).fetchone()
            if(sel_res):
                status = sel_res['status']
                vid =sel_res['id']
                if (status == 0):
                    ins_sql =	"INSERT into  lays_users (voucher_code,user_id) VALUES('"+str(message_content)+"',"+(customer_number)+")"
                    sel_res =	db.engine.execute(ins_sql)
                    message_pro 	=	"Thank for message now your data will save to your server"
                    sendmessage(message_pro,customer_number)
                    upd_sql = "UPDATE voucher_code SET  voucher = '"+str(message_content)+"',status = 1 WHERE id =  "+str(vid)
                    upd_res = db.engine.execute(upd_sql)
                    message_pro = 'Now you are participated '#+emoji.emojize(":grinning_face_with_big_eyes:")
                    sendmessage(message_pro,customer_number)
                    #data = db.Query.filter_by(customer_number=customer_number).first()
                    #num = lays_customer.customer_number
                    num = lays_customer.query.filter_by(customer_number = customer_number).first()
                    #print(num)
                    #print(customer_number)
                    if not num:
                        ins_cus = "insert into lays_customer (customer_name,customer_number) values ('"+str(customer_name)+"','"+str(customer_number)+"')"
                        db.engine.execute(ins_cus)
                    else:
                      message_pro = "You send message from already used phone number, no problem we allow it"
                      sendmessage (message_pro, customer_number)
                    
                else:
                    message_pro="Sorry sir/madam your voucher alredy used"
                    sendmessage(message_pro,customer_number)
                ins_mess = "insert into message_content (customer_number,incoming_message,outgoing_message) values("+str(customer_number)+",'"+str(message_content)+"','"+str(message_pro)+"')"
                db.engine.execute(ins_mess)
            return str('succes')
    else:
        print("get no call")
        return str(10)
    return str('succes')
    
if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0',port=3000) 
    