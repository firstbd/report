import sqlite3
from flask import Flask, jsonify, render_template, request

conn = sqlite3.connect('./oyghs_fin.sqlite3', check_same_thread=False)
cur = conn.cursor()

## 처음에 oyghs_fin.sqlite3 파일이 없을때만 실행! ##
# with open('./온양여고 결과물 데이터.sql', 'r', encoding='utf-8') as f:
#     sql = f.read()
#
# cur.executescript(sql)
# conn.commit()


app = Flask(__name__)
@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

@app.route('/doctors', methods=['POST'])
def get_doctors():
    print(request.form)
    name = request.form['name']
    if name == "all":
        res = cur.execute("""
                select name
                from doctors
                """)
    elif name == "all_cols":
        res = cur.execute("""
                select *
                from doctors
                """)
    else:
        res = cur.execute("""
                select *
                from doctors
                where "name" = :doctor_name
                """, {"doctor_name": name}) # 여기가 named parameter 적용한 부분!

    return jsonify({"result": list(res.fetchall())})

@app.route('/medications', methods=['POST'])
def get_medications():
    print(request.form)
    name = request.form['name']
    if name == "all":
        res = cur.execute("""
                select name
                from medications
                """)
    elif name == "all_cols":
        res = cur.execute("""
                select *
                from medications
                """)
    else:
        res = cur.execute("""
                select *
                from medications
                where "name" = :medication_name
                """, {"medication_name": name}) # 여기가 named parameter 적용한 부분!

    return jsonify({"result": list(res.fetchall())})

@app.route('/patients', methods=['POST'])
def get_patients():
    print(request.form)
    name = request.form['name']
    if name == "all":
        res = cur.execute("""
                select name
                from patients
                """)
    elif name == "all_cols":
        res = cur.execute("""
                select *
                from patients
                """)
    else:
        res = cur.execute("""
                select *
                from patients
                where "name" = :patient_name
                """, {"patient_name": name}) # 여기가 named parameter 적용한 부분!

    return jsonify({"result": list(res.fetchall())})

@app.route('/prescriptions', methods=['POST'])
def get_prescriptions():
    print(request.form)
    name = request.form['name']
    if name == "all":
        res = cur.execute("""
                select patients.name
                from (prescriptions left join patients on prescriptions.patient_id = patients.patient_id) left join medications on prescriptions.medication_id = medications.medication_id
                """)
    elif name == "all_cols":
        res = cur.execute("""
                select prescription_id, patients.name, medications.name, start_date, enddate
                from (prescriptions left join patients on prescriptions.patient_id = patients.patient_id) left join medications on prescriptions.medication_id = medications.medication_id
                """)
    else:
        res = cur.execute("""
                select prescription_id, patients.name "PName", medications.name, start_date, enddate
                from (prescriptions left join patients on prescriptions.patient_id = patients.patient_id) left join medications on prescriptions.medication_id = medications.medication_id
                where "PName" = :patient_name
                """, {"patient_name": name}) # 여기가 named parameter 적용한 부분!

    return jsonify({"result": list(res.fetchall())})

@app.route('/records', methods=['POST'])
def get_records():
    print(request.form)
    name = request.form['name']
    result = {}
    if name == "all":
        res = cur.execute("""
                select patients.name
                from (records left join patients on records.patient_id = patients.patient_id) left join doctors on records.doctor_id = doctors.doctor_id
                """)
        result["result1"] = list(res.fetchall())
        result["result2"] = []
    elif name == "all_cols":
        res = cur.execute("""
                select record_id, patients.name, doctors.name, diagnosis, prescription_id
                from (records left join patients on records.patient_id = patients.patient_id) left join doctors on records.doctor_id = doctors.doctor_id
                """)
        result["result1"] = list(res.fetchall())
        result["result2"] = []
    else:
        res = cur.execute("""
                select record_id, patients.name "PName", doctors.name, diagnosis, prescription_id
                from (records left join patients on records.patient_id = patients.patient_id) left join doctors on records.doctor_id = doctors.doctor_id
                where "PName" = :patient_name
                """, {"patient_name": name}) # 여기가 named parameter 적용한 부분!
        result["result1"] = list(res.fetchall())
        res = cur.execute("""
                        select prescription_id, patients.name "PName", medications.name, dosage, frequency, start_date, enddate
                        from (prescriptions left join patients on prescriptions.patient_id = patients.patient_id) left join medications on prescriptions.medication_id = medications.medication_id
                        where "PName" = :patient_name
                        """, {"patient_name": name})
        result["result2"] = list(res.fetchall())

    return jsonify(result)

app.run(debug=False, port=5001)

conn.close()