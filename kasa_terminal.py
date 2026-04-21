#!/usr/bin/env python3
"""
Terminalde çalışan Kasa Rapor Sistemi
Python3 ile çalıştır: python3 kasa_terminal.py
"""

import os
from datetime import datetime

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    clear_screen()
    print("=" * 50)
    print("📊 TERMİNAL KASA RAPOR SİSTEMİ")
    print("=" * 50)
    print("16 Ekip • Devralma Raporu • Otomatik Hesaplama")
    print()

def get_input(prompt, default=""):
    response = input(f"{prompt} [{default}]: ").strip()
    return response if response else default

def format_currency(amount):
    return f"{amount:,} ₺".replace(",", ".")

def main():
    print_header()
    
    # Temel bilgiler
    tarih = get_input("📅 Rapor Tarihi (GG/AA/YYYY)", datetime.now().strftime("%d/%m/%Y"))
    saat = get_input("🕐 Saat (Devralma)", datetime.now().strftime("%H:%M"))
    hazirlayan = get_input("👤 Hazırlayan", "Kevin X2")
    vardiya = get_input("🌓 Vardiya (G/Ge)", "G")
    vardiya_text = "Gündüz (08:00-20:00)" if vardiya.upper() == "G" else "Gece (20:00-08:00)"
    
    # Ekip listesi
    ekipler = [
        'berlin', 'boca', 'datça', 'heaven', 'kale', 
        'lüksemburg', 'mater', 'mayk', 'paris', 'raptor', 
        'rio', 'suriçi', 'suriçiv2', 'tokyo', 'vadi', 'şırnak'
    ]
    
    print("\n" + "="*50)
    print("💰 EKİP KASA BİLGİLERİNİ GİRİN")
    print("="*50)
    
    rapor_satirlari = []
    toplamlar = {'net': 0, 'kullanilabilir': 0, 'bloke': 0}
    hatalar = []
    
    for ekip in ekipler:
        print(f"\n--- {ekip.upper()} ---")
        
        try:
            net = int(get_input(f"  Net Kasa (₺)", "0") or "0")
            kullanilabilir = int(get_input(f"  Kullanılabilir (₺)", "0") or "0")
            bloke = int(get_input(f"  Bloke (₺)", "0") or "0")
            aciklama = get_input(f"  Açıklama", "")
            
            # Kontrol
            if net != kullanilabilir + bloke:
                hatalar.append(f"{ekip}: Net ({net}) ≠ Kullanılabilir ({kullanilabilir}) + Bloke ({bloke})")
            
            # Toplamlara ekle
            toplamlar['net'] += net
            toplamlar['kullanilabilir'] += kullanilabilir
            toplamlar['bloke'] += bloke
            
            # Satırı kaydet
            satir = f"{ekip:<12} | {format_currency(net):>15} | {format_currency(kullanilabilir):>15} | {format_currency(bloke):>15} | {aciklama}"
            rapor_satirlari.append(satir)
            
        except ValueError:
            print(f"  ⚠️  Sayısal değer girin, 0 varsayılan")
            net = kullanilabilir = bloke = 0
            aciklama = "HATA - sayısal değer değil"
            satir = f"{ekip:<12} | {'0 ₺':>15} | {'0 ₺':>15} | {'0 ₺':>15} | {aciklama}"
            rapor_satirlari.append(satir)
    
    # Raporu göster
    print_header()
    print("✅ RAPOR HAZIR")
    print("="*50)
    print(f"Tarih: {tarih}")
    print(f"Saat: {saat} (Devralma)")
    print(f"Hazırlayan: {hazirlayan}")
    print(f"Vardiya: {vardiya_text}")
    print()
    
    print("Ekip         |      Net Kasa   | Kullanılabilir |      Bloke     | Açıklama")
    print("-" * 80)
    for satir in rapor_satirlari:
        print(satir)
    print("-" * 80)
    
    # Toplamlar
    print(f"{'TOPLAM':<12} | {format_currency(toplamlar['net']):>15} | {format_currency(toplamlar['kullanilabilir']):>15} | {format_currency(toplamlar['bloke']):>15}")
    print()
    
    # Oranlar
    if toplamlar['net'] > 0:
        kullanilabilir_orani = (toplamlar['kullanilabilir'] / toplamlar['net']) * 100
        bloke_orani = (toplamlar['bloke'] / toplamlar['net']) * 100
        
        print("📈 ÖZET ANALİZ:")
        print(f"  Kullanılabilir Oranı: %{kullanilabilir_orani:.1f}")
        print(f"  Bloke Oranı: %{bloke_orani:.1f}")
        
        if bloke_orani > 30:
            print("  ⚠️  LİKİDİTE RİSKİ: Bloke oranı >%30")
        elif bloke_orani > 20:
            print("  ⚠️  DİKKAT: Bloke oranı >%20")
        else:
            print("  ✅ Likidite NORMAL")
    
    # Hatalar
    if hatalar:
        print("\n⚠️  UYARILAR:")
        for hata in hatalar:
            print(f"  • {hata}")
    
    # Kaydetme seçeneği
    print("\n" + "="*50)
    kaydet = input("💾 Raporu kaydetmek istiyor musunuz? (E/h): ").strip().upper()
    
    if kaydet != "H":
        dosya_adi = f"kasa_raporu_{tarih.replace('/', '')}_{saat.replace(':', '')}.txt"
        
        with open(dosya_adi, 'w', encoding='utf-8') as f:
            f.write("KASA RAPORU\n")
            f.write("=" * 40 + "\n")
            f.write(f"Tarih: {tarih}\n")
            f.write(f"Saat (Devralma): {saat}\n")
            f.write(f"Hazırlayan: {hazirlayan}\n")
            f.write(f"Vardiya: {vardiya_text}\n")
            f.write("\n")
            f.write("Ekip | Net Kasa (₺) | Kullanılabilir (₺) | Bloke (₺) | Açıklama\n")
            f.write("-" * 80 + "\n")
            
            for satir in rapor_satirlari:
                # Formatı düzelt
                parts = satir.split("|")
                ekip = parts[0].strip()
                net = parts[1].strip()
                kullanilabilir = parts[2].strip()
                bloke = parts[3].strip()
                aciklama = parts[4].strip() if len(parts) > 4 else ""
                f.write(f"{ekip} | {net} | {kullanilabilir} | {bloke} | {aciklama}\n")
            
            f.write("-" * 80 + "\n")
            f.write(f"TOPLAM Net: {format_currency(toplamlar['net'])}\n")
            f.write(f"TOPLAM Kullanılabilir: {format_currency(toplamlar['kullanilabilir'])}\n")
            f.write(f"TOPLAM Bloke: {format_currency(toplamlar['bloke'])}\n")
            
            if toplamlar['net'] > 0:
                f.write(f"Kullanılabilir Oranı: %{kullanilabilir_orani:.1f}\n")
                f.write(f"Bloke Oranı: %{bloke_orani:.1f}\n")
            
            f.write(f"\nOluşturulma: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        
        print(f"\n✅ Rapor kaydedildi: {dosya_adi}")
        print(f"   Bulunduğu dizin: {os.path.abspath(dosya_adi)}")
    
    print("\n" + "="*50)
    print("👋 Program sonlandı. İyi çalışmalar!")
    print("="*50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ İptal edildi.")
    except Exception as e:
        print(f"\n\n⚠️  Hata: {e}")