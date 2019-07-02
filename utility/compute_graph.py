#!/usr/bin/python

import os
import json
import re
import tempfile
import urllib

HIRAGANA, KATAKANA, KANJI = range(3)


def get_character_type(character):
    if character >= u"\u3040" and character <= u"\u309F":
        return HIRAGANA
    if character >= u"\u30A0" and character <= u"\u30FF":
        return KATAKANA
    # assume everything else is kanji
    return KANJI

def compute_graph(entries):
    graph = {"nodes":[], "edges":[]}
    kanjis = {} # list of entries that contain a specific kanji
    for entry in entries:
        if entry["kanji"] is None:
            continue
        entry["id"] = "vocab_n%d_#%d" % (entry["level"], entry["index"])
        #entry["links"] = []
        for char in entry["kanji"]:
            char_type = get_character_type(char)
            if char_type == KANJI:
                if char not in kanjis:
                    kanjis[char] = []
                kanjis[char].append(entry["id"])
                #entry["links"].append(char)
    for entry in entries:
        if entry["kanji"] is None:
            continue
        graph["nodes"].append(entry)
    for kanji, nodes in kanjis.iteritems():
        # need to link all the nodes together
        for index, node in enumerate(nodes):
            for other in range(index+1, len(nodes)):
                edge = (node, nodes[other])
                if edge not in graph["edges"]:
                    graph["edges"].append(edge)
    return graph
    
def main():
    all_entries = []
    for level in range(1, 6):
        f = open("../data/vocabulary_n%d.json" % level, "r")
        entries = json.loads(f.read())
        f.close()
        graph_level = compute_graph(entries)
        f = open("../data/vocabulary_graph_n%d.json" % level, "w")
        f.write(json.dumps(graph_level))
        f.close()
        all_entries.extend(entries)
    graph = compute_graph(all_entries)
    f = open("../data/vocabulary_graph.json", "w")
    f.write(json.dumps(graph))
    f.close()
    
main()
