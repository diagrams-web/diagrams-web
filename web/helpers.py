import config
import json
import os


def providers(with_nodes=False):
    """Return the list of providers."""
    all_providers = []
    
    resource_path = config.RESOURCE_PATH
    provider_list = os.listdir(resource_path)
    provider_list.sort()
    icons = {}
    for one_provider in provider_list:
        provider_path = '%s%s' % (resource_path, one_provider)
        # get the icons 
        for one_element in os.listdir(provider_path):
            if '.png' in one_element:
                icons.update({one_provider: '%s/%s' % (provider_path, one_element)})
        nodes_list = []
        # get the nodes
        if with_nodes:
            nodes_list = nodes(one_provider, resource_path)
        all_providers.append({'name': one_provider, 'icon': icons.get(one_provider), 'nodes': nodes_list})

    return all_providers


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


def generate_help_template():
    """"""
    from flask import Flask, render_template

    provider_content = providers(with_nodes=True)
    app = Flask(__name__, template_folder=config.TEMPLATE_PATH)
    with app.app_context():
        for one_provider in provider_content:
            with open("%shelp/%s.html" % (config.TEMPLATE_PATH, one_provider['name']), "w+") as provider_template:
                file_content = render_template("help_template.html", one_provider=one_provider)
                provider_template.write(file_content)


if __name__ == "__main__":
    """"""
    print('Generate help templates.')
    generate_help_template()
    print('Help templates generated.')
