import datetime, time
import json
import os
from pprint import pprint

from flask import Flask, request, make_response, redirect, render_template
import sys
sys.path.insert(0, "l:\\_Важное\\6 Работа\\Python\\PyCharm\\UNF_Project\\")
import UNF_OS
import UNF_JSON
import UNF_STRING

app = Flask(__name__)
app.debug = True



def GetParamsFromFilelist(filelist, folder_path):

    files_params_dict = {}

    for filename in filelist:
        fullpath = os.path.join(folder_path, filename)

        params_dict = UNF_JSON.ReadJsonToDict(fullpath)
        Add_spider_settings = params_dict['__Add_spider_settings__']

        summary_path = os.path.join(Add_spider_settings['result_catalog'] , "_outputs", "spider_summary.json")
        progress_path = os.path.join(Add_spider_settings['result_catalog'], "_outputs", "spider_progress.json")

        finished_upload_products = 0
        if os.path.exists(progress_path):
            summary_dict = {}
            is_summary = False
            row_class = "table-warning"
            finish_time = None
            status = "in progress"
            try:
                progress_dict = UNF_JSON.ReadJsonToDict(progress_path)
            except:
                time.sleep(1)
                progress_dict = UNF_JSON.ReadJsonToDict(progress_path)


            groups_comment = f"Группы {progress_dict['num_of_uploaded_groups']} из {progress_dict['num_of_requested_groups']}. "
            products_comment = f"Товары {progress_dict['num_of_uploaded_products']} из {progress_dict['num_of_requested_products']}. "
            images_comment = f"Новые картинки {progress_dict['num_of_uploaded_images']}"


            file_date_time = UNF_OS.modified_date(progress_path)
            duration_s = int((datetime.datetime.now() - file_date_time).total_seconds())
            comment = f"{groups_comment} {products_comment} {images_comment}"
            max_norm_duration = 60
        elif os.path.exists(summary_path):

            try:
                summary_dict = UNF_JSON.ReadJsonToDict(summary_path)
            except:
                time.sleep(1)
                summary_dict = UNF_JSON.ReadJsonToDict(summary_path)

            is_summary = True
            row_class = "table-success"
            finish_time = summary_dict['finish_time']
            in_progress = False
            status = "finished"
            groups_comment = f"Группы {summary_dict['num_of_uploaded_groups']} из {summary_dict['num_of_requested_groups']}. "
            products_comment = f"Товары {summary_dict['num_of_uploaded_products']} из {summary_dict['num_of_requested_products']}. "
            images_comment = f"Новые картинки {summary_dict['num_of_uploaded_images']}"

            file_date_time = UNF_OS.modified_date(summary_path)
            duration_s = int((datetime.datetime.now() - file_date_time).total_seconds())

            comment = f"{groups_comment} {products_comment} {images_comment}"
            max_norm_duration = 7*24*60*60
            finished_upload_products = summary_dict['num_of_uploaded_products']
        else:
            summary_dict = {}
            is_summary = False
            row_class = "table-warning"
            finish_time = None
            in_progress = False
            status = "no status!!!"
            comment = ""
            duration_s = None
            max_norm_duration = 0


        if duration_s == None:
            duration_comment = None
        elif duration_s < 60:
            duration_comment = f"сейчас"
        elif duration_s<60:
            variants = ["секунда", "секунды", "секунд"]
            duration_comment = UNF_STRING.Number_with_Plural_end(duration_s, variants)
        elif duration_s<60*60:
            duration_min = round(duration_s/60, 0)
            variants = ["минута", "минуты", "минут"]
            duration_comment = UNF_STRING.Number_with_Plural_end(duration_min, variants)
        elif duration_s < 24 * 60 * 60:
            duration_hour = round(duration_s / (60*60))
            variants = ["час", "часа", "часов"]
            duration_comment = UNF_STRING.Number_with_Plural_end(duration_hour, variants)
        else:
            duration_day = round(duration_s / (24*60*60), 0)
            duration_comment = f"{duration_day} дней"
            variants = ["день", "дня", "дней"]
            duration_comment = UNF_STRING.Number_with_Plural_end(duration_day, variants)

        if duration_s == None:
            duration_class = "bg-danger bg-gradient"
        elif max_norm_duration == None:
            duration_class = "bg-danger bg-gradient"
        elif duration_s<=max_norm_duration:
            duration_class = ""
        else:
            duration_class = "bg-danger bg-gradient"

        if status == "in progress":
            comment_class = ""
        elif status == "finished" and finished_upload_products>100:
            comment_class = ""
        else:
            comment_class = "bg-danger bg-gradient"

        run_href = f"/run/{filename}"
        html_button_run = f"<button type='submit' formaction='{run_href}' type='button' class='btn btn-info'>Пуск</button>"

        if status == "in progress" and duration_s<60:
            html_button_run = ""



        start_url_list = Add_spider_settings['start_url_list']
        #print(f"start_url_list={start_url_list}")
        params_for_show = {
            'start_url': Add_spider_settings['start_url_list'][0],
            'result_catalog': Add_spider_settings['result_catalog'],
            'summary_path': summary_path,
            'is_summary': is_summary,
            'summary_dict': summary_dict,
            "row_class": row_class,
            'finish_time': finish_time,
            'status': status,
            'comment': comment,
            'duration_comment': duration_comment,
            'duration_class': duration_class,
            'comment_class': comment_class,
            'html_button_run': html_button_run,


        }
        files_params_dict[filename] = params_for_show

    return files_params_dict





@app.route('/')
def index():
    scrapy_settings_path = 'l:\\_Важное\\6 Работа\\Python\\PyCharm\\Parsing3\\Universal_scrapy_app\\'
    filelist = UNF_OS.GetFileList(scrapy_settings_path, "settings*.json")

    filelist.remove("settings_default.json")

    params_from_files = GetParamsFromFilelist(filelist, scrapy_settings_path)

    dt = datetime.datetime.now()
    datetimenow =dt.strftime('%H:%M:%S - %d.%m.%Y года')

    params_dict = {
            "datetimenow": datetimenow,
            #"hello_string": f"Hello! Your IP={request.remote_addr} \n and user_agent={request.user_agent}",
            "file_list": filelist,
            "params_from_files": params_from_files,
                }
    return render_template('index.html', **params_dict)
    #return "Hello! Your IP is {} and you are using {}: ".format(request.remote_addr,
    #                                                            request.user_agent)

@app.route('/run/<setting_file>/')
def run(setting_file):
    import subprocess
    disk = "d:"
    bat_dir = 'd:\\_PythonProjects\\ParserSite\\'
    cmd = bat_dir + 'run_scrapy_parsing.bat' + ' ' + setting_file + " " + bat_dir
    subprocess.Popen(cmd, shell=True)
    print(f"---запускаю {cmd}")
    # PIPE = subprocess.PIPE
    # p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE,
    #                      stderr=subprocess.STDOUT, close_fds=True, cwd='l:\\Temp2\\')
    #os.startfile("1.bat")
    res = f"run {setting_file}"

    #
    # res_bytes = p.stdout.read()
    # res = res_bytes.strip().decode('cp866')
    # #return f"setting file={setting_file} res={res}"

    # import subprocess
    # result = subprocess.run(['ping', 'yandex.ru'], \
    #                              stdout=subprocess.PIPE, encoding='cp866')
    # res = result.stdout
    return redirect("/")
    return f"{res}"


@app.route('/user/<int:user_id>/')
def user_profile(user_id):

    return "Profile page of user #{}".format(user_id)

@app.route('/books/<genre>/')
def books(genre):
    res = make_response("All Books in {} category".format(genre))
    res.headers['Content-Type'] = 'text/plain'
    res.headers['Server'] = 'Foobar'
    return res

# @app.route('/set-cookie')
# def set_cookie():
#     res = make_response("Cookie setter")
#     res.set_cookie("favorite-color", "skyblue", 60*60*24*15)
#     res.set_cookie("favorite-font", "sans-serif", 60*60*24*15)
#     return res

@app.route('/render_markdown')
def render_markdown():
    return "## Heading", 200, {'Content-Type': 'text/markdown'}

@app.route('/transfer')
def transfer():
    #return "", 302, {'location': 'https://localhost:5000/login'}
    return redirect("https://localhost:5000/login")

if __name__ == '__main__':
    app.run(debug=True)

@app.errorhandler(404)
def http_404_handler(error):
    return "<p>HTTP 404 Error Encountered</p>", 404

@app.errorhandler(500)
def http_500_handler(error):
    return "<p>HTTP 500 Error Encountered</p>", 500


@app.before_first_request
def before_first_request():
    pass
    #print("before_first_request() called")

@app.before_request
def before_request():
    pass#
    #print("before_request() called")

@app.after_request
def after_request(response):
    pass
    # print("after_request() called")
    return response


#set FLASK_DEBUG=1
#app.url_map