import csv

rows = [
    ["C1001",85,82,12,12,420,405,54,8200],
    ["C1002",90,34,14,7,510,190,31,12500],
    ["C1003",72,68,10,10,350,340,61,7600],
    ["C1004",55,18,8,3,260,85,22,9800],
    ["C1005",30,42,4,6,120,180,67,2100],
    ["C1006",95,91,16,15,620,600,58,15200],
    ["C1007",80,25,11,5,410,120,18,11300],
    ["C1008",44,41,6,6,190,175,49,3400],
    ["C1009",66,20,9,4,300,95,27,8700],
    ["C1010",25,39,3,5,90,155,72,1800],
    ["C1011",88,84,13,12,470,450,63,13400],
    ["C1012",61,57,8,8,280,265,52,5900],
    ["C1013",78,29,10,5,390,130,24,10400],
    ["C1014",35,31,5,5,140,125,46,2700],
    ["C1015",92,86,15,14,550,525,59,14100],
    ["C1016",70,16,9,3,330,70,12,11900],
    ["C1017",28,46,4,7,110,205,75,2300],
    ["C1018",58,55,7,7,240,230,51,4800],
    ["C1019",83,30,12,5,440,145,19,12800],
    ["C1020",40,43,5,6,160,175,64,3200],
]

header = [
    "customer_id",
    "previous_month_activity",
    "current_month_activity",
    "survey_count_previous",
    "survey_count_current",
    "response_count_previous",
    "response_count_current",
    "nps_score",
    "historical_customer_value",
]

with open(
    "audit/survicate/data/customer_engagement.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print("Synthetic CSV created successfully.")
print("Customers:", len(rows))
