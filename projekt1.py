with open([(plik)], 'r') as plik:
    linie = plik.readlines()
    Xd = []
    Yd = []
    Zd = []
    fd = []
    ld = []
    hd = []
    typ = str(linie[0].split())
    # print(type(typ), 'typ typu')
    elip = list(str(linie[1]))
    print(elip, 'elip')
    dane = linie[2:]
    # print(typ, 'typ')
    typ = list(typ)
    if 'X' in typ:
        print('działa')
    if 'X' in typ:
        for linia in dane:
            linia = linia.split()
            Xd.append(float(linia[0]))
            Yd.append(float(linia[1]))
            Zd.append(float(linia[2]))
    elif 'f' in typ:
        for linia in dane:
            linia = linia.split()
            fd.append(float(linia[0]) * np.pi / 180)
            ld.append(float(linia[1]) * np.pi / 180)
            hd.append(float(linia[2]) * np.pi / 180)