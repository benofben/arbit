#!/usr/bin/env bash

mongoexport --db arbit --collection form4 --out form4.json
mongoexport --db arbit --collection fundamentals --out fundamentals.json
mongoexport --db arbit --collection ratingsChanges --out ratingsChanges.json
mongoexport --db arbit --collection symbols --out symbols.json
mongoexport --db arbit --collection yahooQuotes --out yahooQuotes.json

cat symbols.json | ramda -c 'omit ["_id", "Industry","Sector"]' > symbols.json.new