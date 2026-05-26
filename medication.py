import os
import json


class MedsCSV:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.isfile(self.filename):
            with open(self.filename, "w") as f:
                f.write('')

    def get_meds(self):
        meds_list = []
        with open(self.filename, 'r') as f:
            for row in f:
                meds_list.append(row.split(','))
        return meds_list

    def add_new_med(self, new_med, dose):
        with open(self.filename, 'a') as f:
            f.write(f"{new_med},{dose}\n")
    def get_med_names(self):
        meds_string_list = []
        with open(self.filename, 'r') as f:
            for row in f:
                meds_string_list.append(row.split(',')[0])
        return meds_string_list

class MedsJSON:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.isfile(self.filename):
            with open(self.filename, "w") as f:
                f.write('{}')

    def get_meds(self):
        data = json.load(open(self.filename, 'r'))
        return dict(data)

    def add_new_med(self, category, new_med, dose):
        data = json.load(open(self.filename, 'r'))
        data[category]["meds"].append({"name": new_med, "dose": dose})
        json.dump(data, open(self.filename, 'w'))

    def add_new_category(self, category):
        data = json.load(open(self.filename, 'r'))
        data[category] = {"meds": []}
        json.dump(data, open(self.filename, 'w'))

    def med_names(self):
        return list(self.get_meds().keys())

    def delete_med(self, category, med_name):
        print(med_name)
        data = json.load(open(self.filename, 'r'))
        category = data[category]
        for medication in category['meds']:
            if medication['name'] == med_name:
                category['meds'].remove(medication)
        json.dump(data, open(self.filename, 'w'))

        json.dump(data, open(self.filename, 'w'))
meds_json = MedsJSON('instance/medication.json')

