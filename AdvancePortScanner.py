import socket
import ssl
import threading
import ipaddress
import platform
import subprocess
import queue
from colorama import init, Fore, Style
from getmac import get_mac_address
from mac_vendor_lookup import MacLookup
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)
print_kilidi = threading.Lock()
sonuc_kuyrugu = queue.Queue()

mac_bilgi = MacLookup()
mac_bilgi.load_vendors()

def ip_aktif_mi(ip):
    parametre = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        subprocess.check_output(["ping", parametre, "1", ip], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def hostname_al(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Bilinmiyor"
    
def mac_al(ip):
    try:
        if platform.system().lower() == "windows":
            cikti = subprocess.check_output(f"arp -a {ip}", shell=True).decode()
            for satir in cikti.splitlines():
                if ip in satir:
                    return satir.split()[1].replace("-", ":")
        else:
            cikti = subprocess.check_output(["arp", "-n", ip]).decode()
            for satir in cikti.splitlines():
                if ip in satir:
                    bolumler = satir.split()
                    if len(bolumler) >= 3:
                        return bolumler[2]
        return "Bilinmiyor"
    except:
        return "Bilinmiyor"

def uretici_al(mac):
    try:
        return mac_bilgi.lookup(mac)
    except:
        return "Bilinmiyor"

def servis_adi_al(port):
    try:
        return socket.getservbyport(port)
    except:
        return "BILINMEYEN"

def banner_al(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soket:
            soket.settimeout(1)
            soket.connect((ip, port))
            soket.send(b"HEAD / HTTP/1.1\r\nHost: %s\r\n\r\n" % ip.encode())
            veri = soket.recv(1024).decode(errors="ignore").strip().replace("\r", "").replace("\n", " ")
            return veri if veri else "Banner alinmadi"
    except:
        return "Banner alinmadi"

def ssl_bilgi_al(ip, port=443):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((ip, port), timeout=2) as soket:
            with context.wrap_socket(soket, server_hostname=ip) as ssock:
                sertifika = ssock.getpeercert()
                subject = dict(x[0] for x in sertifika.get("subject", []))
                issuer = dict(x[0] for x in sertifika.get("issuer", []))
                baslangic = sertifika.get("notBefore")
                bitis = sertifika.get("notAfter")
                return f"SSL: CN={subject.get('commonName', '-')}, Issuer={issuer.get('commonName', '-')}, Valid={baslangic} - {bitis}"
    except:
        return "SSL Bilgisi Alinamadi"

def port_tara(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soket:
            soket.settimeout(0.5)
            sonuc = soket.connect_ex((ip, port))
            servis = servis_adi_al(port).upper()
            banner = "-"
            ssl_bilgi = ""
            if sonuc == 0:
                banner = banner_al(ip, port)
                if port == 443:
                    ssl_bilgi = ssl_bilgi_al(ip, port)
                sonuc_kuyrugu.put((port, Fore.GREEN + f"{ip:<18} {port:<6} {servis:<12} ACIK    {banner} {ssl_bilgi}"))
            else:
                sonuc_kuyrugu.put((port, Fore.RED + f"{ip:<18} {port:<6} {servis:<12} KAPALI  {banner}"))
    except:
        sonuc_kuyrugu.put((port, Fore.YELLOW + f"{ip:<18} {port:<6} HATA"))

def ip_icin_port_tara(ip, portlar, aktif_mi):
    durum = "AKTIF" if aktif_mi else "PASIF"
    ad = hostname_al(ip)
    mac = mac_al(ip)
    uretici = uretici_al(mac) if mac != "Bilinmiyor" else "Bilinmiyor"

    print(Fore.CYAN + f"\n=== {ip} TARAMA SONUCU ===")
    print(Fore.YELLOW + f"Durum    : {durum}")
    print(Fore.YELLOW + f"Ad       : {ad}")
    print(Fore.YELLOW + f"IP       : {ip}")
    print(Fore.YELLOW + f"MAC      : {mac}")
    print(Fore.YELLOW + f"Uretici  : {uretici}\n")

    print(Fore.MAGENTA + f"{'IP':<18} {'PORT':<6} {'SERVIS':<12} DURUM   BANNER / SERTIFIKA")
    print(Fore.MAGENTA + "-" * 90)

    with ThreadPoolExecutor(max_workers=100) as havuz:
        futures = [havuz.submit(port_tara, ip, port) for port in portlar]
        for future in futures:
            future.result()

    sirali_sonuclar = sorted(list(sonuc_kuyrugu.queue), key=lambda x: x[0])
    for _, satir in sirali_sonuclar:
        print(satir)

    sonuc_kuyrugu.queue.clear()

def hedef_ipleri_al(hedef):
    try:
        if '/' in hedef:
            return [str(ip) for ip in ipaddress.IPv4Network(hedef, strict=False)]
        else:
            return [hedef]
    except ValueError as hata:
        print(Fore.RED + f"Hatalı IP/CIDR girdisi: {hata}")
        return []

def tum_ipleri_pingle(ip_listesi):
    ip_durumlari = {}

    def ping_gorevi(ip):
        ip_durumlari[ip] = ip_aktif_mi(ip)

    with ThreadPoolExecutor(max_workers=100) as havuz:
        havuz.map(ping_gorevi, ip_listesi)

    return ip_durumlari

def main():
    print(Fore.BLUE + Style.BRIGHT + "=== Python Nmap Stili Port Tarayıcı (Sertifika Destekli) ===\n")
    hedef = input("Hedef IP veya CIDR (örn: 192.168.1.1 ya da 192.168.1.0/24): ").strip()

    yaygin_mi = input("Yaygın portları mı taramak istiyorsun? (E/h): ").strip().lower()
    if yaygin_mi == "e":
        portlar = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389]
    else:
        try:
            baslangic = int(input("Başlangıç portu (0-65535): "))
            bitis = int(input("Bitiş portu (0-65535): "))
        except ValueError:
            print(Fore.RED + "Port numaraları sayı olmalıdır!")
            return

        if baslangic < 0 or bitis > 65535 or baslangic > bitis:
            print(Fore.RED + "Geçersiz port aralığı! 0-65535 arası ve başlangıç <= bitiş olmalı.")
            return

        portlar = list(range(baslangic, bitis + 1))

    hedef_ipler = hedef_ipleri_al(hedef)
    print(Fore.CYAN + "\n[*] Ping testi ile IP'ler kontrol ediliyor...")
    ip_durumlari = tum_ipleri_pingle(hedef_ipler)

    for ip in hedef_ipler:
        if ip_durumlari[ip]:
            ip_icin_port_tara(ip, portlar, True)
        else:
            print(Fore.LIGHTBLACK_EX + f"\n{ip} PASIF (Ping cevabı yok)")

if __name__ == "__main__":
    main()
