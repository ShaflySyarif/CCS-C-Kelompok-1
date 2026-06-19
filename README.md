# Secure Serverless Voting System

Sistem voting berbasis cloud yang dibangun menggunakan arsitektur AWS Serverless. Proyek ini memanfaatkan layanan AWS untuk menyediakan sistem voting yang aman, scalable, dan tidak memerlukan pengelolaan server secara langsung.

---

# Gambaran Umum

Sistem memungkinkan pengguna untuk melakukan voting melalui website yang di-host pada Amazon S3. Seluruh request diproses menggunakan Amazon API Gateway dan AWS Lambda, sedangkan data voting disimpan pada Amazon DynamoDB. Proses autentikasi dan otorisasi pengguna dilakukan menggunakan Amazon Cognito.

Dengan pendekatan serverless, sistem tidak memerlukan instance EC2 ataupun web server tradisional sehingga lebih sederhana dalam pengelolaan dan lebih efisien dari sisi biaya.

---

# Arsitektur Sistem

```text
User
 │
 ▼
Amazon S3
(Frontend Hosting)
 │
 ▼
Amazon API Gateway
(API Management)
 │
 ▼
AWS Lambda
(Business Logic)
 │
 ├───────────────┐
 ▼               ▼
Amazon        Amazon
DynamoDB      Cognito
(Database)    Authentication
```

---

# Layanan AWS yang Digunakan

| Service | Fungsi |
|----------|----------|
| Amazon S3 | Hosting website frontend |
| Amazon API Gateway | Mengelola endpoint API |
| AWS Lambda | Menjalankan logika aplikasi |
| Amazon DynamoDB | Menyimpan data voting |
| Amazon Cognito | Autentikasi pengguna |

---

# Fitur Sistem

## Voting Pengguna

- Melakukan voting melalui website
- Menggunakan token voting unik
- Setiap token hanya dapat digunakan satu kali

## Autentikasi

- Login menggunakan Amazon Cognito
- JWT (JSON Web Token) untuk otorisasi
- Endpoint tertentu hanya dapat diakses oleh pengguna yang terverifikasi

## Manajemen Voting

- Perhitungan suara secara real-time
- Validasi token sebelum voting
- Pencegahan double voting

## Dashboard Admin

- Melihat hasil voting
- Menampilkan jumlah suara masing-masing kandidat
- Akses terbatas untuk admin

---

# Alur Voting

## Voting Menggunakan Token

```text
User
 │
 ▼
Memasukkan Token
 │
 ▼
Memilih Kandidat
 │
 ▼
Submit Vote
 │
 ▼
API Gateway
 │
 ▼
AWS Lambda
 │
 ▼
Validasi Token
 │
 ▼
DynamoDB
 │
 ▼
Suara Tersimpan
 │
 ▼
Token Ditandai Sebagai Digunakan
```

---

## Voting Menggunakan Login Cognito

```text
User Login
 │
 ▼
Amazon Cognito
 │
 ▼
JWT Token
 │
 ▼
API Gateway
 │
 ▼
AWS Lambda
 │
 ▼
DynamoDB
```

---

# Desain Basis Data

## Tabel VoterTokens

Digunakan untuk menyimpan token voting dan status penggunaannya.

Contoh data:

```json
{
  "token_id": "ABC123",
  "is_used": false
}
```

Setelah digunakan:

```json
{
  "token_id": "ABC123",
  "is_used": true
}
```

---

## Tabel ElectionResults

Digunakan untuk menyimpan jumlah suara setiap kandidat.

Contoh data:

```json
{
  "candidate_id": "Candidate_A",
  "vote_count": 120
}
```

---

# Mekanisme Keamanan

## Autentikasi JWT

Amazon Cognito menghasilkan JWT setelah pengguna berhasil login.

## Validasi Token

Token voting diverifikasi sebelum suara diproses.

## Pencegahan Double Voting

Token yang telah digunakan akan ditandai sebagai:

```json
{
  "is_used": true
}
```

Sehingga tidak dapat digunakan kembali.

## Kontrol Akses

Akses dashboard admin dibatasi menggunakan autentikasi dan otorisasi pengguna.

---

# Keunggulan Arsitektur Serverless

## Scalability

AWS Lambda dapat melakukan scaling otomatis sesuai jumlah request yang masuk.

## Cost Efficient

Biaya komputasi hanya dikenakan ketika fungsi dijalankan.

## High Availability

Menggunakan layanan AWS yang memiliki tingkat ketersediaan tinggi.

## Low Maintenance

Tidak memerlukan pengelolaan server, patching, maupun konfigurasi infrastruktur secara manual.

---

# Teknologi yang Digunakan

## Frontend

- HTML
- CSS
- JavaScript

## Backend

- Python
- AWS Lambda

## Database

- Amazon DynamoDB

## Cloud Services

- Amazon S3
- Amazon API Gateway
- Amazon Cognito
