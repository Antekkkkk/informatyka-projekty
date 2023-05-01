if True:
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


    class XYZ:
        a = 6378137
        e2 = 0.00669438002290

        def __init__(self, X, Y, Z):
            self.X = X
            self.Y = Y
            self.Z = Z

        def XYZ2flh(self):
            X = self.X
            Y = self.Y
            Z = self.Z
            f, l, h = gw.hirvonen(X, Y, Z, a, e2)
            self.fi = f
            self.la = l
            self.h = h
            return (self.fi, self.la, self.h)

        def XYZ2neu(self):
            dXYZ = [self.X, self.Y, self.Z]
            f, l, h = gw.hirvonen(self.X, self.Y, self.Z, a, e2)
            self.neu = gw.XYZ2neu(dXYZ, f, l)
            return (self.neu)


    class flh:
        def __init__(self, f, l, h):
            self.f = f
            self.l = l
            self.h = h  # definiuję zmienne dla klasy

        def flh2XYZ(self):
            f = self.f
            l = self.l
            h = self.h
            self.X, self.Y, self.Z = gw.flh2XYZ(f, l, h, a, e2)
            return (self.X, self.Y, self.Z)


    class u2000:
        def __init__(self, f, l, h, elip, typ):
            self.f = f
            self.l = l
            self.h = h
            self.elip = elip
            self.typ = typ

        def trans(self):
            if '0' in elip:
                print('wgs 80')
                self.a = 1
                self.e2 = 2
                self.lam0, self.n = gw.strefy2000(self.l)
                self.xgk, self.ygk = gw.fl2xygk(self.f, self.l, self.lam0, self.a, self.e2)
                self.x, self.y = gw.xy2000(self.xgk, self.ygk, self.n)
                return (self.x, self.y)

            elif '4' in elip:
                print('grs 84')
                self.a = 6378137.000
                self.e2 = 0.00669438
                self.lam0, self.n = gw.strefy2000(self.l)
                self.xgk, self.ygk = gw.fl2xygk(self.f, self.l, self.lam0, self.a, self.e2)
                self.x, self.y = gw.xy2000(self.xgk, self.ygk, self.n)
                return (self.x, self.y)

            elif 'r' in elip and 'a' in elip and 's' in elip:
                print('krasowski')
                self.a = 6378245.000
                self.e2 = 0.00669342
                self.lam0, self.n = gw.strefy2000(self.l)
                self.xgk, self.ygk = gw.fl2xygk(self.f, self.l, self.lam0, self.a, self.e2)
                self.x, self.y = gw.xy2000(self.xgk, self.ygk, self.n)
                return (self.x, self.y)


    class u1992:
        def __init__(self, f, l, h, elip, typ):
            self.f = f
            self.l = l
            self.h = h
            self.elip = elip
            self.typ = typ

        def trans(self):
            if '0' in elip:
                print('wgs 80')
                self.a = 1
                self.e2 = 2
                self.lam0 = gw.dms2rad(19, 0, 0)
                self.xgk, self.ygk = gw.fl2xygk(self.f, self.l, self.lam0, self.a, self.e2)
                self.x, self.y = gw.xy1992(self.xgk, self.ygk)

            elif '4' in elip:
                print('grs 84')
                self.a = 6378137.000
                self.e2 = 0.00669438
                self.lam0 = gw.dms2rad(19, 0, 0)
                self.xgk, self.ygk = gw.fl2xygk(self.f, self.l, self.lam0, self.a, self.e2)
                self.x, self.y = gw.xy1992(self.xgk, self.ygk)

            elif 'r' in elip and 'a' in elip and 's' in elip:
                print('krasowski')
                self.a = 6378245.000
                self.e2 = 0.00669342
                self.lam0 = gw.dms2rad(19, 0, 0)
                self.xgk, self.ygk = gw.fl2xygk(self.f, self.l, self.lam0, self.a, self.e2)
                self.x, self.y = gw.xy1992(self.xgk, self.ygk)