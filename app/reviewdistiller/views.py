from flask import render_template
from reviewdistiller import app
from flask import request
# import nice_app.Main_Code as Main_Code
import reviewdistiller.generate_summaries as generate_summaries

@app.route('/')
def homepage():
	return render_template("homepage.html", title='Ayelet Berger')

@app.route('/reviewdistiller')
def index():
	return render_template("index.html", title = 'Home')

@app.route('/output')
def review_distiller_output():
	doctor_url = request.args.get('doctor_url')
	(top_reviews, review_distribution, review_stats) = generate_summaries.generate_summary(doctor_url)
	return render_template("output.html", topic0 = top_reviews[0], topic1 = top_reviews[1], topic2 = top_reviews[2],
		percent_0 = review_distribution[0], percent_1 = review_distribution[1], percent_2 = review_distribution[2],
		num_reviews = review_stats[0], num_patients = review_stats[1], num_repeat_patients = review_stats[2])