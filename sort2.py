# -*- coding: utf-8 -*-

import os
import yaml

yaml_schema = {
    "meta": {},
    "categories": [
        {
            "category": "${category name}",
            "description": "${category_description}",
            "pkgs": [
                {
                    "pkg": "${package_name_on_pypi}",
                    "description": "${package_description}",
                }
            ]
        }
    ]
}

HERE = os.path.dirname(os.path.abspath(__file__))
arsenal_file = os.path.join(HERE, "arsenal.yml")
arsenal_sorted_file = os.path.join(HERE, "arsenal-sorted.yml")
with open(arsenal_file, "r") as f:
    data = yaml.safe_load(f.read())

for category in data["categories"]:
    # for pkg in category["pkgs"]:
    #     pkg["link"] = "https://pypi.org/search/?q={}".format(pkg["pkg"])
    category["pkgs"] = list(sorted(
        category["pkgs"], key=lambda x: x["pkg"]
    ))

data["categories"] = list(sorted(
    data["categories"], key=lambda x: x["category"]
))

with open(arsenal_sorted_file, "w") as f:
    f.write(yaml.safe_dump(data))
