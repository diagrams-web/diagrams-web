import os
import datetime
import subprocess

from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    """One page app. Display the editor."""
    import helpers

    template = 'app.html'
    values = {
        "providers": helpers.providers(),
    }

    return render_template(template, **values)


@app.route('/help/<string:provider>', methods=['GET'])
def load_provider_help(provider):
    """"""
    with open("templates/help/%s.html" % provider, "r") as f:
        file_content = f.read()
    return {'content': file_content}

@app.route('/build', methods=['POST'])
def build():
    """Build the diagrams and return the file path to display."""
    import config
    values = {}

    diagrams_data = request.form['diagrams_data']
    print('diagrams_data: ', diagrams_data)
    if diagrams_data:
        # get now to append to the image file to force the browser to refresh the file
        # when we edit the code as the file have the same name.
        now = datetime.datetime.now()
        # dir may not exist
        if not os.path.exists(config.DIAGRAM_PATH):
            os.makedirs(config.DIAGRAM_PATH)
        # clean the directory
        _, _, filenames = next(os.walk(config.DIAGRAM_PATH))
        for one_file in filenames:
            os.remove('%s%s' % (config.DIAGRAM_PATH, one_file))
        # write the diagrams_data in a file and execute
        with open("%stemp_code.py" % config.DIAGRAM_PATH, "w") as f:
            f.write(diagrams_data)
        result = subprocess.run(["python3", "temp_code.py"], cwd=config.DIAGRAM_PATH, capture_output=True)
        # delete the temp file
        os.remove("%stemp_code.py" % config.DIAGRAM_PATH)
        # if there's error display them on the template
        if result.stderr:
            error_msg = result.stderr.decode("utf-8")
            # clean up the error message
            error_msg = error_msg.replace('File "temp_code.py", ', '')
            print(diagrams_data)
            values.update({
                "diagrams_data": diagrams_data,
                "error": error_msg
            })
        else:
            # get the pic to display
            # FIXME don't work with Custom
            _, _, filenames = next(os.walk(config.DIAGRAM_PATH))
            pic_name = filenames[0]
 
            values.update({
                "diagrams_data": diagrams_data,
                "pic_name": '%s?%s' % (pic_name, now),
            })
    
    return values


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
