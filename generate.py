import json
from web import helpers, config


with open("web/cache_menu.json", "w+") as cache_file:
    # we call from outside the web so need to prepend the dir and force generate the content
    ressource_path = '%s%s' % ('web/', config.RESSOURCE_PATH)
    file_content = helpers.providers(ressource_path=ressource_path, generate=True)
    cache_file.write(json.dumps(file_content))
