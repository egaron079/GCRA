import zlib
import lzma

def compress(files, arc):
    with open(arc, "wb") as main:
        main.write(b"GCRA")
        main.close()
    for file in files:
        with open(file, "rb") as f:
            data = f.read()
            cData = lzma.compress(data)
            cFile = zlib.compress(bytes(file.split("/")[-1], "ascii"))
            f.close()
        with open(arc, "ab") as main:
            main.write(cFile)
            main.write(b"\xe7\x99\x0a\x06\xaa\xbb\xee\x05")
            main.write(cData)
            main.write(b"\x02\x09\xff\xf4\x89\x44\xee\x3f")
            main.close()

def decompress(arc):
    with open(arc, "rb") as main:
        data = main.read()[4:][:-8]
        chunks = data.split(b"\x02\x09\xff\xf4\x89\x44\xee\x3f")
        for chunk in chunks:
            fchunks = chunk.split(b"\xe7\x99\x0a\x06\xaa\xbb\xee\x05")
            filename = fchunks[0]
            cData = fchunks[1]
            with open(zlib.decompress(filename), "wb") as f:
                f.write(lzma.decompress(cData))
                f.close()
    main.close()