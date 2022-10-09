import config
import json
import os


def providers(resource_path, generate=False):
    """Return the list of providers.


    """
    import json

    if not generate:
        try:
            # return from the cache file if exist
            with open("cache_menu.json", "r") as cache_file:
                return json.load(cache_file)
        except IOError:
            # file don't exist generate the content
            pass

    provider_list = os.listdir(resource_path)
    provider_list.sort()
    # get the icons
    icons = {}
    for one_provider in provider_list:
        provider_path = '%s%s' % (resource_path, one_provider)
        for one_element in os.listdir(provider_path):
            if '.png' in one_element:
                icons.update({one_provider: '%s/%s' % (provider_path, one_element)})
    return [{'name': name, 'icon': icons.get(name), 'nodes': nodes(name, resource_path)} for name in provider_list]


def nodes(provider, resource_path):
    """Return formatted list of nodes for a given provider."""
    provider_path = '%s%s' % (resource_path, provider)
    # build a section for quick navigation
    section = []
    # get the data from the meta file
    with open('%s/meta.json' % provider_path) as meta_file:
        meta_data = json.load(meta_file)
    section_list = []
    for one_section in os.listdir(provider_path):
        if '.' in one_section:
            continue # skip the files
        section_list.append(one_section)
    section_list.sort()
    for one_section in section_list:
        section_path = '%s/%s' % (provider_path, one_section)
        section.append({'path': section_path, 'title': '%s.%s' % (provider, one_section), 'nodes': meta_data[one_section]})

    return section


def generate_cache_menu():
    """"""
    from flask import Flask, render_template

    provider_content = providers(resource_path=config.RESOURCE_PATH, generate=True)
    app = Flask(__name__, template_folder= "templates")
    with app.app_context():
        for one_provider in provider_content:
            with open("templates/help/%s.html" % one_provider['name'], "w+") as provider_template:
                file_content = render_template("help_template.html", one_provider=one_provider)
                provider_template.write(file_content)


if __name__ == "__main__":
    """"""
    print('Generate cache menu.')
    generate_cache_menu()
    print('Cache menu generated.')
