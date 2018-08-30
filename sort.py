#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
sort * list insider header2 or less.
"""

from __future__ import print_function
import json
import string
import requests
import sqlitedict
from pathlib_mate import Path

header_char_mapper = {
    1: "=", 2: "-", 3: "~", 4: "+", 5: "*", 6: "#", 7: "^",
}

summary_cache = sqlitedict.SqliteDict(
    Path(__file__).change(new_basename="summary_cache.sqlite").abspath,
    autocommit=True,
)
"""
Summary cache file.
"""

root = Path(__file__).change(new_basename="arsenal")
n_parts = len(root.parts)
readme_file = Path(__file__).change(new_basename="README.rst").abspath


def read_striped_lines(path):
    """
    Read a text file, strip white space for each line.
    Return line list.
    """

    with open(path, "rb") as f:
        lines = [
            line.strip() for line in
            f.read().decode("utf-8").strip().split("\n")
        ]
    return lines


def _get_summary(package_name):
    """
    Get a single line package summary.

    For example, go to https://pypi.python.org/pypi/requests/json, and find
    ``data["info"]["summary"]``.
    """
    url = "https://pypi.org/pypi/{package_name}/json".format(
        package_name=package_name
    )
    try:
        html = requests.get(url).text
        data = json.loads(html)
        summary = data["info"]["summary"]
        return summary
    except:
        raise Exception("%s is invalid!" % url)


def get_summary(package_name):
    """
    Using cache to avoid hitting PyPI too many times.
    """
    if package_name in summary_cache:
        return summary_cache[package_name]
    else:
        summary = _get_summary(package_name)
        summary_cache[package_name] = summary
        return summary


package_line_charset = set(string.ascii_letters + string.digits + "-_")
"""
Python package name allowed character set. [A-Z,0-9,-_]
"""


def is_package_line(line):
    """
    Test if it is a package line.

    Example: ``* requests``, ``* flask``.
    """
    if not line.startswith("* "):
        return False
    line = line[2:]
    if len(set(line).difference(package_line_charset)):
        return False
    return True


def sorted_content(lines):
    """
    sort package in single ``index.rst`` file by name.

    For example, lines in ``./arsenal/Cache/index.rst``.
    """
    if not lines[1].startswith("=" * 10):
        raise Exception("Hey it's not a valid rst file!")

    ind_and_line = list()
    for ind, line in enumerate(lines):
        if line.startswith("* "):
            ind_and_line.append((ind, line))

    for nth, (ind, line) in enumerate(
            sorted(
                ind_and_line, key=lambda x: x[1].lower()
            )
    ):
        if is_package_line(line):
            package_name = line[2:]
            summary = get_summary(package_name)
            url = "https://pypi.python.org/pypi/{package_name}".format(
                package_name=package_name
            )
            line = "* `{package_name} <{url}>`_ - {summary}".format(
                package_name=package_name,
                url=url,
                summary=summary,
            )
        lines[ind_and_line[nth][0]] = line

    return lines


def test_sorted_content():
    path = Path(__file__).parent.append_parts("arsenal", "Logging",
                                              "index.rst").abspath
    lines = read_striped_lines(path)
    lines = sorted_content(lines)
    print("\n".join(lines))


# test_sorted_content()


def main():
    """
    1. Go through the ./arsenal directory.
    2. Read metadata from pypi.org.
    3. Append summary to package name, create download link.
    4. Generate the ``README.rst`` file

    Create the ``README.rst`` file.
    """

    def filters(p):
        if p.basename == "index.rst":
            return True
        else:
            return False

    blocks = list()
    blocks.append(".. contents::\n\n")
    blocks.append(".. sectnum::\n")
    blocks.append("    :depth: 7\n")
    blocks.append("    :start: 1\n\n")

    for path in Path(root).select_file(filters):
        print("processing: %s ..." % path)
        header_value = len(path.parts) - n_parts

        lines = read_striped_lines(path.abspath)
        lines = sorted_content(lines)

        lines[1] = header_char_mapper[header_value] * 79
        content = "\n".join(lines) + "\n\n\n"
        blocks.append(content)

    with open(readme_file, "wb") as f:
        content = "".join(blocks)
        f.write(content.encode("utf-8"))


if __name__ == "__main__":
    main()
    summary_cache.close()
