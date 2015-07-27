from flask import Flask, render_template, request, url_for, redirect
from werkzeug import secure_filename
import os
import csv
import json
import time
import helper
# configuration
DEBUG = True

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(
    ['csv'])

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

# Time Format : 2013-10-10 23:40:22


def timestr2stamp(timeStr):
    timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


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


def parseHeader(header):
    result = dict()
    result['cpu'] = dict()
    result['memory'] = dict()
    result['cpu']['cpu_count'] = 0
    result['cpu']['pt_indext'] = []
    result['cpu']['ut_indext'] = []
    for item in header:
        # print item
        if helper.is_cpu_process_time(item):
            result['cpu']['pt_indext'].append(header.index(item))
        elif helper.is_cpu_util_time(item):
            result['cpu']['ut_indext'].append(header.index(item))
        elif helper.is_memory_kernel_mbytes(item):
            result['memory']['kernel_mbytes'] = header.index(item)
        elif helper.is_memory_nonkernel_mbytes(item):
            result['memory']['nonkernel_mbytes'] = header.index(item)
        elif helper.is_memory_kernel_state(item):
            result['memory']['kernel_state'] = header.index(item)
        elif helper.is_memory_pshare_shared_mbytes(item):
            result['memory']['pshare_shared_mbytes'] = header.index(item)
        elif helper.is_memory_swap_target_mbytes(item):
            result['memory']['swap_target_mbytes'] = header.index(item)
        elif helper.is_memory_swap_mbytes_read_sec(item):
            result['memory']['swap_mbytes_read'] = header.index(item)
        elif helper.is_memory_swap_mbytes_write_sec(item):
            result['memory']['swap_mbytes_write'] = header.index(item)
    result['cpu']['cpu_count'] = len(result['cpu']['pt_indext'])
    return result


def init_cpu_result(result, index):
    timeStr = '2013-10-10 22:42:26'
    stamp = timestr2stamp(timeStr)
    result['cpu'] = dict()
    result['cpu']['process_time'] = []
    result['cpu']['util_time'] = []
    cpu_count = index['cpu']['cpu_count']
    for i in xrange(0, cpu_count):
        item = dict()
        item['data'] = []
        item['pointStart'] = stamp
        item['pointInterval'] = 5000
        item['dataLength'] = 0
        result['cpu']['process_time'].append(item)
        item1 = dict()
        item1['data'] = []
        item1['pointStart'] = stamp
        item1['pointInterval'] = 5000
        item1['dataLength'] = 0
        result['cpu']['util_time'].append(item1)


def init_memory_result(result, index, catergory):
    timeStr = '2013-10-10 22:42:26'
    stamp = timestr2stamp(timeStr)
    result['memory'][catergory] = dict()
    result['memory'][catergory]['pointInterval'] = 5000
    result['memory'][catergory]['pointStart'] = stamp
    result['memory'][catergory]['dataLength'] = 0
    result['memory'][catergory]['data'] = []


memory_catergory = (
    'kernel_mbytes',
    'nonkernel_mbytes',
    'kernel_state',
    'pshare_shared_mbytes',
    'swap_target_mbytes',
    'swap_mbytes_read',
    'swap_mbytes_write'
)


def init_memory(result, index):
    result['memory'] = dict()
    for catergory in memory_catergory:
        init_memory_result(result, index, catergory)


def create_cpu_process_time(row, index, result):
    cpu_count = index['cpu']['cpu_count']
    pt_indext = index['cpu']['pt_indext']
    for i in xrange(0, cpu_count):
        result['cpu']['process_time'][i][
            'data'].append(float(row[pt_indext[i]]))
        result['cpu']['process_time'][i]['dataLength'] = result[
            'cpu']['process_time'][i]['dataLength'] + 1


def create_cpu_util_time(row, index, result):
    cpu_count = index['cpu']['cpu_count']
    ut_indext = index['cpu']['ut_indext']
    for i in xrange(0, cpu_count):
        result['cpu']['util_time'][i]['data'].append(float(row[ut_indext[i]]))
        result['cpu']['util_time'][i]['dataLength'] = result[
            'cpu']['util_time'][i]['dataLength'] + 1


def create_memory_status(row, index, result, catergory):
    memory_index = index['memory'][catergory]
    result['memory'][catergory]['data'].append(float(row[memory_index]))


def create_memory(row, index, result):
    for catergory in memory_catergory:
        create_memory_status(row, index, result, catergory)


def load_cpu_file(data, catergory, index):
    index_file_name = catergory
    index_file_content = dict()
    index_file_content[catergory] = []
    cpu_count = index['cpu']['cpu_count']
    for i in xrange(0, cpu_count):
        file_name = "static/data/" + catergory + str(i) + ".json"
        index_file_content[catergory].append(catergory + str(i))
        with open(file_name, 'w') as f:
            json.dump(data[i], f)
    with open("static/data/" + index_file_name + ".json", 'w') as f:
        json.dump(index_file_content, f)

def load_memory_file(result):
    for catergory in memory_catergory:
        result['memory'][catergory]['dataLength'] = len(result['memory'][catergory]['data'])
        filename = "static/data/memory_" + catergory + ".json"
        with open(filename, 'w') as f:
            json.dump(result['memory'][catergory], f)

def csv2jsonHC(filename):
    result = dict()
    with open(filename, 'rU') as f:
        f_csv = csv.reader(f)
        headers = f_csv.next()
        index = parseHeader(headers)
        init_cpu_result(result, index)
        init_memory(result, index)
        for row in f_csv:
            create_cpu_process_time(row, index, result)
            create_cpu_util_time(row, index, result)
            create_memory(row, index, result)
    load_cpu_file(result['cpu']['process_time'], 'cpu_process_time', index)
    load_cpu_file(result['cpu']['util_time'], 'cpu_util_time', index)
    load_memory_file(result)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            tid = create_task_dir()
            saved_file = 'upload/' + tid + '/' + filename
            file.save(saved_file)
            csv2jsonHC(saved_file)
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
