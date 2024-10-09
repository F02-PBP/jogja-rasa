# JogjaRasa 🍛 

\~ Selamat datang di JogjaRasa! \~

> Proyek ini dibuat dalam memenuhi tugas Proyek Tengah Semester (PTS) pada mata kuliah Pemrograman Berbasis Platform (CSGE602022).

## 👥 Anggota Kelompok (F02)
Selamat datang di repositori kelompok kami ^___^
| Nama | NPM | Github | 
| -- | -- | -- |
| Grace Karina | 2306275834 | gracekarinn |
| Claudia Paskalia Koesno | 2306275355 | ravenalaa
| Palastha Zhorif Kawiswara | 2306245705 | astzkkk99 |
| Darren Aldrich | 2306206856 | Dardrich
| Adam Caldipawell Sembiring | 232306227160 | AdamCS-code |

## 📜 Cerita Aplikasi

JogjaRasa adalah aplikasi yang dirancang untuk memperkenalkan kekayaan kuliner Daerah Istimewa Yogyakarta dan mewujudkan Gastronomi Nusantara. Nama "JogjaRasa" berasal dari kata "Yogyakarta," sebuah provinsi di Indonesia yang terletak di timur Pulau Jawa, dan kata "Rasa," yang berarti cita rasa. Dengan demikian, JogjaRasa mencerminkan cita rasa khas makanan Yogyakarta. Aplikasi ini memfasilitasi pengguna dalam menemukan rekomendasi tempat makan, baik berdasarkan jenis makanan yang dicari maupun lokasinya. Selain itu, JogjaRasa juga memungkinkan pengguna untuk terhubung dengan pengguna lain melalui forum, memberikan penilaian terhadap restoran, serta markah (_bookmark_).

## 📚 Daftar Modul
Berikut ini adalah daftar modul yang akan kami implementasikan beserta pengembang dari setiap modul.

| Modul | Penjelasan | Pengembang |
| -- | -- | -- |
| **Product (Homepage)** | Menampilkan berbagai restoran beserta daftar makanan yang ditawarkan. Fitur *search engine* memungkinkan pengguna mencari berbagai jenis makanan dan restoran sesuai keinginan. Pencarian ini akan mengutamakan hasil yang paling relevan dan dekat dengan lokasi pengguna saat itu. Selain itu, sistem akan memberikan rekomendasi makanan yang disesuaikan dengan preferensi pengguna. | Grace |
| **Bookmark** | Pengguna dapat menyimpan restoran favorit mereka untuk akses cepat di lain waktu. Pengguna dapat menandai restoran yang mereka sukai, dan restoran tersebut akan tersimpan dalam daftar *bookmark*. Selain itu, pengguna juga dapat melihat, mengelola, atau mengunjungi kembali restoran-restoran yang sudah di-bookmark. | Darren |.
| **Review** | Pengguna dapat memberikan penilaian terhadap restoran yang sudah dikunjungi. Pengguna dapat memberikan *rating* berupa bintang, menulis komentar, serta mengunggah foto makanan atau suasana restoran. Ulasan ini akan membantu pengguna lain dalam mendapatkan gambaran yang lebih jelas mengenai pengalaman di restoran tersebut. | Adam |
| **Reservasi**| Melakukan pemesanan makanan di restoran secara online. Setiap reservasi diterbitkan dalam bentuk tiket digital. Tiket ini dapat diupdate sesuai dengan kebutuhan pengguna, seperti perubahan waktu atau jumlah pesanan. Selain itu, pengguna juga dapat melihat riwayat tiket reservasi yang telah dibuat sebelumnya. | Claudia |
| **Rekomendasi (Forum)** | Modul Rekomendasi (Forum) memungkinkan pengguna untuk membuat diskusi seputar restoran atau makanan tertentu. Pengguna dapat memulai topik baru, dan pengguna lain dapat berpartisipasi dengan memberikan tanggapan atau komentar pada topik yang sudah ada. Forum ini bertujuan untuk memfasilitasi interaksi antar pengguna dalam berbagi rekomendasi dan pengalaman kuliner. | Astha |

## 🕵️ *Role* atau Peran Pengguna 
### 1. 👨‍💻 User
#### 🔓 User yang Sudah Terautentikasi
- Mengakses informasi mengenai restoran dan makanan yang telah disesuaikan dengan preferensi pribadi.
- Menambah dan menghapus restoran pada daftar *bookmark*.
- Memberikan rating dan review untuk restoran yang dipilih.
- Membuat, mengupdate, dan melihat riwayat tiket reservasi.
- Membuat topik baru, memberikan tanggapan, dan berpartisipasi dalam diskusi forum.

#### 🔒 User yang Belum Terautentikasi
- Melihat restoran, makanan yang ditawarkan, dan menggunakan fitur pencarian restoran terdekat.
- Melihat review dan rating dari pengguna lain.
- Melihat diskusi yang sudah ada, tanpa memberikan tanggapan atau membuat topik baru.

### 2. 👩‍💻 Admin
- Menghapus user yang terdaftar pada aplikasi JogjaRasa.
- Mengubah database makanan dan restoran.
- Menghapus review dan rating yang diberikan oleh user.

## Sumber *Dataset*
*Dataset* yang kami gunakan dapat diakses pada tautan [berikut ini](https://docs.google.com/spreadsheets/d/1HOWVDKvhHSFdiAnUizqDHZQ1DrOtZfIu1O4QrA-wlpY/edit?usp=sharing). Data ini dikumpulkan secara manual dengan mengambil lokasi, deskripsi, serta nama restoran yang menjual makanan sesuai dengan nama restorannya.
