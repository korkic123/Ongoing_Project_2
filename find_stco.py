#-*- coding: utf-8 -*-

# Chunk Extractor v0.1
# Created by Korkic
# AVC only

try:
    f = open('C:\\Users\\korki\\Desktop\\F201308021823010.mp4','rb') # 파일 경로 
    byte = 1
    cluster = 0
    fs = (-1)

    # 파일 내 stco 위치 검색
    while fs == (-1):
        byte = f.read(4096)
        cluster += 1
        stco = b"\x73\x74\x63\x6f"
        fs = byte.find(stco)

    stco_addr = ((cluster - 1) * 4096) + fs

    # stco 내 정보(version, flags, entrycount) 출력
    c_stco = byte[fs:fs+4]
    c_version = byte[fs+4:fs+5]
    c_flags = byte[fs+5:fs+8]
    c_entrycount = byte[fs+8:fs+12]

    print("stco : " + c_stco.hex() + "(" + str(hex(stco_addr)) + ")")
    print("------------------------------------------")
    print("Version : "+ c_version.hex() + "(" + str(hex(stco_addr + 4)) + ")")
    print("Flags : " + c_flags.hex() + "(" + str(hex(stco_addr + 5)) + ")")
    print("Entry Count : " + c_entrycount.hex() + "(" + str(hex(stco_addr + 8)) + ")")

    # chunk 주소정보 출력
    init_chunk = fs + 12
    i_entrycount = int.from_bytes(c_entrycount, byteorder='big')
    chunk_addr = []
    for chunk in range(1, i_entrycount+1) :
        chunk_entry_value = byte[init_chunk + ((chunk - 1) * 4):init_chunk + (chunk * 4)]
        chunk_entry_addr = hex(((cluster - 1) * 4096) + init_chunk + ((chunk - 1) * 4))
        print("  chunk " + str(chunk) + " : " + str(chunk_entry_value.hex()) + " (" + str(chunk_entry_addr) + ")")

        # 각 chunk 주소를 리스트(chunk_addr)에 저장
        chunk_addr.append(chunk_entry_value)



    # 각 chunk를 나눠 파일로 추출
    for chunk in range(1, i_entrycount+1) :
        f2 = open("Chunk_" + str(chunk) + ".h264", 'wb')
        i_chunk_addr_start = int.from_bytes(chunk_addr[chunk-1], byteorder='big')
        f.seek(i_chunk_addr_start)

        if chunk == i_entrycount :
            part = f.read()
        else :
            i_chunk_addr_end = int.from_bytes(chunk_addr[chunk], byteorder='big')
            part = f.read(i_chunk_addr_end - i_chunk_addr_start)
        f2.write(part)

    f.close()

except IOError:
    print("IO error")
    print("파일이 없거나 잘못된 파일입니다.")
