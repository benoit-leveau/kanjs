#!/usr/bin/python

import os
import json
import re
import tempfile
import urllib

def parse_url(url, level):
    tmp_file = tempfile.mktemp(suffix=".html")
    urllib.urlretrieve(url, filename=tmp_file)
    f = open(tmp_file, "r")
    data = f.read()
    anchor = "<div class=\"mw-parser-output\"><ol>"
    start = data.find(anchor)
    start = start+len(anchor)
    end = data[start:].find("</ol>")
    block = data[start:end]
    lines = block.split("\n")
    entries = []
    for line in lines:
        m = re.match("<li><span class=\"Jpan\" lang=\"ja\"><a href=\".*?\" title=\".*?\">(.*?)</a></span>(?: / <span class=\"Jpan\" lang=\"ja\"><a href=\".*?\" title=\".*?\">(.*?)</a></span>)?(?:, <span class=\"Jpan\" lang=\"ja\"><a href=\".*\" title=\".*\">(.*)</a></span>)? -(.*)</li>", line)
        if m:
            groups = m.groups()
            entry = {
                "english":groups[3],
                "level":level,
                "index":len(entries)}
            if groups[2] is None:
                entry["kanji"] = None
                entry["kana"] = groups[0] # ,groups[1]
            else:
                entry["kanji"] = groups[0]
                entry["kana"] = groups[2]
            entries.append(entry)
    f.close()
    os.unlink(tmp_file)
    return entries

def main():
    for level in range(1, 6):
        url = "https://en.wiktionary.org/wiki/Appendix:JLPT/N%d" % level
        entries = parse_url(url, level)
        f = open("../data/vocabulary_n%d.json" % level, "w")
        f.write(json.dumps(entries))
        f.close()

main()
