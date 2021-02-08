import mysql.connector
import numpy as np
def register_person_id(person_id, person_name):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="csd"
    )
    cursor = db.cursor()
    sql = "INSERT INTO person_id_name(person_id, person_name) VALUE(%s, %s)"
    value = ([person_id, person_name])
    cursor.execute(sql, value)
    # db.commit()  # 数据表内容有更新，必须使用到该语句
    # feature = np.array([1, 3, 4, 5])
    # bytes_feature = feature.tostring()
    # cursor.execute('insert into feature(person_id, face_id, feature) values(%s,%s,%s)', ([2, 4, bytes_feature]))
    db.commit()  # 数据表内容有更新，必须使用到该语句
def register_face_feature(person_id, face_id, feature_vector):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="csd"
    )
    cursor = db.cursor()
    # print(np.array(feature_vector).shape)
    bytes_feature_vector = feature_vector.tostring()
    sql = "insert into feature_vector(person_id, face_id, feature_vector) values (%s, %s, %s)"
    value = ([person_id, face_id, bytes_feature_vector])
    cursor.execute(sql, value)
    db.commit()
def find_person_id_by_name(person_name):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="csd"
    )
    cursor = db.cursor()
    sql = "SELECT person_id from person_id_name WHERE person_name = (%s)"

    value = ([person_name])
    cursor.execute(sql, value)
    # db.commit()  # 数据表内容有更新，必须使用到该语句
    # feature = np.array([1, 3, 4, 5])
    # bytes_feature = feature.tostring()
    # cursor.execute('insert into feature(person_id, face_id, feature) values(%s,%s,%s)', ([2, 4, bytes_feature]))
    # db.commit()  # 数据表内容有更新，必须使用到该语句
    values = cursor.fetchall()
    return values[0][0]
def load():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="csd"

    )
    cursor = db.cursor()
    sql = 'select person_id, feature_vector from csd.feature_vector'
    cursor.execute(sql)
    values = cursor.fetchall()

    # result = []
    # for i in range(0, len(values)):
    #     values[i][1] = np.frombuffer(values[i][1], dtype=np.float32)
        # result.append(feature)
    # relust = [ [ id1, feature_tostring1 ],
    #            [ id2, feature_tostring2 ]]
    # print(values)
    return values
def find_person_name_by_person_id(person_id):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="csd"
    )
    cursor = db.cursor()
    sql = 'select person_name from csd.person_id_name where person_id = (select person_id from csd.feature_vector where person_id = (%s))'
    val = ([person_id])
    cursor.execute(sql, val)
    values = cursor.fetchall()
    return values[0][0]

    # result = []
    # for i in range(0, len(values)):
    #     values[i][1] = np.frombuffer(values[i][1], dtype=np.float32)
        # result.append(feature)
    # relust = [ [ id1, feature_tostring1 ],
    #            [ id2, feature_tostring2 ]]
    # print(values)
    # return values
# print(register_person_id(3, 'Leonardo'))

# feature = np.loadtxt('features/Leonardo1.txt', dtype=np.float32)
# print(feature,feature.shape, type(feature))
# print(register_face_feature(1,2,feature))
# print(np.frombuffer(load()[0][1], dtype=np.float32).shape)
def R1():
    import os
    feature_dir = os.listdir('features/')
    index = 1
    for i in feature_dir:
        register_person_id(index, i.split('.')[0])
        feature_vector = np.loadtxt('features/' + i, dtype=np.float32)
        # print(feature_vector.shape)

        index += 1
        register_face_feature(find_person_id_by_name(i.split('.')[0]), 1, np.array(feature_vector))
# R1()
# print(find_person_name_by_person_id(10))
def test():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="csd"
    )
    cursor = db.cursor()
    npa = np.array([[-3.57415378e-01, -1.91270351e-01, 8.77791524e-01, -7.07533717e-01,
                     -1.13954544e-01, 1.59952372e-01, 5.69643378e-01, 3.23965818e-01,
                     -1.45808721e+00, -1.10797346e+00, -5.85695386e-01, -3.85645986e-01,
                     1.62441760e-01, 2.64832902e+00, -9.41478252e-01, 1.19124746e+00,
                     -9.13884044e-01, 7.92207062e-01, -2.07454681e-01, -2.27513742e+00,
                     9.38329101e-01, 6.00685716e-01, -7.34502435e-01, -1.27206609e-01,
                     7.65696228e-01, -8.15190017e-01, 1.77376606e-02, 3.38444591e-01,
                     -3.70283276e-01, -4.58475769e-01, 1.49238157e+00, 6.09451532e-03,
                     2.85512537e-01, -1.59730721e+00, 1.01230800e+00, 4.96441633e-01,
                     1.03817381e-01, -9.55118179e-01, -4.19647872e-01, -8.08892678e-03,
                     -4.21005249e-01, -1.76366174e+00, -2.20537156e-01, -8.20649505e-01,
                     4.60948855e-01, -1.77652812e+00, -3.91574025e-01, 3.26310605e-01,
                     9.71992850e-01, 3.53105456e-01, 2.84943879e-01, -1.08534634e+00,
                     -5.31805158e-01, 1.51520872e+00, 1.74533248e+00, -5.16480684e-01,
                     -2.01253414e-01, -1.54071164e+00, 2.71417886e-01, 2.50432670e-01,
                     4.13581520e-01, -1.35138854e-01, 1.50658202e+00, 5.96220851e-01,
                     -9.56330895e-01, -5.88566303e-01, 1.77457678e+00, -1.87112376e-01,
                     -5.90639472e-01, -5.65512657e-01, 5.62599421e-01, 4.94422823e-01,
                     -6.98078215e-01, 5.12796044e-01, 9.27187502e-02, -2.49068290e-01,
                     -8.04589391e-02, 5.35208583e-01, 2.87937075e-01, -6.34572983e-01,
                     -6.62812829e-01, 1.37663770e+00, 8.61887097e-01, -4.51743335e-01,
                     -6.90884888e-02, -1.46354198e+00, 1.28368545e+00, 6.41699314e-01,
                     1.63930804e-01, 9.60422933e-01, -8.76205087e-01, -3.28382641e-01,
                     -5.54804623e-01, -1.25851250e+00, 4.05085832e-03, 8.67565513e-01,
                     -1.77942014e+00, -1.11033058e+00, 1.23444796e+00, -5.89355052e-01,
                     1.45706737e+00, 3.34731132e-01, -1.14689767e+00, 1.46356806e-01,
                     -3.56782019e-01, -1.80544674e+00, 1.95076957e-01, 9.79840875e-01,
                     -4.39509213e-01, 1.26948595e+00, -5.80784976e-02, -2.82809436e-02,
                     -1.16628432e+00, 1.26023114e-01, 9.53356564e-01, 4.95627075e-01,
                     2.30762625e+00, 6.29761934e-01, -5.79455078e-01, 2.73870420e+00,
                     -1.50105608e+00, -1.83120966e+00, -7.66552567e-01, 6.94787502e-02,
                     -3.92213374e-01, 3.76526535e-01, 1.57209349e+00, -1.26317084e+00,
                     1.03692937e+00, 9.29199040e-01, -8.16896975e-01, -6.15737021e-01,
                     2.40580112e-01, 8.75885189e-02, -7.67888129e-01, -4.63138372e-01,
                     8.72819543e-01, 3.59745622e-02, -5.76106191e-01, 5.40735602e-01,
                     1.80201697e+00, 1.01401281e+00, 1.58961043e-01, -2.46845531e+00,
                     -7.01887786e-01, -5.02803266e-01, 1.12521851e+00, 1.73173845e+00,
                     3.11720759e-01, 8.52062106e-01, -6.14436090e-01, -9.51389968e-03,
                     2.94235975e-01, -4.25003588e-01, -5.98602295e-01, -4.39488381e-01,
                     1.06172729e+00, 1.36453247e+00, -2.49283642e-01, -1.37132883e+00,
                     2.99910635e-01, 1.66915345e+00, 2.39976555e-01, 2.32457876e-01,
                     1.06126821e+00, 8.79389226e-01, 5.16353667e-01, -5.32266259e-01,
                     -1.06272507e+00, 4.74590272e-01, -1.00683188e+00, -6.35726213e-01,
                     -9.53140259e-01, -1.56878626e+00, -5.09122491e-01, 3.11952680e-02,
                     -2.05704880e+00, 1.33341670e-01, -1.12209463e+00, 5.45685887e-01,
                     -6.23563826e-02, -1.44081640e+00, 5.24943233e-01, 1.59003723e+00,
                     -1.25019705e+00, -3.51860344e-01, 5.77616096e-02, 2.71759927e-03,
                     1.23379517e+00, 6.51743770e-01, 5.13698637e-01, 6.28805220e-01,
                     -2.11730272e-01, 1.66839495e-01, 5.25779426e-02, -4.87758219e-01,
                     1.46388912e+00, -6.90768957e-02, -4.59372878e-01, 7.30657160e-01,
                     -2.60671437e-01, -7.50087798e-02, 7.73952723e-01, 2.65331060e-01,
                     -2.49902904e-01, -4.68800426e-01, 5.81122041e-01, 8.48922849e-01,
                     5.90246320e-01, 4.47421968e-01, 1.03455901e+00, 2.22669125e-01,
                     -1.16688228e+00, 1.31708109e+00, -8.81451845e-01, -8.30954075e-01,
                     4.52138454e-01, -1.94497883e-01, -5.77958703e-01, 9.95233774e-01,
                     -1.91323471e+00, -4.75410670e-01, 2.12810755e+00, -3.03934693e-01,
                     1.14643764e+00, -6.59597099e-01, 4.33283508e-01, -3.19920480e-01,
                     2.10988641e-01, 6.05047226e-01, 2.17050925e-01, 4.26506028e-02,
                     5.64077616e-01, -3.78873587e-01, 1.31337285e+00, 5.21751642e-01,
                     -7.34216154e-01, -4.29867625e-01, -1.01178813e+00, 8.40794623e-01,
                     -6.80967510e-01, 1.13342834e+00, -7.02221766e-02, -6.83880627e-01,
                     -1.02442719e-01, -9.26198363e-01, -7.88610101e-01, -1.15891480e+00,
                     4.15042043e-01, -3.30958724e-01, -4.09226000e-01, -8.72564763e-02,
                     -1.48877501e+00, -1.21281576e+00, -3.05882812e-01, 1.10878378e-01]])
    bytes_feature_vector = npa.tostring()
    sql = 'select * from csd.feature_vector where feature_vector = (%s)'
    val = ([bytes_feature_vector])
    # sql = 'select feature_vector from csd.feature_vector'
    cursor.execute(sql, val)
    values = cursor.fetchall()
    # print(values)
    result = []
    for i in range(0, len(values)):
        feature = np.frombuffer(values[i][0], dtype=np.float32)
        result.append(feature)
    return result
# print(test())