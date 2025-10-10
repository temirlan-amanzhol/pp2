import os
import json

print(os.getcwd())

json_path = os.path.join(os.getcwd(), "sample-data.json")

if not os.path.exists(json_path):
    print("File not found:", json_path)
else:
    with open(r"C:\Users\ASUS\Downloads\bob\guga\tasky4\sample-data.json") as f:
        data = json.load(f)


    print("Interface Status")
    print("=" * 60)
    print("DN".ljust(50), "Description".ljust(20), "Speed".ljust(10), "MTU")
    print("-" * 60)

    for item in data["imdata"]:
        dn = item["l1PhysIf"]["attributes"]["dn"]
        desc = item["l1PhysIf"]["attributes"]["descr"]
        speed = item["l1PhysIf"]["attributes"]["speed"]
        mtu = item["l1PhysIf"]["attributes"]["mtu"]
        print(f"{dn:50}{desc:20}{speed:10}{mtu}")
