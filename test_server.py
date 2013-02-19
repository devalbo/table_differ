import web
from web.contrib.template import render_jinja
import test_forms
import compare_data
import verify_lists as vl
from datetime import datetime

render = render_jinja(
        'templates',   # Set template directory.
        encoding = 'utf-8',                         # Encoding.
    )
urls = (
    '/verify_lists', 'verify_lists',
    '/compare', 'compare',
    '/compare_with_tolerance', 'compare_with_tolerance',
    '/favicon.ico', 'favicon',
    '/(.*)', 'index'
)
app = web.application(urls, globals())

def get_log_file_name():
        log_file_name = "%s_%s_%s_%s_%s_%s.log" % datetime.timetuple(datetime.now())[0:6]
        return log_file_name
    

class compare:
    def GET(self):
        return render.data_comparison()

    def POST(self):
        prod_data = web.input()["prod_data"]
        int_data = web.input()["int_data"]
        results = compare_data.compare_tabular_inputs(prod_data, int_data)
        return render.data_comparison_results(content=results)


class compare_with_tolerance:
    def GET(self):
        return render.data_comparison_results_with_tolerance()

    def POST(self):
        prod_data = web.input()["prod_data"]
        int_data = web.input()["int_data"]
        results = compare_data.compare_tabular_inputs_with_tolerance(prod_data, int_data)
        return render.data_comparison_results(content=results)


class verify_lists:
    def GET(self):
        return render.verify_lists()

    def POST(self):
        expected_list = web.input()["expected_list"]
        actual_list = web.input()["actual_list"]
        compare_type = web.input()["compare_type"]

        log_file_name = get_log_file_name()
        vl.init_logging(log_file_name)
        results = vl.verify_lists(expected_list, actual_list,
                                  compare_type, True)
        vl.stop_logging
        f = open(log_file_name)
        contents = f.read()
        f.close()

        #return contents
        return render.verify_lists_results(content=contents)


class index:
    def GET(self, path):
        return render.index(
            title="Testing Tools and Services",
            contents="Hello, world!",
            )

f = open('static/favicon.ico', 'rb')
favicon_ico = f.read()
f.close()

class favicon:
    def GET(self):
        web.header("Content-Type", "image/x-icon") 
        return favicon_ico


if __name__ == "__main__":
    app.run()
