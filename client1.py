#!/usr/bin/env python3
"""
CLIENT 1 - Data Sender
Kullanıcıdan metin alır, kontrol bilgisi üretir ve server'a gönderir.
"""

import socket
import sys

# ==================== KONTROL BİLGİSİ HESAPLAMA FONKSİYONLARI ====================

def calculate_even_parity(data):
    """
    Even Parity hesaplar.
    Her karakter için ASCII değerindeki 1'lerin sayısı çift olmalı.
    """
    parity_bits = []
    for char in data:
        ascii_val = ord(char)
        # Bit sayısını hesapla
        ones_count = bin(ascii_val).count('1')
        # Çift parite için: eğer tek sayıda 1 varsa parite biti 1, yoksa 0
        parity_bit = '1' if ones_count % 2 == 1 else '0'
        parity_bits.append(parity_bit)
    
    return ''.join(parity_bits)

def calculate_crc16(data):
    """
    CRC-16 hesaplar (CRC-16-CCITT polinomu kullanarak).
    Polinom: x^16 + x^12 + x^5 + 1 (0x1021)
    """
    polynomial = 0x1021  # CRC-16-CCITT
    crc = 0xFFFF  # Başlangıç değeri
    
    for char in data:
        byte = ord(char)
        crc ^= (byte << 8)
        
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc = crc << 1
            crc &= 0xFFFF  # 16 bit'te tut
    
    return format(crc, '04X')  # 4 haneli hex olarak döndür

def calculate_internet_checksum(data):
    """
    Internet Checksum (IP Checksum) hesaplar.
    16-bit kelimeler toplamının 1'e tümleyeni.
    """
    # Veriyi bytes'a çevir
    data_bytes = data.encode('utf-8')
    
    # Tek sayıda byte varsa sonuna 0 ekle
    if len(data_bytes) % 2 == 1:
        data_bytes += b'\x00'
    
    # 16-bit kelimelere böl ve topla
    total = 0
    for i in range(0, len(data_bytes), 2):
        word = (data_bytes[i] << 8) + data_bytes[i + 1]
        total += word
        # Taşmayı (carry) ekle
        total = (total & 0xFFFF) + (total >> 16)
    
    # 1'e tümleyen (complement)
    checksum = ~total & 0xFFFF
    
    return format(checksum, '04X')

def calculate_2d_parity(data):
    """
    2D Parity hesaplar.
    Veriyi 8x8 matrise yerleştirir, satır ve sütun pariteleri hesaplar.
    """
    # Veriyi 8 karakterlik bloklara böl
    block_size = 8
    blocks = []
    
    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        # Eksik blokları boşlukla doldur
        if len(block) < block_size:
            block += ' ' * (block_size - len(block))
        blocks.append(block)
    
    # Eksik satırları boşluklarla doldur
    while len(blocks) < block_size:
        blocks.append(' ' * block_size)
    
    # Matris oluştur (her karakter için 8-bit)
    matrix = []
    for block in blocks:
        row_bits = []
        for char in block:
            bits = format(ord(char), '08b')
            row_bits.append(bits)
        matrix.append(row_bits)
    
    # Satır pariteleri
    row_parities = []
    for row in matrix:
        row_str = ''.join(row)
        ones = row_str.count('1')
        row_parities.append('1' if ones % 2 == 1 else '0')
    
    # Sütun pariteleri (her bit pozisyonu için)
    col_parities = []
    for col_idx in range(block_size):
        for bit_idx in range(8):
            ones = 0
            for row_idx in range(len(matrix)):
                if matrix[row_idx][col_idx][bit_idx] == '1':
                    ones += 1
            col_parities.append('1' if ones % 2 == 1 else '0')
    
    # Hex formatına çevir
    all_parities = ''.join(row_parities) + ''.join(col_parities)
    # 4'er bit grupla ve hex'e çevir
    hex_result = ''
    for i in range(0, len(all_parities), 4):
        nibble = all_parities[i:i+4]
        if len(nibble) < 4:
            nibble += '0' * (4 - len(nibble))
        hex_result += format(int(nibble, 2), 'X')
    
    return hex_result

# ==================== ANA PROGRAM ====================

def main():
    # Server bilgileri
    SERVER_HOST = 'localhost'
    SERVER_PORT = 5555
    
    print("=" * 60)
    print("CLIENT 1 - DATA SENDER")
    print("=" * 60)
    
    # Kullanıcıdan metin al
    data = input("\nGöndermek istediğiniz metni girin: ").strip()
    
    if not data:
        print("Hata: Boş metin gönderilemez!")
        sys.exit(1)
    
    # Kontrol yöntemi seçimi
    print("\nKontrol Bilgisi Yöntemlerini Seçin:")
    print("1. Even Parity")
    print("2. CRC-16")
    print("3. Internet Checksum")
    print("4. 2D Parity")
    
    choice = input("\nSeçiminiz (1-4): ").strip()
    
    # Kontrol bilgisi hesapla
    if choice == '1':
        method = "PARITY"
        control_info = calculate_even_parity(data)
    elif choice == '2':
        method = "CRC16"
        control_info = calculate_crc16(data)
    elif choice == '3':
        method = "CHECKSUM"
        control_info = calculate_internet_checksum(data)
    elif choice == '4':
        method = "2D_PARITY"
        control_info = calculate_2d_parity(data)
    else:
        print("Geçersiz seçim! Varsayılan olarak CRC-16 kullanılıyor.")
        method = "CRC16"
        control_info = calculate_crc16(data)
    
    # Paketi oluştur
    packet = f"{data}|{method}|{control_info}"
    
    print("\n" + "-" * 60)
    print("Gönderilen Paket Bilgileri:")
    print(f"  Veri            : {data}")
    print(f"  Yöntem          : {method}")
    print(f"  Kontrol Bilgisi : {control_info}")
    print(f"  Paket           : {packet}")
    print("-" * 60)
    
    # Server'a bağlan ve gönder
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        
        print(f"\n✓ Server'a bağlanıldı: {SERVER_HOST}:{SERVER_PORT}")
        
        # Paketi gönder
        client_socket.send(packet.encode('utf-8'))
        print("✓ Paket gönderildi!")
        
        client_socket.close()
        print("\n✓ Bağlantı kapatıldı.")
        
    except ConnectionRefusedError:
        print(f"\n✗ Hata: Server'a bağlanılamadı ({SERVER_HOST}:{SERVER_PORT})")
        print("  Lütfen önce server'ı başlatın: python server.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Hata oluştu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()