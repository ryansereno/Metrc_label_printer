import PySimpleGUI as sg
import requests
import json
from requests.auth import HTTPBasicAuth
from zebra import Zebra
import keys
sg.theme("DarkBlue11")
title_column1 = [sg.Text("Template:", text_color="white", font=("Helevetic", 13), pad=(0,0))]
title_columns2 = [[sg.Text("Tag Number:", text_color="white", font=("Helvetica", 13), pad=(0,0))]]
input_columns2 = [[sg.InputText(key="-UID-", size=(25,1), font=("Helvetica", 14), background_color="white", pad=(0,0), do_not_clear=False), sg.Button("Print", bind_return_key=True)]]
layout2 = [[sg.Image(r"METRC-LOGO.png",
                     size=(125,50), pad=(0,0))],[sg.Column(title_columns2), sg.Column(input_columns2)],
          [sg.Text("© Ryan Sereno 2021", text_color="black" ,font=("Helvetica", 8))]]
error_layout =[[sg.Text("Invalid UID", text_color="white", font=("Helvetica", 13), pad=(10,10))]]
window = sg.Window("Metrc Label Printer", layout2, keep_on_top=True)
error_window = sg.Window("Error", error_layout, keep_on_top=True)

def API_call(x):        #add User key parameter
    # software_key = "ByDuekpGQ8Uyy73vo1en1QslAvJXqMWCe53VVdyBKXedSuxa"
    software_key = keys.soft()
    # user_key = "sK8zzfHHSQaIYMDujGXu09M1zdZ1vAEC80GtBxfGxMpOwoQe"
    user_key = keys.user()
    UID_URL = f"https://api-ca.metrc.com/packages/v1/{x}?licenseNumber=CDPH-10003394"
    r = requests.get(UID_URL, auth=HTTPBasicAuth(software_key, user_key))
    json_resp = r.json()
    resp_string = json.dumps(json_resp, indent=2)
    Quantity = str(json_resp["Quantity"]) + " " + json_resp["UnitOfMeasureAbbreviation"]
    Item = json_resp["Item"]["Name"]
    BatchNumber = json_resp["ProductionBatchNumber"]
    return Quantity, Item, BatchNumber

def Zebra_print(UID, Quantity, Item, BatchNumber):      #add template parameter and printer name parameter
    z = Zebra("Zebra_Technologies_ZTC_ZP_450_200dpi") #add printer name fetching function
    Item_line_one = Item[:25]
    def Item_line_two():
        if len(Item) > 25:
            return Item[25:len(Item)]
        else:
            return ""
    label = "^XA^CFA,30^FO50,40^FDBatch: " + BatchNumber + "^FS^FO50,90^FD" + Item_line_one + "^FS" \
            "^FO50,140^FD" + Item_line_two() + "^FS" \
            "^FO50,190^FD" + UID + "^FS^FO50,240^FDTare:^FS^FO50,290^FDTotal Qnty: " + Quantity + "^FS" \
            "^GB20,20,2,B,1^BCN,40,N,N,N,N^CFA,30" \
            "^FO100,350,0^BY2,2,20^FD" + UID + "^FS" \
            "^FO550,75,0^GB40,40,5,B,1^FS^FO600,85^FDTested^FS" \
            "^FO550,125,0^GB40,40,5,B,1^FS" \
            "^FO600,135^FDFormulated^FS" \
            "^FO550,175,0^GB40,40,5,B,1^FS^FO600,185^FDR&D^FS" \
            "^FO550,225,0^GB40,40,5,B,1^FS^FO600,235^FDHOLD^FS^XZ"
    z.output(label)
    print(BatchNumber)
    print(Item)
    print(Quantity)
    print(UID)

while True:
    event, values = window.read()
    if event == "Print":
        UID = values["-UID-"]
        if UID == "":
            print("null value")
            pass
        else:
            try:
                Quantity, Item, BatchNumber = API_call(UID)
                Zebra_print(UID, Quantity, Item, BatchNumber)
            except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError):
                print("invalid ID/ system error")
                error_window.read()
                input_columns2.clear()
                pass
    if event == sg.WIN_CLOSED:
        window.close()
        break

    #test comment
