import base64
import os

SECRET_KEY = 'CAUFZ7T9WVEQGXSM99KJMMBGB7C5R975P633C6706BR7D7IE3G8AUVK5WBOMG0WL'

def gen_rand_code(uid):
	return str(uid) + ";" +  base64.urlsafe_b64encode(os.urandom(30))