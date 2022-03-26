#!/bin/env python

import pathlib
import json
import time

def compile_conferencestats(root_dir):
    json_object = {}
    json_object["sponsors"] = {}
    json_object["compiledTime"] = time.time()

    total_sponsors = 0
    total_conferences = 0
    total_events = 0
    
    sponsors = [path for path in pathlib.Path(root_dir).iterdir() 
                if (path.is_dir() and not path.name.startswith('.'))]

    for sponsor in sponsors:
        total_sponsors += 1
        
        sponsor_object = {}
        sponsor_object["conferences"] = {}

        conferences = [path for path in sponsor.iterdir() 
                       if (path.is_dir() and not path.name.startswith('.'))]

        for conference in conferences:
            total_conferences += 1
            
            with open(conference.joinpath('meta.json')) as f:
                conference_object = json.load(f)

            conference_object["years"] = {}

            years = [path for path in conference.iterdir() 
                     if (path.is_dir() and not path.name.startswith('.'))]

            for year in years:
                total_events += 1
                
                with open(year.joinpath('meta.json')) as f:
                    year_object = json.load(f)

                with open(year.joinpath('tracks.json')) as f:
                    year_object['tracks'] = json.load(f)

                conference_object["years"][year.name] = year_object

            sponsor_object["conferences"][conference.name] = conference_object

        json_object["sponsors"][sponsor.name] = sponsor_object

    return json_object

if __name__ == '__main__':
    with open('stats.json', 'w') as f:
        json.dump(compile_conferencestats('.'), f, indent=4)
