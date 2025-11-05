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

    def add_new_med(self, new_med, dose):
        data = json.load(open(self.filename, 'r'))
        data[f"{new_med}"] = dose
        json.dump(data, open(self.filename, 'w'))

    def med_names(self):
        return list(self.get_meds().keys())

    def delete_med(self, med):
        data = json.load(open(self.filename, 'r'))
        del data[f"{med}"]
        json.dump(data, open(self.filename, 'w'))
meds_json = MedsJSON('instance/medication.json')

