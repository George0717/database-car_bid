# car-bid
Merupakan sebuah desain database sederhana untuk pelelangan mobil.


blog : [Desain Database Lelang Mobil](https://blog.mrayhanfadil.my.id/desain-database-lelang-mobile/)

youtube : [Relational Database Pacmann - Car Bid](https://youtu.be/ef-qpjmwB8I)


## ERD

![image](https://user-images.githubusercontent.com/55126764/232323710-5793c2f8-2b21-4a35-a9b3-28c4b1ac5192.png)

## DDL

```sql
CREATE TABLE kota (
  kota_id INTEGER PRIMARY KEY,
  nama_kota TEXT NOT NULL,
  latitude NUMERIC(9, 6) NOT NULL,
  longitude NUMERIC(9, 6) NOT NULL
);

CREATE TABLE "user" (
  user_id SERIAL PRIMARY KEY,
  nama VARCHAR(225) NOT NULL,
  kontak VARCHAR(45) NOT NULL,
  kota_id INTEGER NOT NULL,
  CONSTRAINT fk_user_kota
    FOREIGN KEY (kota_id)
    REFERENCES "kota" (kota_id)
);

CREATE TABLE "iklan" (
  iklan_id SERIAL NOT NULL,
  judul VARCHAR(225) NOT NULL,
  merk VARCHAR(45) NOT NULL,
  model VARCHAR(45) NOT NULL,
  jenis_body VARCHAR(45) NOT NULL,
  transmission VARCHAR(45) NOT NULL,
  tahun DATE NOT NULL,
  deskripsi TEXT NOT NULL,
  price INT NOT NULL,
  date DATE NOT NULL,
  user_id INT NOT NULL,
  kota_id INT NOT NULL,
  PRIMARY KEY (iklan_id, user_id),
  CONSTRAINT fk_iklan_user
    FOREIGN KEY (user_id)
    REFERENCES "user" (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_iklan_kota
    FOREIGN KEY (kota_id)
    REFERENCES "kota" (kota_id)
);

CREATE TABLE "bid" (
  bid_id SERIAL  NOT NULL,
  status VARCHAR(45) NOT NULL,
  price INT NOT NULL,
  date DATE NOT NULL,
  user_id INT NOT NULL,
  PRIMARY KEY (bid_id, user_id),
  CONSTRAINT fk_bid_user
    FOREIGN KEY (user_id)
    REFERENCES "user" (user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE TABLE iklan_has_bid (
  iklan_has_bid_id SERIAL NOT null,
  iklan_id INT NOT NULL,
  iklan_user_id INT NOT NULL,
  bid_id INT NOT NULL,
  bid_user_id INT NOT NULL,
  PRIMARY KEY (iklan_has_bid_id, iklan_id, iklan_user_id, bid_id, bid_user_id),
  CONSTRAINT fk_iklan_has_bid_iklan
    FOREIGN KEY (iklan_id, iklan_user_id)
    REFERENCES iklan (iklan_id, user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_iklan_has_bid_bid
    FOREIGN KEY (bid_id, bid_user_id)
    REFERENCES bid (bid_id, user_id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
```

## Contoh pembuatan dummy data
Berikut ini merupakan contoh pembuatan dummy data kota dan user. Contoh lain dapat dilihat langsung pada file [main.py](https://github.com/Fadil3/car-bid/blob/master/main.py).
```python
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
```
