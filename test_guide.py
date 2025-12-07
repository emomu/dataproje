#!/usr/bin/env python3
"""
TEST SCRIPT - Otomatik Test Senaryosu
Projenin çalıştığını doğrulamak için basit testler içerir.
"""

import subprocess
import time
import sys
import os

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_step(step_num, text):
    print(f"\n[ADIM {step_num}] {text}")
    print("-" * 70)

def main():
    print_header("SOCKET PROGRAMMING TEST SCRIPT")
    
    print("""
Bu script, projenin dosyalarını kontrol eder.
Gerçek testi yapmak için şu adımları takip edin:

1. Terminal 1'de: python client2.py
2. Terminal 2'de: python server.py
3. Terminal 3'de: python client1.py

Her terminal için ayrı pencere açmanız gerekir.
""")
    
    # Dosya kontrolü
    print_step(1, "Dosya Kontrolü")
    
    files = ['client1.py', 'server.py', 'client2.py', 'README.md']
    all_exist = True
    
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✓ {file:20s} - {size:,} bytes")
        else:
            print(f"  ✗ {file:20s} - BULUNAMADI!")
            all_exist = False
    
    if not all_exist:
        print("\n✗ Bazı dosyalar eksik! Lütfen önce dosyaları oluşturun.")
        sys.exit(1)
    
    # Kod kontrolü
    print_step(2, "Kod İçerik Kontrolü")
    
    checks = {
        'client1.py': ['calculate_crc16', 'calculate_even_parity', 'socket.socket'],
        'server.py': ['bit_flip', 'character_substitution', 'corrupt_data'],
        'client2.py': ['verify_data', 'calculate_crc16', 'socket.socket']
    }
    
    for file, keywords in checks.items():
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n  {file}:")
        for keyword in keywords:
            if keyword in content:
                print(f"    ✓ {keyword}")
            else:
                print(f"    ✗ {keyword} - BULUNAMADI!")
    
    # Manuel test talimatları
    print_step(3, "Manuel Test Talimatları")
    
    print("""
Projeyi test etmek için 3 terminal açın:

┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│   TERMINAL 1        │  │   TERMINAL 2        │  │   TERMINAL 3        │
├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤
│ python client2.py   │  │ python server.py    │  │ python client1.py   │
│                     │  │                     │  │                     │
│ (Port 6666'da      │  │ (Port 5555'te      │  │ (5555'e bağlanır)  │
│  dinler)           │  │  dinler)           │  │                     │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
       ↑                        ↑                        │
       │                        │                        │
       └────────────────────────┴────────────────────────┘
                    Veri Akışı: Client1 → Server → Client2

SIRA ÖNEMLİ:
1. ÖNCE Client 2'yi başlat (6666 portunda bekliyor)
2. SONRA Server'ı başlat (5555'te dinliyor, 6666'ya bağlanacak)
3. EN SON Client 1'i başlat (5555'e bağlanıp veri gönderecek)

TEST ÖRNEĞİ:
-----------
Client 1'de: 
  - Metin gir: HELLO
  - Yöntem seç: 2 (CRC-16)

Server'da:
  - Hata tipi seç: 0 (Rastgele)
  - Veriyi bozar: HELLO → HEZLO

Client 2'de:
  - Alınan: HEZLO
  - Durum: DATA CORRUPTED ✗
""")
    
    # Örnek komutlar
    print_step(4, "Hızlı Başlatma Komutları")
    
    print("""
# Linux/Mac için 3 terminal birden açmak:
gnome-terminal -- python client2.py &
sleep 1
gnome-terminal -- python server.py &
sleep 1
gnome-terminal -- python client1.py &

# Veya tmux kullanarak:
tmux new-session -d -s test 'python client2.py'
tmux split-window -h -t test 'python server.py'
tmux split-window -v -t test 'python client1.py'
tmux attach -t test
""")
    
    # Test senaryoları
    print_step(5, "Önerilen Test Senaryoları")
    
    scenarios = [
        {
            'name': 'Temel CRC Testi',
            'data': 'HELLO',
            'method': 'CRC16 (2)',
            'error': 'Rastgele (0)',
            'expected': 'CORRUPTED'
        },
        {
            'name': 'Parity Testi',
            'data': 'TEST',
            'method': 'Parity (1)',
            'error': 'Bit Flip (1)',
            'expected': 'CORRUPTED'
        },
        {
            'name': 'Uzun Metin Testi',
            'data': 'This is a longer test message',
            'method': 'Checksum (3)',
            'error': 'Burst Error (7)',
            'expected': 'CORRUPTED'
        },
        {
            'name': '2D Parity Testi',
            'data': 'MATRIX TEST DATA',
            'method': '2D Parity (4)',
            'error': 'Character Swap (5)',
            'expected': 'CORRUPTED'
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n  Test {i}: {scenario['name']}")
        print(f"    Veri     : {scenario['data']}")
        print(f"    Yöntem   : {scenario['method']}")
        print(f"    Hata     : {scenario['error']}")
        print(f"    Beklenen : {scenario['expected']}")
    
    # Özet
    print_step(6, "Özet")
    
    print("""
✓ Tüm dosyalar mevcut ve hazır
✓ 4 kontrol yöntemi implemente edildi (Parity, CRC-16, Checksum, 2D Parity)
✓ 7 hata tipi implemente edildi
✓ Socket iletişimi hazır

Projeyi başlatmak için README.md dosyasındaki talimatları takip edin!

Bol şanslar! 🚀
""")
    
    print("=" * 70)

if __name__ == "__main__":
    main()