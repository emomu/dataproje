#!/usr/bin/env python3
"""
SERVER - Intermediate Node + Data Corruptor
Client 1'den veri alır, bozar ve Client 2'ye iletir.
"""

import socket
import random
import sys
import time

# ==================== HATA ENJEKSİYON FONKSİYONLARI ====================

def bit_flip(data, num_flips=1):
    """
    Rastgele bit(ler)i ters çevirir (1→0 veya 0→1).
    """
    data_bytes = bytearray(data.encode('utf-8'))
    
    for _ in range(num_flips):
        if len(data_bytes) == 0:
            break
        
        # Rastgele byte seç
        byte_idx = random.randint(0, len(data_bytes) - 1)
        # Rastgele bit seç (0-7)
        bit_idx = random.randint(0, 7)
        # Bit'i ters çevir
        data_bytes[byte_idx] ^= (1 << bit_idx)
    
    try:
        return data_bytes.decode('utf-8', errors='replace')
    except:
        return data_bytes.decode('utf-8', errors='ignore')

def character_substitution(data):
    """
    Rastgele bir karakteri başka bir karakterle değiştirir.
    """
    if len(data) == 0:
        return data
    
    idx = random.randint(0, len(data) - 1)
    # Rastgele yeni karakter (printable ASCII)
    new_char = chr(random.randint(65, 90))  # A-Z arası
    
    corrupted = data[:idx] + new_char + data[idx + 1:]
    return corrupted

def character_deletion(data):
    """
    Rastgele bir karakteri siler.
    """
    if len(data) <= 1:
        return data
    
    idx = random.randint(0, len(data) - 1)
    corrupted = data[:idx] + data[idx + 1:]
    return corrupted

def character_insertion(data):
    """
    Rastgele bir pozisyona rastgele karakter ekler.
    """
    if len(data) == 0:
        return data
    
    idx = random.randint(0, len(data))
    # Rastgele karakter (printable ASCII)
    new_char = chr(random.randint(97, 122))  # a-z arası
    
    corrupted = data[:idx] + new_char + data[idx:]
    return corrupted

def character_swap(data):
    """
    İki bitişik karakterin yerini değiştirir.
    """
    if len(data) < 2:
        return data
    
    idx = random.randint(0, len(data) - 2)
    data_list = list(data)
    data_list[idx], data_list[idx + 1] = data_list[idx + 1], data_list[idx]
    
    return ''.join(data_list)

def burst_error(data):
    """
    3-8 ardışık karakteri bozar (değiştirir).
    """
    if len(data) < 3:
        return character_substitution(data)
    
    burst_length = random.randint(3, min(8, len(data)))
    start_idx = random.randint(0, len(data) - burst_length)
    
    # Burst bölgesini rastgele karakterlerle değiştir
    corrupted = list(data)
    for i in range(start_idx, start_idx + burst_length):
        corrupted[i] = chr(random.randint(65, 90))
    
    return ''.join(corrupted)

def multiple_bit_flips(data):
    """
    Birden fazla rastgele bit'i ters çevirir.
    """
    num_flips = random.randint(2, 5)
    return bit_flip(data, num_flips)

# ==================== SERVER FONKSİYONLARI ====================

def corrupt_data(data, error_type=None):
    """
    Veriyi belirtilen veya rastgele hata tipiyle bozar.
    """
    error_methods = {
        '1': ('Bit Flip', lambda d: bit_flip(d, 1)),
        '2': ('Character Substitution', character_substitution),
        '3': ('Character Deletion', character_deletion),
        '4': ('Character Insertion', character_insertion),
        '5': ('Character Swap', character_swap),
        '6': ('Multiple Bit Flips', multiple_bit_flips),
        '7': ('Burst Error', burst_error),
    }
    
    if error_type is None:
        error_type = random.choice(list(error_methods.keys()))
    
    error_name, error_func = error_methods.get(error_type, ('Bit Flip', bit_flip))
    corrupted = error_func(data)
    
    return corrupted, error_name

def handle_client1(conn):
    """Client 1'den gelen veriyi alır."""
    try:
        data = conn.recv(4096).decode('utf-8')
        return data
    except Exception as e:
        print(f"✗ Client 1'den veri alınırken hata: {e}")
        return None

def send_to_client2(packet, client2_host, client2_port):
    """Bozulmuş paketi Client 2'ye gönderir."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((client2_host, client2_port))
        
        client_socket.send(packet.encode('utf-8'))
        client_socket.close()
        
        return True
    except ConnectionRefusedError:
        print(f"✗ Client 2'ye bağlanılamadı ({client2_host}:{client2_port})")
        print("  Lütfen önce Client 2'yi başlatın: python client2.py")
        return False
    except Exception as e:
        print(f"✗ Client 2'ye gönderilirken hata: {e}")
        return False

# ==================== ANA PROGRAM ====================

def main():
    SERVER_HOST = 'localhost'
    SERVER_PORT = 5555
    CLIENT2_HOST = 'localhost'
    CLIENT2_PORT = 6666
    
    print("=" * 60)
    print("SERVER - Intermediate Node + Data Corruptor")
    print("=" * 60)
    
    # Hata tipi seçimi
    print("\nHata Enjeksiyon Yöntemi:")
    print("1. Bit Flip (tek bit)")
    print("2. Character Substitution")
    print("3. Character Deletion")
    print("4. Character Insertion")
    print("5. Character Swap")
    print("6. Multiple Bit Flips")
    print("7. Burst Error")
    print("0. Rastgele seç (önerilen)")
    
    error_choice = input("\nSeçiminiz (0-7): ").strip()
    if error_choice not in ['0', '1', '2', '3', '4', '5', '6', '7']:
        error_choice = '0'
    
    # Socket oluştur
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(5)
        
        print(f"\n✓ Server başlatıldı: {SERVER_HOST}:{SERVER_PORT}")
        print("✓ Client 1'den gelen bağlantı bekleniyor...\n")
        
        while True:
            # Client 1'den bağlantı kabul et
            conn, addr = server_socket.accept()
            print("-" * 60)
            print(f"✓ Client 1 bağlandı: {addr}")
            
            # Veriyi al
            packet = handle_client1(conn)
            conn.close()
            
            if not packet:
                print("✗ Geçersiz paket alındı!")
                continue
            
            # Paketi ayrıştır
            try:
                parts = packet.split('|')
                if len(parts) != 3:
                    print("✗ Hatalı paket formatı!")
                    continue
                
                original_data, method, control_info = parts
                
                print(f"\nAlınan Paket:")
                print(f"  Veri            : {original_data}")
                print(f"  Yöntem          : {method}")
                print(f"  Kontrol Bilgisi : {control_info}")
                
            except Exception as e:
                print(f"✗ Paket ayrıştırılırken hata: {e}")
                continue
            
            # Veriyi boz
            error_type_to_use = None if error_choice == '0' else error_choice
            corrupted_data, error_name = corrupt_data(original_data, error_type_to_use)
            
            print(f"\nHata Enjeksiyonu:")
            print(f"  Yöntem          : {error_name}")
            print(f"  Orijinal        : {original_data}")
            print(f"  Bozulmuş        : {corrupted_data}")
            
            # Yeni paketi oluştur (bozulmuş veri + orijinal kontrol bilgisi)
            corrupted_packet = f"{corrupted_data}|{method}|{control_info}"
            
            print(f"\nClient 2'ye gönderiliyor...")
            
            # Client 2'ye gönder
            if send_to_client2(corrupted_packet, CLIENT2_HOST, CLIENT2_PORT):
                print(f"✓ Paket Client 2'ye iletildi!")
            else:
                print(f"✗ Paket Client 2'ye gönderilemedi!")
            
            print("-" * 60 + "\n")
            print("Yeni bağlantı bekleniyor...\n")
    
    except KeyboardInterrupt:
        print("\n\n✓ Server kapatılıyor...")
    except Exception as e:
        print(f"\n✗ Server hatası: {e}")
    finally:
        server_socket.close()
        print("✓ Server kapatıldı.")

if __name__ == "__main__":
    main()