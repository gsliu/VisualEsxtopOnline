from flask import Flask, render_template, request, url_for, redirect
from werkzeug import secure_filename
import os, csv, json
# configuration
DEBUG = True

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(
    ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'gz', 'tar', 'bz', 'csv'])

app = Flask(__name__)
app.config.from_object(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def create_task_dir():
    tasklist = sorted(os.listdir('upload'), reverse=True)
    if len(tasklist) == 0:
        tid = "1000"
    else:
        tid = str((int(tasklist[0]) + 1))
    os.mkdir('upload/' + tid)
    return tid

def str2dict(row):
	item = dict()
	item['cpu_count'] = 2
	item['time'] = row[0]
	process_time = [row[1], row[2]]
	item['process_time'] = process_time
	cpu_util = [row[4], row[5]]
	item['cpu_util'] = cpu_util
	return item

def csv2json(filename):
	result = []
	with open(filename, 'rU') as f:
		f_csv = csv.reader(f)
		headers = f_csv.next()
		for row in f_csv:
			result.append(str2dict(row))
	print len(result)
	with open("test.json", 'w') as f:
		json.dump(result, f)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            tid = create_task_dir()
            saved_file = 'upload/' + tid + '/' + filename
            file.save(saved_file)
            csv2json(saved_file)
            # reportdirname = create_report_dir(tid)
            # analyze_data(saved_file, 'report/' + tid + '/')
            # add_new_task(tid)
            return redirect(url_for('esxtop'))
    return render_template('index.html')


@app.route('/esxtop')
def esxtop():
    return render_template('start.html')

if __name__ == '__main__':
    app.run(port=5001)
