# JogjaRasa 🍛

> Proyek ini dibuat dalam memenuhi tugas Proyek Tengah Semester (PTS) pada mata kuliah Pemrograman Berbasis Platform (CSGE602022).

## 👥 Anggota Kelompok (F02)

| Nama                       | NPM          | Github      |
| -------------------------- | ------------ | ----------- |
| Grace Karina               | 2306275834   | gracekarinn |
| Claudia Paskalia Koesno    | 2306275355   | ravenalaa   |
| Palastha Zhorif Kawiswara  | 2306245705   | astzkkk99   |
| Darren Aldrich             | 2306206856   | Dardrich    |
| Adam Caldipawell Sembiring | 232306227160 | AdamCS-code |

## 📜 Cerita Aplikasi

🌟 **Selamat datang di JogjaRasa!** 🌟

**_"Rasakan keberagaman kuliner, temukan cerita di setiap suapan!"_**

**JogjaRasa** adalah aplikasi yang didedikasikan untuk memperkenalkan kekayaan kuliner Daerah Istimewa Yogyakarta, sebuah kota yang kaya akan budaya dan dikenal sebagai pusat kuliner yang memikat. Nama "JogjaRasa" berasal dari kata "Yogyakarta," sebuah provinsi di Indonesia yang terletak di timur Pulau Jawa, dan kata "Rasa," yang berarti cita rasa. Dengan demikian, JogjaRasa mencerminkan cita rasa khas makanan Yogyakarta, menjadikannya pintu gerbang bagi siapa saja yang ingin menjelajahi kelezatan kuliner kota ini.

JogjaRasa mengintegrasikan kemudahan teknologi dengan eksplorasi cita rasa lokal. Aplikasi ini membantu pengguna menemukan rekomendasi tempat makan berdasarkan jenis makanan yang dicari serta lokasi yang strategis. Dari warung sederhana hingga restoran yang menyajikan hidangan tradisional, JogjaRasa menjadikan setiap perjalanan kuliner sebagai pengalaman yang mudah dan menyenangkan.

## 📅 Fitur Unggulan

### Reservasi Online

- **Pemesanan Praktis:** Melakukan reservasi tempat atau makanan secara online.
- **Tiket Digital:** Setiap reservasi diterbitkan dalam bentuk tiket digital yang dapat diperbarui sesuai kebutuhan.

### Forum Diskusi

- **Berbagi Cerita:** Pengguna dapat berbagi ulasan, cerita, dan rekomendasi tentang tempat makan yang telah dikunjungi.
- **Interaksi Komunitas:** Ruang berbagi pengalaman kuliner untuk memberikan wawasan baru.

### Penilaian dan Bookmark

- **Ulasan Langsung:** Pengguna dapat memberikan penilaian pada restoran dan menyimpan tempat makan favorit untuk kunjungan berikutnya.

## 🌟 Kenapa Memilih JogjaRasa?

JogjaRasa tidak hanya berfungsi sebagai panduan kuliner, tetapi juga menjadi penghubung antara wisatawan dan masyarakat lokal melalui kekayaan cita rasa yang ditawarkan kota ini.

## 🎉 Bergabunglah Bersama Kami!

Aplikasi JogjaRasa sekarang bisa dicoba secara langsung di [JogjaRasa](https://jogja-rasa-production.up.railway.app).

- 🔑 Jangan lupa untuk **login** atau **registrasi** jika belum memiliki akun.
- 🎯 Mulailah mencari tempat makan terbaik di Yogyakarta!

**Selamat menjelajah!** 🌍✨

---

## 📚 Daftar Modul

Berikut ini adalah daftar modul yang akan kami implementasikan beserta pengembang dari setiap modul.

| Modul                   | Penjelasan                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Pengembang |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | --- |
| **Product (Homepage)**  | Menampilkan berbagai restoran beserta daftar makanan yang ditawarkan. Fitur _search engine_ memungkinkan pengguna mencari berbagai jenis makanan dan restoran sesuai keinginan. Pencarian ini akan mengutamakan hasil yang paling relevan dan dekat dengan lokasi pengguna saat itu. Selain itu, sistem akan memberikan rekomendasi makanan yang disesuaikan dengan preferensi pengguna.                                                                                  | Grace      |
| **Bookmark**            | Pengguna dapat menyimpan restoran favorit mereka untuk akses cepat di lain waktu. Pengguna dapat menandai restoran yang mereka sukai, dan restoran tersebut akan tersimpan dalam daftar _bookmark_. Selain itu, pengguna juga dapat melihat, mengelola, atau mengunjungi kembali restoran-restoran yang sudah di-bookmark.                                                                                                                                                | Darren     |
| **Review**              | Pengguna dapat memberikan penilaian terhadap restoran yang sudah dikunjungi. Pengguna dapat memberikan _rating_ berupa bintang, menulis komentar, serta mengunggah foto makanan atau suasana restoran. Ulasan ini akan membantu pengguna lain dalam mendapatkan gambaran yang lebih jelas mengenai pengalaman di restoran tersebut.                                                                                                                                       | Adam       |
| **Reservasi**           | Melakukan pemesanan makanan di restoran secara online. Setiap reservasi diterbitkan dalam bentuk tiket digital. Tiket ini dapat diupdate sesuai dengan kebutuhan pengguna, seperti perubahan waktu atau jumlah pesanan. Selain itu, pengguna juga dapat melihat riwayat tiket reservasi yang telah dibuat sebelumnya.                                                                                                                                                     | Claudia    |
| **Rekomendasi (Forum)** | Modul Rekomendasi (Forum) memungkinkan pengguna untuk membuat diskusi seputar restoran atau makanan tertentu. Pengguna dapat memulai topik baru, dan pengguna lain dapat berpartisipasi dengan memberikan tanggapan atau komentar pada topik yang sudah ada. Forum ini bertujuan untuk memfasilitasi interaksi antar pengguna dalam berbagi rekomendasi dan pengalaman kuliner. Admin dapat menyoroti dan memoderasi diskusi tertentu yang dianggap relevan atau populer. | Astha      |

## 🕵️ _Role_ atau Peran Pengguna

### 1. 👨‍💻 User

#### 🔓 User yang Sudah Terautentikasi

- Mengakses informasi mengenai restoran dan makanan yang telah disesuaikan dengan preferensi pribadi.
- Menambah dan menghapus restoran pada daftar _bookmark_.
- Memberikan rating dan review untuk restoran yang dipilih.
- Membuat, mengupdate, dan melihat riwayat tiket reservasi.
- Membuat topik baru, memberikan tanggapan, dan berpartisipasi dalam diskusi forum.

#### 🔒 User yang Belum Terautentikasi

- Melihat restoran, makanan yang ditawarkan, dan menggunakan fitur pencarian restoran terdekat.
- Melihat review dan rating dari pengguna lain.
- Melihat diskusi yang sudah ada, tanpa memberikan tanggapan atau membuat topik baru.

## Sumber _Dataset_

_Dataset_ yang kami gunakan dapat diakses pada tautan [berikut ini](https://docs.google.com/spreadsheets/d/1EWzbPrJWy8ChZi6N0tm_GsCz2lU1QidzWzlQ8C3sphI/edit?usp=sharing). Data ini dikumpulkan secara manual dengan mengambil lokasi, deskripsi, serta nama restoran yang menjual makanan sesuai dengan nama restorannya.
