# -*- coding: utf-8 -*-

import os
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

p_before = os.path.join(os.path.dirname(__file__), "python-arsenal-editor.yml")
p_after = os.path.join(os.path.dirname(__file__), "python-arsenal.yml")
content = open(p_before, "r").read()

data = load(content, Loader=Loader)

data = list(sorted(
    data,
    key=lambda dct: dct["list_name"],
))
for l in data:
    l["weapons"] = list(sorted(
        l["weapons"],
        key=lambda dct: dct["name"],
    ))

new_content = dump(data, Dumper=Dumper, allow_unicode=True, width=1000, sort_keys=False)
open(p_after, "w").write(new_content)
