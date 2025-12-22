
import socket




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


def verify_data(data, method, received_control):
    """
    Alınan veri için kontrol bilgisini yeniden hesaplar ve karşılaştırır.
    """
    # Yönteme göre kontrol bilgisini hesapla
    if method == "PARITY":
        computed_control = calculate_even_parity(data)
    elif method == "CRC16":
        computed_control = calculate_crc16(data)
    elif method == "CHECKSUM":
        computed_control = calculate_internet_checksum(data)
    elif method == "2D_PARITY":
        computed_control = calculate_2d_parity(data)
    else:
        return None, "UNKNOWN METHOD"
    
    # Karşılaştır
    is_correct = (computed_control == received_control)
    status = "DATA CORRECT ✓" if is_correct else "DATA CORRUPTED ✗"
    
    return computed_control, status



def main():
    CLIENT2_HOST = 'localhost'
    CLIENT2_PORT = 6666
    
    print("=" * 60)
    print("CLIENT 2 - RECEIVER + ERROR CHECKER")
    print("=" * 60)
    
    # Socket oluştur
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((CLIENT2_HOST, CLIENT2_PORT))
        server_socket.listen(5)
        
        print(f"\n✓ Client 2 başlatıldı: {CLIENT2_HOST}:{CLIENT2_PORT}")
        print("✓ Server'dan gelen veri bekleniyor...\n")
        
        while True:
            # Server'dan bağlantı kabul et
            conn, addr = server_socket.accept()
            
            try:
                # Veriyi al
                packet = conn.recv(4096).decode('utf-8')
                conn.close()
                
                if not packet:
                    print("✗ Boş paket alındı!")
                    continue
                
                # Paketi ayrıştır
                parts = packet.split('|')
                if len(parts) != 3:
                    print("✗ Hatalı paket formatı!")
                    continue
                
                received_data, method, received_control = parts
                
                # Kontrol bilgisini yeniden hesapla
                computed_control, status = verify_data(received_data, method, received_control)
                
                # Sonuçları yazdır
                print("=" * 60)
                print("PAKET ALINDI VE KONTROL EDİLDİ")
                print("=" * 60)
                print(f"Received Data        : {received_data}")
                print(f"Method               : {method}")
                print(f"Sent Check Bits      : {received_control}")
                print(f"Computed Check Bits  : {computed_control}")
                print(f"Status               : {status}")
                print("=" * 60)
                print()
                
                # Detaylı analiz
                if status == "DATA CORRUPTED ✗":
                    print("⚠ UYARI: Veri iletim sırasında bozulmuş!")
                    print("  Gönderilen ve hesaplanan kontrol bitleri eşleşmiyor.")
                    
                    # Farklılıkları göster (eğer aynı uzunluktaysa)
                    if len(received_control) == len(computed_control):
                        diff_count = sum(1 for i in range(len(received_control)) 
                                       if received_control[i] != computed_control[i])
                        print(f"  Farklı bit/karakter sayısı: {diff_count}/{len(received_control)}")
                else:
                    print("✓ Veri başarıyla doğrulandı!")
                    print("  Gönderilen ve hesaplanan kontrol bitleri eşleşiyor.")
                
                print("\nYeni paket bekleniyor...\n")
                
            except Exception as e:
                print(f"✗ Paket işlenirken hata: {e}\n")
                continue
    
    except KeyboardInterrupt:
        print("\n\n✓ Client 2 kapatılıyor...")
    except Exception as e:
        print(f"\n✗ Client 2 hatası: {e}")
    finally:
        server_socket.close()
        print("✓ Client 2 kapatıldı.")

if __name__ == "__main__":
    main()