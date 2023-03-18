from flask import Flask, jsonify, request, render_template
from flask_restful import Api, Resource
from werkzeug.security import check_password_hash
import pytz
from datetime import datetime
from flask_cors import CORS, cross_origin
from flask import request, url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import *

tz = pytz.timezone("Asia/Ho_Chi_Minh")
txt_path = r'D:\DevSenior_Training\crawl_beetoon\Tozi_beetoon\restapi\blacklist.txt'