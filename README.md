# AdvancePortScanner

**AdvancePortScanner**, Python ile yazılmış gelişmiş ve çoklu iş parçacıklı (multi-threaded) bir port tarayıcıdır. Yerel veya uzak ağlarda açık portları tespit eder, servis bilgilerini ve banner’ları toplar, SSL sertifika detaylarını gösterir ve MAC adreslerinden üreticiyi tespit eder.

---

## Özellikler

- IP veya CIDR blokları için tarama
- Yaygın veya özel port aralıklarında tarama
- Çoklu iş parçacığı ile hızlı port tarama
- Servis adı ve banner bilgisi alma
- SSL sertifikası bilgilerini gösterme (CN, Issuer, geçerlilik)
- MAC adresi ve üretici bilgisi tespiti
- Renkli terminal çıktısı ile kolay okunabilirlik

---

## Kullanım

1. Python ortamınızı hazırlayın:
    ```bash
    pip install -r requirements.txt
    ```
    veya manuel:
    ```bash
    pip install colorama getmac mac-vendor-lookup
    ```

2. Programı çalıştırın:
    ```bash
    python AdvancePortScanner.py
    ```

3. Ekrandaki yönergeleri takip ederek hedef IP veya CIDR aralığını ve portları belirleyin.

---

## Gereksinimler

- Python 3.x
- colorama
- getmac
- mac-vendor-lookup

---

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakınız.

---

## İletişim

Herhangi bir soru veya öneri için:

- GitHub: [https://github.com/umutckem](https://github.com/umutckem)

---

**Teşekkürler!**

# Başlangıç Ekranı İp Girişi

<img width="1484" height="432" alt="Ekran görüntüsü 2025-07-11 222338" src="https://github.com/user-attachments/assets/d68ee77c-9006-4870-8b45-9bfc7e45d9cf" />

Bu Ekranda İp girişi yapılarak ya da örenğin 192.168.1.0/24 ve ya 192.168.1.1 tek bir ip girilerek program başlatılabiliyor.

<img width="1479" height="660" alt="Ekran görüntüsü 2025-07-11 222357" src="https://github.com/user-attachments/assets/a1dc9363-e061-42bb-ad7d-3759043abe8c" />

Bu ekranda ise belirli portların taranması ya da girilen port aralıklarına bakılması sağlanılıyor 0-1024 arası örneğin

#Örnek Ekran Çıktısı

<img width="1898" height="952" alt="Ekran görüntüsü 2025-07-11 222411" src="https://github.com/user-attachments/assets/a8cd8fe7-8bda-4668-bd73-190b4efb1f72" />

Burda ise bütün portlara ping atarak hangi portların açık ya da kapalı olduğuna ya da banner'ları var mı onları kontrolünü sağlıyor.

<img width="1820" height="957" alt="Ekran görüntüsü 2025-07-11 222420" src="https://github.com/user-attachments/assets/8fafe735-effe-4ab5-b209-bb0b2ac9f130" />

threads yapısı sayesinde çok hızlı işlem yapıyor ve bu threads yapılarını düzenli bir şekilde ekrana verilmesini sağlıyor



