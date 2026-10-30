"""Builds data/dds_leave.db: 100 DDS employees, one branch (Dubai), plus leave requests.

Rules follow DDS-HR-POL-001 v2.0: 22 annual days, 15 sick days, leave year = calendar year.
Balances are COMPUTED from the leave_requests table, so the two tables always agree.
Run:  python3 build_database.py
"""
import random, sqlite3, os
from datetime import date, timedelta

TODAY = date(2026, 10, 28)
YEAR = 2026
rng = random.Random(42)

FIRST = ["Aisha","John","Maria","David","Omar","Fatima","Liam","Sara","Yusuf","Noor","Priya","Rahul","Emma","Hassan",
         "Layla","Daniel","Mei","Carlos","Zainab","Arjun","Sophie","Khalid","Nadia","Tom","Amira","Ravi","Elena","Bilal",
         "Hana","Peter","Reem","Sanjay","Julia","Tariq","Mona","Ethan","Lina","Imran","Chloe","Faisal"]
LAST = ["Khan","Doe","Garcia","Lee","Hassan","Ali","Smith","Patel","Ahmed","Nair","Sharma","Brown","Rahman","Costa",
        "Wang","Ibrahim","Singh","Evans","Haddad","Silva","Mehta","Clarke","Farouk","Reddy","Santos"]
DEPTS = {"Engineering": 22, "Data & AI Training": 20, "Marketing": 14, "Sales": 14, "People & Culture": 6,
         "Finance": 8, "Operations": 10, "Community": 6}
TITLES = {"Engineering": ["Software Engineer","Data Engineer","ML Engineer"],
          "Data & AI Training": ["Instructor","Curriculum Designer","Program Manager"],
          "Marketing": ["Content Lead","Growth Marketer","Designer"],
          "Sales": ["Business Development Associate","Account Manager"],
          "People & Culture": ["HR Partner","Head of People & Culture"],
          "Finance": ["Accountant","Finance Analyst"],
          "Operations": ["Operations Associate","Event Coordinator"],
          "Community": ["Community Manager","Support Specialist"]}

def working_days(start, end):
    d, n = start, 0
    while d <= end:
        if d.weekday() < 5:
            n += 1
        d += timedelta(days=1)
    return n

def next_workday(d):
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d

# --- employees --------------------------------------------------------------------------
people = [(1024,"Aisha Khan","Engineering","Software Engineer"),
          (1025,"John Doe","Marketing","Content Lead"),
          (1026,"Maria Garcia","Data & AI Training","Instructor"),
          (1027,"David Lee","Finance","Finance Analyst")]
used_names = {p[1] for p in people}
slots = [d for d, n in DEPTS.items() for _ in range(n)]
rng.shuffle(slots)
eid = 1000
employees = []
for p in people:
    employees.append(p)
while len(employees) < 100:
    eid += 1
    if eid in (1024,1025,1026,1027):
        continue
    name = f"{rng.choice(FIRST)} {rng.choice(LAST)}"
    if name in used_names:
        continue
    used_names.add(name)
    dept = slots.pop() if slots else "Operations"
    employees.append((eid, name, dept, rng.choice(TITLES[dept])))
employees.sort()

# fixed join dates for the demo people, random for the rest (2019 - mid 2026)
fixed_join = {1024: date(2022,3,14), 1025: date(2024,9,2), 1026: date(2021,1,10), 1027: date(2025,11,3)}

# --- leave requests ---------------------------------------------------------------------
requests = []
rid = 5000
def add(emp, ltype, start, end, status, requested_on=None):
    global rid
    rid += 1
    wd = working_days(start, end)
    requests.append((rid, emp, ltype, start.isoformat(), end.isoformat(), wd, status,
                     (requested_on or start - timedelta(days=rng.randint(8, 40))).isoformat()))

# hand-written story for the four demo employees (used in class)
add(1024,"Annual",date(2026,2,9),date(2026,2,13),"Approved")
add(1024,"Annual",date(2026,6,22),date(2026,7,3),"Approved")           # 10 working days
add(1024,"Sick",date(2026,4,7),date(2026,4,8),"Approved")
add(1024,"Annual",date(2026,12,21),date(2026,12,25),"Approved")       # booked, 5 days
add(1025,"Annual",date(2026,5,4),date(2026,5,8),"Approved")
add(1025,"Sick",date(2026,9,15),date(2026,9,15),"Approved")
add(1025,"Annual",date(2026,11,16),date(2026,11,20),"Pending")
add(1026,"Annual",date(2026,3,2),date(2026,3,6),"Approved")
add(1026,"Annual",date(2026,8,10),date(2026,8,21),"Approved")
add(1026,"Sick",date(2026,1,12),date(2026,1,14),"Approved")
add(1026,"Study",date(2026,5,18),date(2026,5,22),"Approved")
add(1027,"Annual",date(2026,7,6),date(2026,7,10),"Approved")
add(1027,"Sick",date(2026,3,23),date(2026,3,24),"Approved")
add(1027,"Annual",date(2026,12,28),date(2026,12,31),"Rejected")

demo_ids = {1024,1025,1026,1027}
for emp, name, dept, title in employees:
    if emp in demo_ids:
        continue
    # annual leave: 1-3 blocks
    for _ in range(rng.choice([1,2,2,3])):
        start = next_workday(date(YEAR, rng.randint(1,12), rng.randint(1,26)))
        end = start + timedelta(days=rng.choice([0,1,2,4,4,6,9,11]))
        if end.year != YEAR:
            continue
        status = "Approved" if rng.random() < 0.82 else rng.choice(["Pending","Rejected","Cancelled"])
        if status == "Pending" and start <= TODAY:
            status = "Approved"
        add(emp,"Annual",start,end,status)
    # sick leave
    if rng.random() < 0.55:
        start = next_workday(date(YEAR, rng.randint(1,10), rng.randint(1,26)))
        end = start + timedelta(days=rng.choice([0,0,1,2,3]))
        add(emp,"Sick",start,end,"Approved")
    # a few other leave types, in line with the policy
    r = rng.random()
    if r < 0.03:
        s = next_workday(date(YEAR, rng.randint(2,9), 10)); add(emp,"Bereavement",s,s+timedelta(days=2),"Approved")
    elif r < 0.05:
        s = next_workday(date(YEAR, rng.randint(2,9), 12)); add(emp,"Marriage",s,s+timedelta(days=2),"Approved")
    elif r < 0.07:
        s = next_workday(date(YEAR, rng.randint(2,9), 8)); add(emp,"Paternity",s,s+timedelta(days=6),"Approved")

# cap: nobody may exceed their entitlement with APPROVED leave (taken + booked)
def approved(emp, ltype):
    return [r for r in requests if r[1]==emp and r[2]==ltype and r[6]=="Approved"]
for emp, *_ in employees:
    for ltype, cap in (("Annual",22),("Sick",15)):
        total = sum(r[5] for r in approved(emp, ltype))
        for r in sorted(approved(emp, ltype), key=lambda x: x[3], reverse=True):
            if total <= cap:
                break
            requests.remove(r); total -= r[5]

# --- write the database -----------------------------------------------------------------
os.makedirs("data", exist_ok=True)
path = "data/dds_leave.db"
if os.path.exists(path):
    os.remove(path)
con = sqlite3.connect(path)
con.executescript("""
CREATE TABLE employees (
  employee_id INTEGER PRIMARY KEY,
  name TEXT, department TEXT, job_title TEXT, branch TEXT, join_date TEXT,
  annual_total INTEGER, annual_used INTEGER, annual_booked INTEGER, annual_remaining INTEGER,
  sick_total INTEGER, sick_used INTEGER, sick_remaining INTEGER
);
CREATE TABLE leave_requests (
  request_id INTEGER PRIMARY KEY,
  employee_id INTEGER REFERENCES employees(employee_id),
  leave_type TEXT, start_date TEXT, end_date TEXT, working_days INTEGER,
  status TEXT, requested_on TEXT
);
""")
for emp, name, dept, title in employees:
    join = fixed_join.get(emp) or date(rng.randint(2019,2025), rng.randint(1,12), rng.randint(1,28))
    ann = approved(emp,"Annual"); sick = approved(emp,"Sick")
    a_used = sum(r[5] for r in ann if date.fromisoformat(r[3]) <= TODAY)
    a_book = sum(r[5] for r in ann if date.fromisoformat(r[3]) > TODAY)
    s_used = sum(r[5] for r in sick)
    con.execute("INSERT INTO employees VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (emp,name,dept,title,"Dubai HQ",join.isoformat(),22,a_used,a_book,22-a_used-a_book,15,s_used,15-s_used))
con.executemany("INSERT INTO leave_requests VALUES (?,?,?,?,?,?,?,?)", requests)
con.commit()
print("employees:", con.execute("select count(*) from employees").fetchone()[0],
      "| requests:", con.execute("select count(*) from leave_requests").fetchone()[0])
con.close()
