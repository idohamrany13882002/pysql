from functions import connect_db, read_query, update_query, action_query

conn, curser = connect_db("sql_prep4.db")

action_query(curser,conn,"DROP TABLE IF EXISTS garage") # dropping the table if exists
action_query(curser,conn,"""
CREATE TABLE IF NOT EXISTS garage (
    fix_id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_number TEXT UNIQUE NOT NULL,
    car_problem TEXT NOT NULL,
    fixed BOOLEAN DEFAULT FALSE,
    owner_ph TEXT NOT NULL
);
""") #creating table
action_query(curser, conn, """
INSERT INTO garage (car_number, car_problem, fixed, owner_ph)
VALUES
('23', 'Engine overheating after long drives', TRUE, '555-1023'),
('34', 'Brake pads worn out, needs replacement', TRUE, '555-1034'),
('30', 'Check engine light on, possible sensor issue', TRUE, '555-1030'),
('24', 'Battery drains overnight, needs diagnosis', FALSE, '555-1024'),
('3', 'Strange noise from suspension when turning', FALSE, '555-1003');
""") # affiliating the table with data


op_dict: dict[int,str] = {1:"Enter a new car",
                     2:"End session",
                     3:"Remove car for garage",
                     4:"Check availability",
                     5:"Exit"} #print options list for user

for key,value in op_dict.items():
    print(f"{key}: {op_dict[key]}")

op: int = int(input("Choose one of the options above: "))

if op == 1:
    car_num: str = input("Enter car's number: ")
    car_prob: str = input("Enter car's problem: ")
    phone_num: str = input("Enter phone number: ")
    update_query(curser,conn,"INSERT INTO garage (car_number, car_problem, owner_ph) values(?,?,?)",(car_num, car_prob, phone_num))
elif op == 2:
    car_num: int = int(input("Enter car's number: "))
    action_query(curser, conn, "SELECT garage.* FROM garage")
    cars = curser.fetchall()
    answer:list[int] = []
    for car in cars:
        answer.append(int(car["car_number"]))
    if car_num in answer:
        curser.execute("SELECT garage.* FROM garage WHERE car_number = ?", (car_num,))
        rows = curser.fetchall()
        status: int = None
        for row in rows:
            status = int(row["fixed"])
        if status == 1:
            print("Car is ready")
        else:
            curser.execute("""UPDATE garage
            SET fixed = 1
            WHERE car_number = ?;
            """, (car_num,))
        conn.commit()
    else:
        print ("the car is not in the garage")
elif op == 3:
    car_num: int = int(input("Enter car's number: "))
    action_query(curser, conn, "SELECT garage.* FROM garage")
    cars = curser.fetchall()
    answer: list[int] = []
    for car in cars:
        answer.append(int(car["car_number"]))
    if car_num in answer:
        curser.execute("SELECT garage.* FROM garage WHERE car_number = ?", (car_num,))
        rows = curser.fetchall()
        status: int = None
        for row in rows:
            status = int(row["fixed"])
        if status == 0:
            print("Car is not ready")
        else:
            curser.execute("SELECT garage.* FROM garage WHERE car_number = ?;", (car_num,))
            rows = curser.fetchall()
            phone = [row["owner_ph"] for row in rows]
            print(f"Car is ready owner phone number is {phone}")
        conn.commit()
    else:
        print ("the car is not in the garage")
elif op == 4:
    print(read_query(curser,"""
    SELECT garage.* FROM garage
    WHERE fixed is false
    """, tuple))
else:
    print("Goodbye")

conn.close()