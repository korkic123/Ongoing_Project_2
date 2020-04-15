#-*- coding: utf-8 -*-

# Chunk Extractor v0.1
# Created by Korkic
# AVC only

try:
    file_path = 'C:\\Users\\korki\\Desktop\\test\\bb2.mp4'
    f = open(file_path,'rb')
    bytes = 1
    fs = (-1)

    # 파일 내 mdat 위치 검색
    while fs == (-1):
        bytes = f.read(4096)
        mdat = b"\x6d\x64\x61\x74"
        fs = bytes.find(mdat)

    # mdat 시작위치 저장(moov_addr)
    c_mdat = bytes[fs-4:fs]
    moov_addr = int.from_bytes(c_mdat, byteorder='big') + fs-4

    # mdat 시작위치(moov_addr)로 포인터 이동
    f.seek(moov_addr)
    fs = (-1)

    # vide 위치 검색
    while fs == (-1):
        if 4096<=len(bytes):
            bytes = f.read(4096)
        else :
            bytes = f.read()
        vide = b"\x76\x69\x64\x65"
        fs = bytes.find(vide)

    f.seek(moov_addr)
    fs = (-1)

    # 비디오 트랙의 stsc 위치 검색
    while fs == (-1):
        if 4096<=len(bytes):
            bytes = f.read(4096)
        else :
            bytes = f.read()
        stsc = b"\x73\x74\x73\x63"
        fs = bytes.find(stsc)

    stsc_addr = f.tell() - 4096 + fs

    # stsc 내 정보(version, flags, entrycount) 출력
    c_stsc = bytes[fs:fs+4]
    c_stsc_version = bytes[fs+4:fs+5]
    c_stsc_flags = bytes[fs+5:fs+8]
    c_stsc_entry_count = bytes[fs+8:fs+12]

#   C_entry = []
#   for :

    f.seek(moov_addr)
    fs = (-1)

    # 비디오 트랙의 stsz 위치 검색
    while fs == (-1):
        if 4096<=len(bytes):
            bytes = f.read(4096)
        else :
            bytes = f.read()
        stsz = b"\x73\x74\x73\x7a"
        fs = bytes.find(stsz)

    stsz_addr = f.tell() - 4096 + fs

    # stcz 내 정보(version, flags, entrycount) 출력
    c_stsz = bytes[fs:fs+4]
    c_stsz_version = bytes[fs+4:fs+5]
    c_stsz_flags = bytes[fs+5:fs+8]
    c_stsz_sample_size = bytes[fs+8:fs+12]

    f.seek(moov_addr)
    fs = (-1)

    # 비디오 트랙의 stco 위치 검색
    while fs == (-1):
        if 4096<=len(bytes):
            bytes = f.read(4096)
        else :
            bytes = f.read()
        stco = b"\x73\x74\x63\x6f"
        fs = bytes.find(stco)

    stco_addr = f.tell() - 4096 + fs

    # stco 내 정보(version, flags, entrycount) 출력
    c_stco = bytes[fs:fs+4]
    c_stco_version = bytes[fs+4:fs+5]
    c_stco_flags = bytes[fs+5:fs+8]
    c_stco_entry_count = bytes[fs+8:fs+12]

    print("stco : " + c_stco.hex() + "(" + str(hex(stco_addr)) + ")")
    print("------------------------------------------")
    print("Version : "+ c_version.hex() + "(" + str(hex(stco_addr + 4)) + ")")
    print("Flags : " + c_flags.hex() + "(" + str(hex(stco_addr + 5)) + ")")
    print("Entry Count : " + c_entry_count.hex() + "(" + str(hex(stco_addr + 8)) + ")")

    # chunk 주소정보 출력
    init_chunk = fs + 12
    i_entry_count = int.from_bytes(c_entry_count, byteorder='big')
    chunk_addr = []
    for chunk in range(1, i_entry_count+1) :
        chunk_entry_value = bytes[init_chunk + ((chunk - 1) * 4):init_chunk + (chunk * 4)]
        chunk_entry_addr = hex(f.tell() - 4096 + init_chunk + ((chunk - 1) * 4))
        print("  chunk " + str(chunk) + " : " + str(chunk_entry_value.hex()) + " (" + str(chunk_entry_addr) + ")")

        # 각 chunk 주소를 리스트(chunk_addr)에 저장
        chunk_addr.append(chunk_entry_value)

    # 각 chunk를 나눠 파일로 추출
    for chunk in range(1, i_entry_count+1) :
        f2 = open("Chunk_" + str(chunk) + ".h264", 'wb')
        i_chunk_addr_start = int.from_bytes(chunk_addr[chunk-1], byteorder='big')
        f.seek(i_chunk_addr_start)

        if chunk == i_entry_count :
            part = f.read()
        else :
            i_chunk_addr_end = int.from_bytes(chunk_addr[chunk], byteorder='big')
            part = f.read(i_chunk_addr_end - i_chunk_addr_start)
        f2.write(part)

    f.close()

except IOError:
    print("IO error")
    print("파일이 없거나 잘못된 파일입니다.")
