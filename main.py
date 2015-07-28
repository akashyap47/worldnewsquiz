import math
import os
import random
import shelve
import traceback
import datetime

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask.ext.cors import cross_origin
from flask.ext.sqlalchemy import SQLAlchemy

from aux import SECRET_KEY, gen_rand_code
from consts import DOMAINS, DOMAIN_TO_STORIES, ISO_CODE_TO_COUNTRY_NAME, STRINGS_D, STORIES, SURVEYS, QUESTIONS, CODE_TO_CUISINE

DEBUG = True

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///worldnewsquiz.db"
db = SQLAlchemy(app)

app.config['CORS_HEADERS'] = 'Content-Type'

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ip_addr = db.Column(db.String(45))
	crowdflower = db.Column(db.Boolean)
	consent = db.Column(db.Boolean)
	age = db.Column(db.String(32))
	gender = db.Column(db.String(32))
	education = db.Column(db.String(32))
	country_origin = db.Column(db.String(32))
	country_residence = db.Column(db.String(32))
	native_lang = db.Column(db.String(32))
	confirmation_code = db.Column(db.String(64), nullable=True)
	valid = db.Column(db.Boolean)
	confirmed = db.Column(db.Boolean)
	authentic = db.Column(db.Boolean)

class Quiz(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	lang = db.Column(db.String(32))
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
	q1_sid = db.Column(db.Integer)
	q1_c1 = db.Column(db.String(8))
	q1_c2 = db.Column(db.String(8))
	q1_c3 = db.Column(db.String(8))
	q1_c4 = db.Column(db.String(8))
	q1_ans = db.Column(db.String(8), nullable=True)
	q2_sid = db.Column(db.Integer)
	q2_c1 = db.Column(db.String(8))
	q2_c2 = db.Column(db.String(8))
	q2_c3 = db.Column(db.String(8))
	q2_c4 = db.Column(db.String(8))
	q2_ans = db.Column(db.String(8), nullable=True)
	q3_sid = db.Column(db.Integer)
	q3_c1 = db.Column(db.String(8))
	q3_c2 = db.Column(db.String(8))
	q3_c3 = db.Column(db.String(8))
	q3_c4 = db.Column(db.String(8))
	q3_ans = db.Column(db.String(8), nullable=True)
	q4_sid = db.Column(db.Integer)
	q4_c1 = db.Column(db.String(8))
	q4_c2 = db.Column(db.String(8))
	q4_c3 = db.Column(db.String(8))
	q4_c4 = db.Column(db.String(8))
	q4_ans = db.Column(db.String(8), nullable=True)
	q5_sid = db.Column(db.Integer)
	q5_c1 = db.Column(db.String(8))
	q5_c2 = db.Column(db.String(8))
	q5_c3 = db.Column(db.String(8))
	q5_c4 = db.Column(db.String(8))
	q5_ans = db.Column(db.String(8), nullable=True)
	q6_sid = db.Column(db.Integer)
	q6_c1 = db.Column(db.String(8))
	q6_c2 = db.Column(db.String(8))
	q6_c3 = db.Column(db.String(8))
	q6_c4 = db.Column(db.String(8))
	q6_ans = db.Column(db.String(8), nullable=True)
	q7_sid = db.Column(db.Integer)
	q7_c1 = db.Column(db.String(8))
	q7_c2 = db.Column(db.String(8))
	q7_c3 = db.Column(db.String(8))
	q7_c4 = db.Column(db.String(8))
	q7_ans = db.Column(db.String(8), nullable=True)
	q8_sid = db.Column(db.Integer)
	q8_c1 = db.Column(db.String(8))
	q8_c2 = db.Column(db.String(8))
	q8_c3 = db.Column(db.String(8))
	q8_c4 = db.Column(db.String(8))
	q8_ans = db.Column(db.String(8), nullable=True)
	q9_sid = db.Column(db.Integer)
	q9_c1 = db.Column(db.String(8))
	q9_c2 = db.Column(db.String(8))
	q9_c3 = db.Column(db.String(8))
	q9_c4 = db.Column(db.String(8))
	q9_ans = db.Column(db.String(8), nullable=True)
	q10_sid = db.Column(db.Integer)
	q10_c1 = db.Column(db.String(8))
	q10_c2 = db.Column(db.String(8))
	q10_c3 = db.Column(db.String(8))
	q10_c4 = db.Column(db.String(8))
	q10_ans = db.Column(db.String(8), nullable=True)
	q11_sid = db.Column(db.Integer)
	q11_c1 = db.Column(db.String(8))
	q11_c2 = db.Column(db.String(8))
	q11_c3 = db.Column(db.String(8))
	q11_c4 = db.Column(db.String(8))
	q11_ans = db.Column(db.String(8), nullable=True)
	q12_sid = db.Column(db.Integer)
	q12_c1 = db.Column(db.String(8))
	q12_c2 = db.Column(db.String(8))
	q12_c3 = db.Column(db.String(8))
	q12_c4 = db.Column(db.String(8))
	q12_ans = db.Column(db.String(8), nullable=True)
	q13_sid = db.Column(db.Integer)
	q13_c1 = db.Column(db.String(8))
	q13_c2 = db.Column(db.String(8))
	q13_c3 = db.Column(db.String(8))
	q13_c4 = db.Column(db.String(8))
	q13_ans = db.Column(db.String(8), nullable=True)
	q14_sid = db.Column(db.Integer)
	q14_c1 = db.Column(db.String(8))
	q14_c2 = db.Column(db.String(8))
	q14_c3 = db.Column(db.String(8))
	q14_c4 = db.Column(db.String(8))
	q14_ans = db.Column(db.String(8), nullable=True)
	q15_sid = db.Column(db.Integer)
	q15_c1 = db.Column(db.String(8))
	q15_c2 = db.Column(db.String(8))
	q15_c3 = db.Column(db.String(8))
	q15_c4 = db.Column(db.String(8))
	q15_ans = db.Column(db.String(8), nullable=True)
	q16_sid = db.Column(db.Integer)
	q16_c1 = db.Column(db.String(8))
	q16_c2 = db.Column(db.String(8))
	q16_c3 = db.Column(db.String(8))
	q16_c4 = db.Column(db.String(8))
	q16_ans = db.Column(db.String(8), nullable=True)
	q17_sid = db.Column(db.Integer)
	q17_c1 = db.Column(db.String(8))
	q17_c2 = db.Column(db.String(8))
	q17_c3 = db.Column(db.String(8))
	q17_c4 = db.Column(db.String(8))
	q17_ans = db.Column(db.String(8), nullable=True)
	q18_sid = db.Column(db.Integer)
	q18_c1 = db.Column(db.String(8))
	q18_c2 = db.Column(db.String(8))
	q18_c3 = db.Column(db.String(8))
	q18_c4 = db.Column(db.String(8))
	q18_ans = db.Column(db.String(8), nullable=True)
	q19_sid = db.Column(db.Integer)
	q19_c1 = db.Column(db.String(8))
	q19_c2 = db.Column(db.String(8))
	q19_c3 = db.Column(db.String(8))
	q19_c4 = db.Column(db.String(8))
	q19_ans = db.Column(db.String(8), nullable=True)
	q20_sid = db.Column(db.Integer)
	q20_c1 = db.Column(db.String(8))
	q20_c2 = db.Column(db.String(8))
	q20_c3 = db.Column(db.String(8))
	q20_c4 = db.Column(db.String(8))
	q20_ans = db.Column(db.String(8), nullable=True)
	q21_sid = db.Column(db.Integer)
	q21_c1 = db.Column(db.String(8))
	q21_c2 = db.Column(db.String(8))
	q21_c3 = db.Column(db.String(8))
	q21_c4 = db.Column(db.String(8))
	q21_ans = db.Column(db.String(8), nullable=True)
	q22_sid = db.Column(db.Integer)
	q22_c1 = db.Column(db.String(8))
	q22_c2 = db.Column(db.String(8))
	q22_c3 = db.Column(db.String(8))
	q22_c4 = db.Column(db.String(8))
	q22_ans = db.Column(db.String(8), nullable=True)
	t_started = db.Column(db.DateTime)
	t_submitted = db.Column(db.DateTime, nullable=True)

basedir = os.path.dirname(os.path.abspath(__file__))
if not os.path.isfile(basedir + "/histogram.db"):
	s = shelve.open(basedir + "/histogram.db")
	for i in xrange(10):
		shelf_k = str(i*10) + "s"
		s[shelf_k] = 0
	s.close()
	db.create_all()

SUPPORTED_LANGS = ["en", "chn"]

VALID_AGES = ["na", "1-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85+"]
VALID_GENDERS = ["na", "f", "m", "other"]
VALID_EDUCATIONS = ["na", "hs_incomplete", "hs_complete", "vocational_degree", "two_yr_grad_degree", "four_yr_grad_degree", "postgrad_degree"]
VALID_ORIGINS = ISO_CODE_TO_COUNTRY_NAME.keys() + ["na", "other"]
VALID_RESIDENCES = ISO_CODE_TO_COUNTRY_NAME.keys() + ["na", "other"]
VALID_LANGS = SUPPORTED_LANGS + ["na", "other"]

PC_TO_IMGUR_HASH = {
	"en0": "3z0Bi0R",
	"en4": "GVU0dv4",
	"en9": "QrhjrhD",
	"en13": "O6mDRS8",
	"en18": "rP4wWnq",
	"en22": "Kjbufos",
	"en27": "sSV4Cdm",
	"en31": "UycxQIa",
	"en36": "UeU4mSV",
	"en40": "QbzOpTP",
	"en45": "O41HpsX",
	"en50": "scfVHm7",
	"en54": "TmmC37W",
	"en59": "MjNqu9R",
	"en63": "thSUuL9",
	"en68": "SpbEDEn",
	"en72": "TmnTg1k",
	"en77": "OHwBDSa",
	"en81": "MhythEs",
	"en86": "oqBzrqZ",
	"en90": "XSqHtuS",
	"en95": "iYec9VZ",
	"en100": "9VXJpAO",
	"chn0": "XI7cANq",
	"chn4": "JvYpKg8",
	"chn9": "bnECaiI",
	"chn13": "qiLVXTz",
	"chn18": "P5oT7ww",
	"chn22": "GhegrDa",
	"chn27": "Tpj2czZ",
	"chn31": "Bv6t8w2",
	"chn36": "8nf39y5",
	"chn40": "zA7EmQv",
	"chn45": "5dcKKAE",
	"chn50": "nLQGuQp",
	"chn54": "RDoTLOL",
	"chn59": "oRPGJX1",
	"chn63": "NG4C626",
	"chn68": "FPf99TX",
	"chn72": "XmdrbS4",
	"chn77": "SO537jI",
	"chn81": "9hio7UD",
	"chn86": "FGuoFgW",
	"chn90": "9ZdFVw2",
	"chn95": "9rqbnBF",
	"chn100": "eMprxRJ",
}

def user_bad_effort():
	return session.get("bad_effort")

def user_completed_experiment():
	return session.get("experiment_completed")

def user_completed_quiz():
	return session.get("quiz_completed")

def user_started_experiment():
	return session.get("experiment_started")

def user_started_quiz():
	return session.get("quiz_started")

def user_crowdflower():
	return session.get("crowdflower")

def user_chosen_lang():
	return session.get("lang") in SUPPORTED_LANGS

def user_completed_demographics():
	return session.get("demographics_completed")

def user_bad_demographics():
	return ((session.get("native_lang") != session.get("lang")) or
		    (session.get("lang") == "chn" and session.get("country_residence") != "chn") or
		    (session.get("lang") == "en" and session.get("country_residence") != "usa"))

def user_code_invalidated():
	return (user_crowdflower() and user_completed_quiz() and (not user_completed_experiment()) and
		   (user_bad_demographics() or session.get("consent") == False))

def persist_initial_state(quiz_data):
	u = User()
	u.crowdflower = session["crowdflower"]
	u.ip_addr = session["ip_addr"]
	u.consent = session["consent"]
	u.age = session["age"]
	u.gender = session["gender"]
	u.education = session["education"]
	u.country_origin = session["country_origin"]
	u.country_residence = session["country_residence"]
	u.native_lang = session["native_lang"]
	u.valid = False
	u.confirmed = False
	u.authentic = True
	if session.get("authentic") == False:
		u.authentic = False
	db.session.add(u)
	db.session.commit()
	session["id"] = u.id
	u.confirmation_code = gen_rand_code(session["id"])
	db.session.commit()

	q = Quiz()
	q.user_id = session["id"]
	q.lang = session["lang"]
	for i in xrange(22):
		setattr(q, "q" + str(i+1) + "_sid", quiz_data[i]["story_id"])
		choices = quiz_data[i]["choices"]
		for j in xrange(4):
			setattr(q, "q" + str(i+1) + "_c" + str(j+1), choices[j])
	q.t_started = datetime.datetime.now()
	db.session.add(q)
	db.session.commit()

# Routing
def redirect_appropriately():
	if not user_started_experiment():
		return redirect(url_for("index"))
	elif not user_chosen_lang():
		return redirect(url_for("index"))
	elif session.get("consent") is None:
		return redirect(url_for("get_consent"))
	elif session.get("consent") == False:
		if user_crowdflower() and user_completed_quiz() and not user_completed_experiment():
			return redirect(url_for("code_invalidated"))
		else:
			return redirect(url_for("no_consent"))
	elif not user_completed_demographics():
		return redirect(url_for("get_demographics"))
	elif user_crowdflower() and user_bad_demographics():
		if user_completed_quiz() and not user_completed_experiment():
			return redirect(url_for("code_invalidated"))
		else:
			return redirect(url_for("bad_demographics"))
	elif not user_started_quiz():
		return redirect(url_for("quiz"))
	elif not user_completed_quiz():
		return redirect(url_for("quiz"))
	else:
		return redirect(url_for("get_results"))

def get_next_module():
	if not user_started_experiment():
		return "index"
	elif not user_chosen_lang():
		return "index"
	elif session.get("consent") is None:
		return "get_consent"
	elif session.get("consent") == False:
		if user_crowdflower() and user_completed_quiz() and not user_completed_experiment():
			return "code_invalidated"
		else:
			return "no_consent"
	elif not user_completed_demographics():
		return "get_demographics"
	elif user_crowdflower() and user_bad_demographics():
		if user_completed_quiz() and not user_completed_experiment():
			return "code_invalidated"
		else:
			return "bad_demographics"
	elif not user_started_quiz():
		return "quiz"
	elif not user_completed_quiz():
		return "quiz"
	else:
		return "results"

@app.route("/", methods=["GET"])
def index():
	if user_completed_quiz():
		return redirect(url_for("get_results"))
	elif user_started_quiz():
		return redirect(url_for("quiz"))
	elif user_started_experiment():
		if user_crowdflower():
			return redirect_appropriately()
		else:
			 return render_template("index.html")
	else:
		is_crowdflower = request.args.get("crowdflower")
		lang = request.args.get("lang")
		session["ip_addr"] = request.access_route[0] or request.remote_addr
		print "referrer:", request.referrer
		if is_crowdflower == "true" and lang in SUPPORTED_LANGS:
			session["crowdflower"] = True
			session["lang"] = lang
			session["experiment_started"] = True
			return redirect(url_for("get_consent"))
		else:
			session["crowdflower"] = False
			session["experiment_started"] = True
			storyv = request.args.get("storyv")
			imgur_hash = None
			if storyv in PC_TO_IMGUR_HASH.keys():
				imgur_hash = PC_TO_IMGUR_HASH[storyv]
				pc = None
				story_lang = None
				if storyv[0:2] == "en":
					story_lang = "en"
					pc = storyv[2:]
				else:
					story_lang = "chn"
					pc = storyv[3:]
				return render_template("index.html", is_var=True, pc=pc, story_lang=story_lang, imgur_hash=imgur_hash)
			return render_template("index.html", is_var=False)

@app.route("/set_lang/", methods=["POST"])
def set_lang():
	if not user_started_experiment() or user_started_quiz() or user_crowdflower():
		return jsonify({"next": get_next_module()})
	req_data = request.get_json()
	if "lang" not in req_data or (req_data["lang"] not in SUPPORTED_LANGS):
		return jsonify({"next": get_next_module()})
	if DEBUG: print "User has set lang to:", req_data["lang"]
	session["lang"] = req_data["lang"]
	return jsonify({"next": get_next_module()})

@app.route("/get_consent/", methods=["GET"])
def get_consent():
	if not user_started_experiment():
		return redirect(url_for("index"))
	elif not user_chosen_lang():
		return redirect(url_for("index"))
	elif user_completed_experiment() and user_crowdflower():
		return redirect(url_for("get_results"))
	else:
		return render_template("consent.html", lang=session.get("lang"),
										   	   strings_d=STRINGS_D)

@app.route("/set_consent/", methods=["POST"])
def set_consent():
	if not user_started_experiment() or not user_chosen_lang():
		return jsonify({"next": get_next_module()})
	elif user_completed_experiment() and user_crowdflower():
		return jsonify({"next": get_next_module()})
	req_data = request.get_json()
	if "consent" not in req_data or type(req_data["consent"]) != bool:
		return jsonify({"next": get_next_module()})
	if req_data["consent"] != session.get("consent"):
		try:
			session["consent"] = req_data["consent"]
			if user_started_quiz():
				user = User.query.filter_by(id=session.get("id")).first()
				user.consent = session.get("consent")
				if not session.get("consent") and user_crowdflower():
					user.authentic = False
				db.session.commit()
				if user_completed_quiz() and user_crowdflower() and not session.get("consent"):
						user.valid = False
						db.session.commit()
						return jsonify({"next": "code_invalidated"})
			if session["consent"] == False and user_crowdflower():
				session["authentic"] = False
			if DEBUG: print "Consent changed to:", session["consent"]
		except Exception:
			traceback.print_exc()
			traceback.print_stack()
			return jsonify({"next": "error"})
	return jsonify({"next": get_next_module()})

@app.route("/no_consent/", methods=["GET"])
def no_consent():
	if session.get("consent") == False:
		return render_template("no_consent.html", lang=session.get("lang"),
								  		  		  strings_d=STRINGS_D)
	else:
		return redirect_appropriately()

@app.route("/get_demographics/", methods=["GET"])
def get_demographics():
	if not user_started_experiment():
		return redirect(url_for("index"))
	elif not user_chosen_lang():
		return redirect(url_for("index"))
	elif session.get("consent") is None:
		return redirect(url_for("get_consent"))
	elif session.get("consent") == False:
		return redirect(url_for("no_consent"))
	elif user_completed_experiment() and user_crowdflower():
		return redirect(url_for("get_results"))
	else:
		return render_template("demographics.html", lang=session.get("lang"),
												    strings_d=STRINGS_D)

@app.route("/set_demographics/", methods=["POST"])
def set_demographics():
	if not session.get("consent"):
		return jsonify({"next": get_next_module()})
	elif user_crowdflower() and user_completed_experiment():
		return jsonify({"next": get_next_module()})
	req_data = request.get_json()
	if ("age" not in req_data or "gender" not in req_data
		or "education" not in req_data or "country_origin" not in req_data
		or "country_residence" not in req_data or "native_lang" not in req_data):
		return jsonify({"next": get_next_module()})
	if ((req_data["age"] not in VALID_AGES) or
		(req_data["gender"] not in VALID_GENDERS) or
		(req_data["education"] not in VALID_EDUCATIONS) or
		(req_data["country_origin"] not in VALID_ORIGINS) or
		(req_data["country_residence"] not in VALID_RESIDENCES) or
		(req_data["native_lang"] not in VALID_LANGS)):
		return jsonify({"next": get_next_module()})
	session["age"] = req_data["age"]
	session["gender"] = req_data["gender"]
	session["education"] = req_data["education"]
	session["country_origin"] = req_data["country_origin"]
	session["country_residence"] = req_data["country_residence"]
	session["native_lang"] = req_data["native_lang"]
	session["demographics_completed"] = True
	try:
		if user_started_quiz():
			user = User.query.filter_by(id=session.get("id")).first()
			user.age = session.get("age")
			user.gender = session.get("gender")
			user.education = session.get("education")
			user.country_origin = session.get("country_origin")
			user.country_residence = session.get("country_residence")
			user.native_lang = session.get("native_lang")
			db.session.commit()
		if user_crowdflower():
			if user_bad_demographics():
				session["authentic"] = False
				if user_started_quiz():
					user = User.query.filter_by(id=session.get("id")).first()
					user.authentic = False
					db.session.commit()
					if user_completed_quiz():
						user.valid = False
						db.session.commit()
						return jsonify({"next": "code_invalidated"})
				else:
					return jsonify({"next": "bad_demographics"})
	except Exception:
		traceback.print_exc()
		return jsonify({"next": "error"})
	return jsonify({"next": get_next_module()})

@app.route("/bad_demographics/", methods=["GET"])
def bad_demographics():
	if user_crowdflower() and user_bad_demographics() and not user_completed_quiz():
			return render_template("bad_demographics.html", lang=session.get("lang"),
															strings_d=STRINGS_D)
	else:
		return redirect_appropriately()

@app.route("/code_invalidated/", methods=["GET"])
def code_invalidated():
	if (user_crowdflower() and user_completed_quiz() and not user_completed_experiment() and
	   (user_bad_demographics() or session.get("consent") == False)):
			return render_template("code_invalidated.html", lang=session.get("lang"),
															strings_d=STRINGS_D)
	else:
		return redirect_appropriately()

@app.route("/effort/", methods=["GET"])
def effort():
	if (user_crowdflower() and user_completed_quiz() and not user_completed_experiment() and
		user_bad_effort()):
		return render_template("poor_effort.html", lang=session.get("lang"),
											       strings_d=STRINGS_D)
	else:
		return redirect_appropriately()

@app.route("/quiz/", methods=["GET"])
def quiz():
	if not user_started_experiment():
		return redirect(url_for("index"))
	elif not user_chosen_lang():
		return redirect(url_for("index"))
	elif session.get("consent") is None:
		return redirect(url_for("get_consent"))
	elif session.get("consent") == False:
		if user_crowdflower() and user_completed_quiz() and not user_completed_experiment():
			return redirect(url_for("code_invalidated"))
		else:
			return redirect(url_for("no_consent"))
	elif not user_completed_demographics():
		return redirect(url_for("get_demographics"))
	elif user_crowdflower() and user_bad_demographics():
		if user_completed_quiz() and not user_completed_experiment():
			return redirect(url_for("code_invalidated"))
		else:
			return redirect(url_for("bad_demographics"))
	elif user_completed_quiz():
		return redirect(url_for("get_results"))
	try:
		quiz_data = get_quiz_data(session.get("id"))
		if not quiz_data:
			quiz_data = generate_quiz_data()
			persist_initial_state(quiz_data)
	except Exception:
		traceback.print_exc()
		return render_template("error.html", lang=session.get("lang"),
									         strings_d=STRINGS_D)
	session["quiz_started"] = True
	return render_template("quiz.html", quiz_data=quiz_data,
	 									code_to_name=ISO_CODE_TO_COUNTRY_NAME,
	 									lang=session.get("lang"),
	 									strings_d=STRINGS_D)

@app.route("/submit_quiz/", methods=["POST"])
def submit_quiz():
	if user_completed_quiz() or not user_started_quiz():
		return jsonify({"next": get_next_module()})
	if session.get("consent") == False:
		return jsonify({"next": get_next_module()})
	if user_crowdflower() and user_bad_demographics():
		return jsonify({"next": get_next_module()})
	req_data = request.get_json()
	tt = None
	try:
		result = Quiz.query.filter_by(user_id=session.get("id")).first()
		for i in xrange(22):
			if not req_data.has_key("q" + str(i+1) + "_ans"):
				return jsonify({"next": get_next_module()})
			choices = []
			for j in range(1, 5):
				choices.append(getattr(result, "q" + str(i+1) + "_c" + str(j)))
			if req_data["q" + str(i+1) +"_ans"] not in choices + ["na"]:
				return jsonify({"next": get_next_module()})
			setattr(result, "q" + str(i+1) + "_ans", req_data["q" + str(i+1) + "_ans"])
		result.t_submitted = datetime.datetime.now()
		tt = result.t_submitted - result.t_started
		tt = divmod(tt.days * 86400 + tt.seconds, 60)
		user = User.query.filter_by(id=session.get("id")).first()
		user.valid = True
	except Exception, err:
		print err
		return jsonify({"next": "error"})

	num_correct = 0
	num_incorrect = 0
	available_countries = ISO_CODE_TO_COUNTRY_NAME.keys()
	readup_countries = []
	gold_wrong = False
	for i in xrange(22):
		story_id = getattr(result, "q" + str(i+1) + "_sid")
		ans = req_data["q" + str(i+1) + "_ans"]
		if ans == STORIES[story_id]["country"]:
			num_correct += 1
		else:
			correct_ans = STORIES[story_id]["country"]
			if correct_ans not in readup_countries:
				readup_countries.append(correct_ans)
			if correct_ans in available_countries:
				available_countries.remove(correct_ans)
			if (i+1 == 7 and ans != "usa") or (i+1 == 16 and ans != "chn"):
				gold_wrong = True
	if len(readup_countries) < 3:
		readup_countries += random.sample(available_countries, 3 - len(readup_countries))
	else:
		readup_countries = random.sample(readup_countries, 3)
	session["readup_countries"] = readup_countries

	pct_correct = int(float(num_correct)*100/22)
	session["num_correct"] = num_correct
	session["pct_correct"] = pct_correct
	try:
		basedir = os.path.dirname(os.path.abspath(__file__))
		shelf = shelve.open(basedir + "/histogram.db")
		shelf_k = int(math.floor(pct_correct/10) * 10)
		if shelf_k == 100:
			shelf_k = "90s"
		else:
			shelf_k = str(shelf_k) + "s"
		shelf[shelf_k] += 1
		shelf.close()
		db.session.commit()
	except Exception, err:
		traceback.print_exc()
		return jsonify({"next": "error"})

	if user_crowdflower() and gold_wrong and (tt[0] < 2 or (tt[0] == 2 and tt[1] < 30)):
		session["bad_effort"] = True
		try:
			user.valid = False
			db.session.commit()
		except Exception:
			print traceback.print_exc()
			return jsonify({"next": "error"})
	session["quiz_completed"] = True
	if not user_crowdflower():
		session["experiment_completed"] = True
	return jsonify({"next": get_next_module()})

@app.route("/results/", methods=["GET"])
def get_results():
	if not user_started_experiment():
		return redirect(url_for("index"))
	elif not user_chosen_lang():
		return redirect(url_for("index"))
	elif session.get("consent") is None:
		return redirect(url_for("get_consent"))
	elif session.get("consent") == False:
		if user_crowdflower() and user_completed_quiz() and not user_completed_experiment():
			return redirect(url_for("code_invalidated"))
		else:
			return redirect(url_for("no_consent"))
	elif not user_completed_demographics():
		return redirect(url_for("get_demographics"))
	elif user_crowdflower() and user_bad_demographics():
		if user_completed_quiz() and not user_completed_experiment():
			return redirect(url_for("code_invalidated"))
		else:
			return redirect(url_for("bad_demographics"))
	elif not user_started_quiz():
		return redirect(url_for("quiz"))
	elif not user_completed_quiz():
		return redirect(url_for("quiz"))
	elif user_crowdflower() and user_bad_effort():
		return redirect(url_for("effort"))
	if user_crowdflower():
			try:
				user = User.query.filter_by(id=session.get("id")).first()
				return render_template("confirmation.html", confirmation_code=user.confirmation_code,
															lang=session.get("lang"),
															strings_d=STRINGS_D)
			except Exception:
				traceback.print_exc()
				return render_template("error.html", lang=session.get("lang"),
											         strings_d=STRINGS_D)
	else:
		try:
			result = Quiz.query.filter_by(user_id=session.get("id")).first()
			num_correct = 0
			lang = session.get("lang")
			quiz_data = []
			pos_valence = []
			for i in xrange(22):
				q_data = {}
				story_id = getattr(result, "q" + str(i+1) + "_sid")
				ans = getattr(result, "q" + str(i+1) + "_ans")
				if STORIES[story_id].get("gold_answer") == "Positive":
					pos_valence.append(ans)
				if ans == STORIES[story_id]["country"]:
					num_correct += 1
				q_data["story"] = STORIES[story_id][lang]
				q_data["choices"] = []
				for j in xrange(1, 5):
					(q_data["choices"]).append(getattr(result, "q" + str(i+1) + "_c" + str(j)))
				q_data["correct_ans"] = STORIES[story_id]["country"]
				q_data["user_ans"] = ans
				q_data["link"] = STORIES[story_id]["link"]
				quiz_data.append(q_data)
			liked_country = None
			if len(pos_valence) == 0:
				liked_country = random.choice(ISO_CODE_TO_COUNTRY_NAME.keys())
			else:
				liked_country = random.choice(pos_valence)
			basedir = os.path.dirname(os.path.abspath(__file__))
			histogram = shelve.open(basedir + "/histogram.db")
			histogram_d = {}
			for i in xrange(10):
				h_k = str(i*10) + "s"
				histogram_d[h_k] = histogram[h_k]
			in_china = (session.get("crowdflower") and session.get("lang") == "chn") or session.get("country_residence") == "chn"
			purple_bar_i = session["pct_correct"]/10
			if purple_bar_i == 10:
				purple_bar_i = 9
			return render_template("results2.html", pct_correct=session["pct_correct"],
												   num_correct=str(session["num_correct"]),
												   lang=session.get("lang"),
												   histogram_d = histogram_d,
												   purple_bar_i = purple_bar_i,
												   readup_countries = session["readup_countries"],
												   in_china = in_china,
												   code_to_country = ISO_CODE_TO_COUNTRY_NAME,
												   code_to_cuisine = CODE_TO_CUISINE,
												   strings_d = STRINGS_D,
												   liked_country = liked_country,
												   quiz_data = quiz_data)
		except Exception:
			traceback.print_exc()
			return render_template("error.html", lang=session.get("lang"),
										         strings_d=STRINGS_D)

@app.route('/error/', methods=['GET'])
def error():
	return render_template("error.html", lang=session.get("lang"),
									     strings_d=STRINGS_D)

@app.route('/confirm_quiz_completion/', methods=['POST'])
@cross_origin()
def confirm_quiz_completion():
	data = request.get_json()
	if "confirmation_code" not in data:
		return jsonify({"success": False})
	confirmation_code = data["confirmation_code"]
	confirmation_code_split = confirmation_code.split(";")
	try:
		if len(confirmation_code_split) == 2:
			identifier, code = confirmation_code_split
			query_result = (db.session.query(User).filter(User.id == int(identifier))).first()
			if query_result and query_result.confirmation_code.split(";")[1] == code and query_result.valid and not query_result.confirmed:
				query_result.confirmed = True
				db.session.commit()
				return jsonify({'success': True, 'confirmation_code': confirmation_code})
			else:
				return jsonify({'success': False, "retry": False})
		else:
			return jsonify({'success': False, "retry": False})
	except Exception:
		traceback.print_exc()
		return jsonify({"success": False, "retry": True})

def get_quiz_data(uid):
	result = Quiz.query.filter_by(user_id=uid).first()
	quiz_data = None
	if result:
		lang = session.get("lang")
		quiz_data = []
		for i in xrange(22):
			story_id = getattr(result, "q" + str(i+1) + "_sid")
			choices = []
			for j in xrange(4):
				choices.append(getattr(result, "q" + str(i+1) + "_c" + str(j+1)))
			quiz_data.append({"story_id": story_id, "story": (STORIES[story_id][lang]).decode("utf-8"), "choices": choices})
	return quiz_data

def generate_quiz_data():
	quiz_data = []
	available_stories = {}
	for domain in DOMAIN_TO_STORIES:
		available_stories[domain] = {"Positive": [], "Negative": []}
		for valence in ["Positive", "Negative"]:
			for story_id in DOMAIN_TO_STORIES[domain][valence]:
				available_stories[domain][valence].append(story_id)

	lang = session.get("lang")
	for domain in DOMAINS:
		for i in xrange(2):
			story_id = None
			choices = []
			if random.random() < 0.5:
				story_id = random.choice(available_stories[domain]["Positive"])
				available_stories[domain]["Positive"].remove(story_id)
			else:
				story_id = random.choice(available_stories[domain]["Negative"])
				available_stories[domain]["Negative"].remove(story_id)
			choices.append(STORIES[story_id]["country"])
			available_countries = ISO_CODE_TO_COUNTRY_NAME.keys()
			available_countries.remove(STORIES[story_id]["country"])
			choices += random.sample(available_countries, 3)
			random.shuffle(choices)
			quiz_data.append({"story_id": story_id, "story": (STORIES[story_id][lang]).decode("utf-8"), "choices": choices})
	random.shuffle(quiz_data)
	c400 = ["usa", "cod", "vnm", "pak"]
	random.shuffle(c400)
	c401 = ["chn", "usa", "ind", "deu"]
	random.shuffle(c401)
	quiz_data.insert(6, {"story_id": 400, "story": (STORIES[400][lang]).decode("utf-8"), "choices": c400})
	quiz_data.insert(15, {"story_id": 401, "story": (STORIES[401][lang]).decode("utf-8"), "choices": c401})
	return quiz_data

if __name__ == '__main__':
	app.run(debug=True)