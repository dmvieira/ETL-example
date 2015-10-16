#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

links = [
    dict(
        uri="http://www.dfg.de/en/research_funding/programmes/prizes/haendel_prize/in_brief/index.html",
        name=u"Ursula M. Händel Prize",
        kind="premio",
        site="www.dfg.de"),

    dict(
        uri="http://www.dfg.de/en/research_funding/programmes/prizes/rendel_prize/in_brief/index.html",
        name=u"Bernd Rendel Prize",
        kind="premio",
        site="www.dfg.de"),

    dict(
        uri="http://www.dfg.de/en/research_funding/programmes/prizes/von_kaven_award/in_brief/index.html",
        name=u"von Kaven Award",
        kind="premio",
        site="www.dfg.de"),

    dict(
        uri="http://www.dfg.de/en/research_funding/programmes/prizes/von_kaven_award/in_brief/index.html",
        name=u"von Kaven Award",
        kind="premio",
        site="www.dfg.de"),

    dict(
        uri="http://www.dfg.de/en/research_funding/programmes/prizes/maier_leibnitz_prize/in_brief/index.html",
        name=u"The Heinz Maier-Leibnitz Prize",
        kind="premio",
        site="www.dfg.de"),
]

with open("items.json", "w") as f:
    f.write(json.dumps(links))
