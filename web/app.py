from flask import Flask, render_template

app = Flask(__name__)

DIAGRAM_PATH = "static/diagrams/"
RESSOURCE_PATH = "static/resources/"


@app.route('/', methods=['POST', 'GET'])
def builder():
    """One page app."""
    import os
    import datetime
    import subprocess
    from flask import request

    template = 'app.html'
    values = {
        "providers": providers(),
    }
    # get now to append to the image file to force the browser to refresh the file
    # when we edit the code as the file have the same name.
    now = datetime.datetime.now()

    diagrams_data = request.form.get('diagrams_data')
    if diagrams_data:
        # dir may not exist
        if not os.path.exists(DIAGRAM_PATH):
            os.makedirs(DIAGRAM_PATH)
        # clean the directory
        _, _, filenames = next(os.walk(DIAGRAM_PATH))
        for one_file in filenames:
            os.remove('%s%s' % (DIAGRAM_PATH, one_file))
        # write the diagrams_data in a file and execute
        with open("%stemp_code.py" % DIAGRAM_PATH, "w") as f:
            f.write(diagrams_data)
        result = subprocess.run(["python3", "temp_code.py"], cwd=DIAGRAM_PATH, capture_output=True)
        # delete the temp file
        os.remove("%stemp_code.py" % DIAGRAM_PATH)
        # if there's error display them on the template
        if result.stderr:
            error_msg = result.stderr.decode("utf-8")
            # clean up the error message
            error_msg = error_msg.replace('File "temp_code.py", ', '')
            values.update({
                "diagrams_data": diagrams_data,
                "error": error_msg
            })
        else:
            # get the pic to display
            # FIXME don't work with Custom
            _, _, filenames = next(os.walk(DIAGRAM_PATH))
            pic_name = filenames[0]
            values.update({
                "diagrams_data": diagrams_data,
                "pic_name": '%s?%s' % (pic_name, now),
            })

    return render_template(template, **values)


def providers():
    """Return the list of providers."""
    import os
    provider_list = os.listdir(RESSOURCE_PATH)
    provider_list.sort()
    # get the icons
    icons = {}
    for one_provider in provider_list:
      provider_path = '%s/%s' % (RESSOURCE_PATH, one_provider)
      for one_element in os.listdir(provider_path):
        if '.png' in one_element:
          icons.update({one_provider: '%s/%s' % (provider_path, one_element)})
    return [{'name': name, 'icon': icons.get(name)} for name in provider_list]

def nodes(provider):
    """Return formatted list of nodes for a gibven provider."""
    import os

    provider_path = '%s/%s' % (RESSOURCE_PATH, provider)
    # build a section for quick navigation
    section = {}
    for one_section in os.listdir(provider_path):
      section_path = '%s/%s' % (provider_path, one_section)
      for one_node in os.listdir(section_path):
        nodes = {one_node}
      section.update({'path': section_path, 'title': '%s.%s' % (provider, one_section), 'nodes': nodes})

    print(section)
    return section


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
