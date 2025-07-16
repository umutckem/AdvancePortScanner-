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

<img width="1121" height="845" alt="image" src="https://github.com/user-attachments/assets/26f3c907-9347-43e0-ab6b-d0ffbb8a0acb" />

Bu Ekranda İp girişi yapılarak ya da örenğin 192.168.1.0/24 ve ya 192.168.1.1 tek bir ip girilerek program başlatılabiliyor.

<img width="1123" height="849" alt="image" src="https://github.com/user-attachments/assets/a9ccb962-b2ec-4b42-b0cf-c652590d4458" />

Bu ekranda ise belirli portların taranması ya da girilen port aralıklarına bakılması sağlanılıyor 0-1024 arası örneğin

#Örnek Ekran Çıktısı

<img width="621" height="666" alt="image" src="https://github.com/user-attachments/assets/6d44796e-cdfd-42e1-b9f7-4a1cab6b5158" />

Burda ise bütün portlara ping atarak hangi portların açık ya da kapalı olduğuna ya da banner'ları var mı onları kontrolünü sağlıyor.

<img width="804" height="705" alt="image" src="https://github.com/user-attachments/assets/e39bbe85-811f-4dd8-93e7-cea54e267224" />

threads yapısı sayesinde çok hızlı işlem yapıyor ve bu threads yapılarını düzenli bir şekilde ekrana verilmesini sağlıyor



