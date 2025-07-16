import socket
import ssl
import threading
import ipaddress
import platform
import subprocess
import queue
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
from getmac import get_mac_address
from mac_vendor_lookup import MacLookup
from concurrent.futures import ThreadPoolExecutor

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
                if not sertifika:
                    return "SSL Bilgisi Alinamadi"
                subject = {k: v for x in sertifika.get("subject", []) for (k, v) in x}
                issuer = {k: v for x in sertifika.get("issuer", []) for (k, v) in x}
                baslangic = sertifika.get("notBefore")
                bitis = sertifika.get("notAfter")
                return f"SSL: CN={subject.get('commonName', '-')}, Issuer={issuer.get('commonName', '-')}, Valid={baslangic} - {bitis}"
    except Exception:
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
                sonuc_kuyrugu.put((port, f"{ip:<18} {port:<6} {servis:<12} ACIK    {banner} {ssl_bilgi}"))
            else:
                sonuc_kuyrugu.put((port, f"{ip:<18} {port:<6} {servis:<12} KAPALI  {banner}"))
    except:
        sonuc_kuyrugu.put((port, f"{ip:<18} {port:<6} HATA"))

def ip_icin_port_tara_gui(ip, portlar, aktif_mi):
    ad = hostname_al(ip)
    mac = mac_al(ip)
    uretici = uretici_al(mac) if mac != "Bilinmiyor" else "Bilinmiyor"
    sonuc_alani.insert(tk.END, f"\n=== {ip} TARAMA SONUCU ===\n")
    sonuc_alani.insert(tk.END, f"Durum    : {'AKTIF' if aktif_mi else 'PASIF'}\n")
    sonuc_alani.insert(tk.END, f"Ad       : {ad}\n")
    sonuc_alani.insert(tk.END, f"IP       : {ip}\n")
    sonuc_alani.insert(tk.END, f"MAC      : {mac}\n")
    sonuc_alani.insert(tk.END, f"Uretici  : {uretici}\n\n")
    sonuc_alani.insert(tk.END, f"{'IP':<18} {'PORT':<6} {'SERVIS':<12} DURUM   BANNER / SERTIFIKA\n")
    sonuc_alani.insert(tk.END, "-" * 90 + "\n")
    with ThreadPoolExecutor(max_workers=100) as havuz:
        futures = [havuz.submit(port_tara, ip, port) for port in portlar]
        for future in futures:
            future.result()
    sirali_sonuclar = sorted(list(sonuc_kuyrugu.queue), key=lambda x: x[0])
    for _, satir in sirali_sonuclar:
        sonuc_alani.insert(tk.END, satir + "\n")
    sonuc_kuyrugu.queue.clear()

def hedef_ipleri_al(hedef):
    try:
        if '/' in hedef:
            return [str(ip) for ip in ipaddress.IPv4Network(hedef, strict=False)]
        else:
            return [hedef]
    except ValueError as hata:
        return []

def tum_ipleri_pingle(ip_listesi):
    ip_durumlari = {}
    def ping_gorevi(ip):
        ip_durumlari[ip] = ip_aktif_mi(ip)
    with ThreadPoolExecutor(max_workers=100) as havuz:
        havuz.map(ping_gorevi, ip_listesi)
    return ip_durumlari

# === GUI TANIMI ===
pencere = tk.Tk()
pencere.title("Python Port Tarayıcı (GUI)")
pencere.geometry("900x650")
pencere.configure(bg="#23272e")

style = ttk.Style()
try:
    style.theme_use("clam")
except:
    pass
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", background="#23272e", foreground="#f8f8f2", font=("Segoe UI", 10))
style.configure("TRadiobutton", background="#23272e", foreground="#f8f8f2", font=("Segoe UI", 10))

container = ttk.Frame(pencere)
container.pack(anchor="w", padx=10, pady=10, fill="x")

etiket1 = ttk.Label(container, text="Hedef IP veya CIDR:")
etiket1.pack(anchor="w")
giris_ip = ttk.Entry(container, width=50)
giris_ip.pack(anchor="w", pady=5)

secim_var = tk.StringVar(value="yaygin")
rb1 = ttk.Radiobutton(container, text="Yaygın Portlar", variable=secim_var, value="yaygin")
rb1.pack(anchor="w")
rb2 = ttk.Radiobutton(container, text="Belirli Aralık", variable=secim_var, value="aralik")
rb2.pack(anchor="w")

frame_port = ttk.Frame(container)
frame_port.pack(anchor="w", pady=5)
label_baslangic = ttk.Label(frame_port, text="Başlangıç Portu:")
label_baslangic.grid(row=0, column=0, sticky="w")
entry_baslangic = ttk.Entry(frame_port, width=10)
entry_baslangic.grid(row=0, column=1)
label_bitis = ttk.Label(frame_port, text="Bitiş Portu:")
label_bitis.grid(row=0, column=2, sticky="w")
entry_bitis = ttk.Entry(frame_port, width=10)
entry_bitis.grid(row=0, column=3)

def port_aralik_kutularini_guncelle(*args):
    if secim_var.get() == "aralik":
        entry_baslangic.config(state="normal")
        entry_bitis.config(state="normal")
    else:
        entry_baslangic.config(state="disabled")
        entry_bitis.config(state="disabled")

secim_var.trace_add("write", port_aralik_kutularini_guncelle)
port_aralik_kutularini_guncelle()

progress = ttk.Progressbar(container, orient="horizontal", length=400, mode="determinate")
progress.pack(anchor="w", pady=5)

btn_tara = ttk.Button(container, text="Taramayı Başlat")
btn_tara.pack(anchor="w", pady=10)

monospace_font = font.Font(family="Consolas", size=10)
sonuc_alani = scrolledtext.ScrolledText(pencere, width=110, height=30, bg="#181a20", fg="#f8f8f2", insertbackground="#f8f8f2", font=monospace_font)
sonuc_alani.pack(fill="both", expand=True, padx=10)

def taramayi_baslat():
    hedef = giris_ip.get().strip()
    secim = secim_var.get()
    sonuc_alani.delete(1.0, tk.END)
    if not hedef:
        messagebox.showerror("Hata", "Lütfen IP veya CIDR girin!")
        return
    if secim == "yaygin":
        portlar = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389]
    else:
        try:
            baslangic = int(entry_baslangic.get())
            bitis = int(entry_bitis.get())
            portlar = list(range(baslangic, bitis + 1))
        except:
            messagebox.showerror("Hata", "Geçerli port aralığı girin!")
            return
    def arka_plan():
        ip_listesi = hedef_ipleri_al(hedef)
        if not ip_listesi:
            messagebox.showerror("Hata", "Geçersiz IP/CIDR girdisi!")
            return
        ip_durumlari = tum_ipleri_pingle(ip_listesi)
        toplam_is = sum(1 for ip in ip_listesi if ip_durumlari[ip])
        progress["maximum"] = toplam_is
        ilerleme = 0
        for ip in ip_listesi:
            if ip_durumlari[ip]:
                ip_icin_port_tara_gui(ip, portlar, True)
            else:
                sonuc_alani.insert(tk.END, f"\n{ip} PASIF (Ping cevabı yok)\n")
            ilerleme += 1
            progress["value"] = ilerleme
            pencere.update_idletasks()
        progress["value"] = 0
    threading.Thread(target=arka_plan).start()

btn_tara.config(command=taramayi_baslat)

pencere.mainloop()