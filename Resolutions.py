import csv
import json

resolutions =[]
def res_already_in_list(resolutions, width, height):
    for index in range(len(resolutions)):
        if resolutions[index]["width"] == width and resolutions[index]["height"] == height:
            return True, index
    return False, -1

with open('Res_list.csv', newline="") as res_csv:
    res_reader = csv.reader(res_csv, delimiter=",")
    for row in res_reader:
        dictionary = {}
        dictionary["device"] = row[0].replace(" ", "_")
        res_list = row[1].split(" x ")
        width = int(res_list[0])
        dictionary["width"] = width
        height = int(res_list[1])
        dictionary["height"] = height
        dictionary["other_devices"] = []
        is_in_list, index = res_already_in_list(resolutions, width, height)
        if is_in_list:
            resolutions[index]["other_devices"].append(row[0].replace(" ", "_"))
        else:
            resolutions.append(dictionary)


with open('res_list.json', "w") as res_json:
    json.dump(resolutions, res_json, indent=4)
