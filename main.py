import psycopg2
from faker import Faker
import csv


def save_to_csv(nama_file, data):
    with open(nama_file + '.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data[0].keys())
        for row in data:
            writer.writerow(row.values())


conn = psycopg2.connect(
    dbname="car_bid",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

fake_id = Faker('id_ID')

# data kota
data_kota = []
# read data from csv
with open('city.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        data_kota.append(
            {
                'kota_id': row[0],
                'nama_kota': row[1],
                'latitude': row[2],
                'longitude': row[3]

            }
        )
#  delete first row
data_kota.pop(0)
sql_kota = 'INSERT INTO kota (kota_id, nama_kota, latitude, longitude) VALUES (%(kota_id)s, %(nama_kota)s, %(latitude)s, %(longitude)s) '
cur.executemany(sql_kota, data_kota)


# data user
data_user = []
for i in range(20):
    data_user.append(
        {
            'nama': fake_id.name(),
            'kota_id': data_kota[fake_id.random_int(min=0, max=14)]['kota_id'],
            'kontak': fake_id.phone_number()
        }
    )

save_to_csv('data_user', data_user)
sql_user = 'INSERT INTO "user" (nama, kota_id, kontak) VALUES (%(nama)s, %(kota_id)s, %(kontak)s) '
cur.executemany(sql_user, data_user)
#  check if data is successfully inserted
cur.execute('SELECT * FROM "user"')

# data iklan
data_iklan = []
merk = ['Toyota', 'Honda', 'Mitsubishi', 'Suzuki', 'Daihatsu',
        'Nissan', 'BMW', 'Mercedes', 'Audi', 'Volkswagen']
jenis = ['Sedan', 'SUV', 'MPV', 'Hatchback', 'Coupe',
         'Convertible', 'Wagon', 'Pickup', 'Van', 'Minivan']
model = ['Avanza', 'Yaris', 'Innova', 'Fortuner', 'Camry', 'Corolla', 'Alphard', 'Vellfire', 'C-HR', 'Prius',
         'Civic', 'Jazz', 'Accord', 'CR-V', 'HR-V', 'Odyssey', 'Pilot', 'City', 'BR-V', 'CR-Z',]
for i in range(200):
    data_iklan.append(
        {
            'judul': fake_id.sentence(nb_words=6, variable_nb_words=True),
            'merk': fake_id.random_element(elements=merk),
            'model': fake_id.random_element(elements=model),
            'jenis_body': fake_id.random_element(elements=jenis),
            'transmission': fake_id.random_element(elements=('Manual', 'Automatic')),
            'tahun': fake_id.year(),
            'deskripsi': fake_id.paragraph(nb_sentences=3, variable_nb_sentences=True),
            'price': fake_id.random_int(min=80_000_000, max=500_000_000),
            'date': fake_id.date_time_between(start_date='-1y', end_date='now'),
            'user_id': fake_id.random_int(min=1, max=20),
            'kota_id': data_kota[fake_id.random_int(min=0, max=14)]['kota_id'],
            # 'id': i+1
        }
    )
save_to_csv("data_iklan", data_iklan)
sql_iklan = 'INSERT INTO iklan (judul, merk, model, jenis_body, transmission, tahun, deskripsi, price, date, user_id, kota_id) VALUES (%(judul)s, %(merk)s, %(model)s, %(jenis_body)s, %(transmission)s, to_date(%(tahun)s, \'YYYY\'), %(deskripsi)s, %(price)s, %(date)s, %(user_id)s, %(kota_id)s) '
cur.executemany(sql_iklan, data_iklan)
#  check if data is successfully inserted
cur.execute('SELECT * FROM iklan')


# data bid
data_bid = []
data_relation = []
status = ['SENT', 'CANCELLED']
for i in range(500):
    #  get user_id from data_user

    rand_iklan = fake_id.random_int(min=1, max=50)
    iklan_id = rand_iklan
    iklan_user_id = data_iklan[rand_iklan-1]['user_id']

    # bid_id = i+1
    bid_user_id = fake_id.random_int(min=1, max=20)

    data_bid.append(
        {
            'status': fake_id.random_element(elements=status),
            'price': fake_id.random_int(min=80_000_000, max=500_000_000),
            'date': fake_id.date_time_between(start_date='-1y', end_date='now'),
            'user_id': bid_user_id
        }
    )
    data_relation.append(
        {
            'iklan_id': iklan_id,
            'iklan_user_id': iklan_user_id,
            'bid_id': i+1,
            'bid_user_id': bid_user_id
        }
    )
save_to_csv("data_bid", data_bid)
sql_bid = 'INSERT INTO bid (date, price, status, user_id) VALUES (%(date)s, %(price)s, %(status)s, %(user_id)s) '
cur.executemany(sql_bid, data_bid)

save_to_csv("data_relation", data_relation)
sql_relation = 'INSERT INTO iklan_has_bid (iklan_id, iklan_user_id, bid_id, bid_user_id) VALUES (%(iklan_id)s, %(iklan_user_id)s, %(bid_id)s, %(bid_user_id)s) '
cur.executemany(sql_relation, data_relation)

# commit data
conn.commit()

# close connection
conn.close()
