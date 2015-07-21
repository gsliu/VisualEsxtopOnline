from flask import Flask, render_template
# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
	return "Index Page Here!"

@app.route('/esxtop')
def esxtop():
	return render_template('start.html')

if __name__ == '__main__':
	app.run()