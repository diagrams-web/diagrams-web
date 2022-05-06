import os


def providers(ressource_path, generate=False):
    """Return the list of providers."""
    import json

    if not generate:
        try:
            # return from the cache file if exist
            with open("cache_menu.json", "r") as cache_file:
                return json.load(cache_file)
        except IOError:
            # file don't exist generate the content
            pass

    provider_list = os.listdir(ressource_path)
    provider_list.sort()
    # get the icons
    icons = {}
    for one_provider in provider_list:
        provider_path = '%s%s' % (ressource_path, one_provider)
        for one_element in os.listdir(provider_path):
            if '.png' in one_element:
                icons.update({one_provider: '%s/%s' % (provider_path.replace('web/', ''), one_element)})
    return [{'name': name, 'icon': icons.get(name), 'nodes': nodes(name, ressource_path)} for name in provider_list]


def nodes(provider, ressource_path):
    """Return formatted list of nodes for a given provider."""
    provider_path = '%s%s' % (ressource_path, provider)
    # build a section for quick navigation
    section = []
    for one_section in os.listdir(provider_path):
        if '.' in one_section:
            continue # skip the provider pics
        section_path = '%s/%s' % (provider_path, one_section)
        nodes = []
        for one_node in os.listdir(section_path):
            class_name = clean_class_name(one_node)
            nodes.append({'img': one_node, 'class_name': class_name})
        section.append({'path': section_path.replace('web/', ''), 'title': '%s.%s' % (provider, one_section), 'nodes': nodes})

    return section


def clean_class_name(one_node):
  """Generate the class name from the ressource file."""
  return one_node.capitalize().replace('.png', '')
