if __name__ == '__main__' :
    import numpy as np
    a = 6378137
    e2 = 0.00669438002290
    import gw as gw

    import argparse
    parser = argparse.ArgumentParser(description='Przeliczanie danych')
    parser.add_argument('path', type = str, help='Ścieżka pliku')               #tworze zmienną args.path która będzie zawierała nazwę pliku do odczytu
    args = parser.parse_args()
    print(args.path)
    #path = '''C:\Users\antek\Desktop\xyz.txt'''
    with open(args.path, 'r') as plik:
        print('plik odczytany prawidłowo')
        linie = plik.readlines()
        Xd = []
        Yd = []
        Zd = []                                          #tworzę puste biblioteki na dane z pliku
        fd = []
        ld = []
        hd = []
        typ = str(linie[0].split())
        elip = list(str(linie[1]))
        dane = linie[2:]                                #z pierwszych linijek odczytuję rodzaj danych i typ elipsoidy
        typ = list(typ)
        if 'X' in typ:
            for linia in dane:
                linia = linia.split()
                Xd.append(float(linia[0]))
                Yd.append(float(linia[1]))               # puste listy zapełniam danymi
                Zd.append(float(linia[2]))
        elif 'f' in typ:
            for linia in dane:
                linia = linia.split()
                fd.append(float(linia[0])*np.pi/180)
                ld.append(float(linia[1])*np.pi/180)        # jeśli rodzaj danych to flh, inne dane są podawane
                hd.append(float(linia[2])*np.pi/180)


    if 'X' in typ:                                           # odpalany gdy typ danych to xyz
        class XYZ:
            a = 6378137
            e2 = 0.00669438002290

            def __init__(self, X, Y, Z):
                self.X = X
                self.Y = Y                                     # wprowadzam dane do klasy
                self.Z = Z

            def XYZ2flh(self):
                X = self.X
                Y = self.Y
                Z = self.Z
                f,l,h = gw.hirvonen(X,Y,Z,a,e2)                 # funkcja przeliczająca xyz na flh
                self.fi = f
                self.la = l
                self.h = h
                return(self.fi,self.la,self.h)

            def XYZ2neu(self):
                dXYZ = [self.X,self.Y,self.Z]
                f, l, h = gw.hirvonen(self.X,self.Y,self.Z,a,e2)
                self.neu = gw.XYZ2neu(dXYZ,f,l)                     # funkcja przeliczająca xyz na neu
                return(self.neu)

    elif 'f' in typ or 'B' in typ or 'F' in typ:
        #print('flh uruchomione')
        class flh:
            def __init__(self, f, l, h):
                self.f = f
                self.l = l
                self.h = h                                           #definiuję zmienne dla klasy

            def flh2XYZ(self):
                f = self.f
                l = self.l
                h = self.h                                          # funkcja przeliczająca flh na xyz
                self.X,self.Y,self.Z = gw.flh2XYZ(f,l,h,a,e2)
                return(self.X,self.Y,self.Z)

        class u2000:
            def __init__(self,f,l,h,elip,typ):
                self.f = f
                self.l = l
                self.h = h                                          #nowa klasa dla układu 2000
                self.elip = elip
                self.typ = typ

            def trans(self):
                if '0' in elip and '8' in elip:
                    #print('wgs 80')
                    self.a = 1
                    self.e2 = 2
                    self.lam0, self.n = gw.strefy2000(self.l)                                              #funkcja przeliczająca dane z wybranej elipsoidy na ukłąd 2000
                    self.xgk, self.ygk = gw.fl2xygk(self.f, self.l, self.lam0, self.a, self.e2)
                    self.x, self.y = gw.xy2000(self.xgk, self.ygk, self.n)
                    return(self.x, self.y)

                elif '4' in elip and '8' in elip:
                    #print('grs 84')
                    self.a = 6378137.000
                    self.e2 = 0.00669438
                    self.lam0, self.n = gw.strefy2000(self.l)
                    self.xgk, self.ygk = gw.fl2xygk(self.f, self.l, self.lam0, self.a, self.e2)
                    self.x, self.y = gw.xy2000(self.xgk, self.ygk, self.n)
                    return (self.x, self.y)

                elif 'r' in elip and 'a' in elip and 's' in elip:
                    #print('krasowski')
                    self.a = 6378245.000
                    self.e2 = 0.00669342
                    self.lam0, self.n = gw.strefy2000(self.l)
                    self.xgk, self.ygk = gw.fl2xygk(self.f, self.l, self.lam0, self.a, self.e2)
                    self.x, self.y = gw.xy2000(self.xgk, self.ygk, self.n)
                    return (self.x, self.y)
                else:
                    print('Podana elispsoida nie jest obsługiwana, albo zrobiłeś literówkę. Sprawdź wprowadzony plik i spróbuj ponownie.')
                    raise SystemExit


        class u1992:
            def __init__(self, f, l, h, elip, typ):
                self.f = f
                self.l = l
                self.h = h
                self.elip = elip
                self.typ = typ

            def trans(self):
                if '0' in elip and '8' in elip:
                    #print('wgs 80')
                    self.a = 1
                    self.e2 = 2                                                     #funkcja przeliczająca dane z wybranej elipsoidy na ukłąd 1992
                    self.lam0 = gw.dms2rad(19,0,0)
                    self.xgk, self.ygk = gw.fl2xygk(self.f, self.l, self.lam0, self.a, self.e2)
                    self.x, self.y = gw.xy1992(self.xgk, self.ygk)
                    return (self.x, self.y)

                elif '4' in elip and '8' in elip:
                    #print('grs 84')
                    self.a = 6378137.000
                    self.e2 = 0.00669438
                    self.lam0 = gw.dms2rad(19, 0, 0)
                    self.xgk, self.ygk = gw.fl2xygk(self.f, self.l, self.lam0, self.a, self.e2)
                    self.x, self.y = gw.xy1992(self.xgk, self.ygk)
                    return (self.x, self.y)

                elif 'r' in elip and 'a' in elip and 's' in elip:
                    #print('krasowski')
                    self.a = 6378245.000
                    self.e2 = 0.00669342
                    self.lam0 = gw.dms2rad(19, 0, 0)
                    self.xgk, self.ygk = gw.fl2xygk(self.f, self.l, self.lam0, self.a, self.e2)
                    self.x, self.y = gw.xy1992(self.xgk, self.ygk)
                    return (self.x, self.y)
                else:
                    print('Podana elispsoida nie jest obsługiwana, albo zrobiłeś literówkę. Sprawdź wprowadzony plik i spróbuj ponownie.')
                    raise SystemExit
    gotflh = []
    gotneu = []
    if 'X' in typ:
        #print('XYZ wywołanie odpalone')
        for i in range(0,len(Xd)):
            wsp = XYZ(Xd[i], Yd[i], Zd[i])
            f,l,h = wsp.XYZ2flh()
            neu = wsp.XYZ2neu()
            wynikflh = [f,l,h]
            gotflh.append(wynikflh)                             #gotowe wyniki wrzucam do listy, która posłuży mi przy tworzeniu pliku wyjściowego
            gotneu.append(neu)
    gotxyz = []
    gotxy2000 = []
    gotxy1992 = []
    if 'f' in typ or 'B' in typ or 'F' in typ:
        #print('flh wywołanie odpalone')
        #print(fd)
        for i in range(0,len(fd)):
            wsp = flh(fd[i], ld[i], hd[i])
            X,Y,Z = wsp.flh2XYZ()
            wsp2000 = u2000(fd[i], ld[i], hd[i], elip, typ)
            x2000, y2000 = wsp2000.trans()
            wsp1992 = u1992(fd[i], ld[i], hd[i], elip, typ)
            x1992, y1992 = wsp1992.trans()
            wynikxyz = [X,Y,Z]                                  #gotowe wyniki wrzucam do listy, która posłuży mi przy tworzeniu pliku wyjściowego
            wynikxy2000 = [x2000, y2000]
            wynikxy1992 = [x1992, y1992]
            gotxyz.append(wynikxyz)
            gotxy2000.append(wynikxy2000)
            gotxy1992.append(wynikxy1992)

    import os
    current_file_path = os.path.abspath(__file__)
    current_directory_path = os.path.dirname(current_file_path)     #wpisuje miejsce, w którym zapisany zostanie plik z wynikami. Jest to folder
    print(current_directory_path)                                   # w którym znajduje się plik z kodem

    with open(f"{current_directory_path}\otrzymane wyniki.txt", "w") as file:       #tworzę plik z wynikami
        if 'X' in typ:
            podanytyp = 'XYZ'
            obliczany = 'flh'
        else:
            podanytyp = 'flh'
            obliczany = 'XYZ'

        if '0' in elip:
            elipsoida = 'WGS 80'
        elif '4' in elip:
            elipsoida = 'GRS 84'
        elif 'r' in elip and 'a' in elip and 's' in elip:
            elipsoida = 'Krasowski'

        file.write(f"Podałeś dane w formacie {podanytyp}, dla elipsoidy {elipsoida}.\n")
        file.write(f"Dane przeliczone z {podanytyp} na {obliczany}:\n")
        if podanytyp == 'XYZ':
            for i in gotflh:
                file.write(f"X: {i[0]} Y: {i[1]} Z: {i[2]}\n")
            file.write(f"Dane przeliczone z {podanytyp} na układ neu:\n")
            for i in gotneu:
                file.write(f"n: {i[0]} e: {i[1]} u: {i[2]}\n")
        elif podanytyp == 'flh':
            for i in gotxyz:
                file.write(f"X: {i[0]} Y: {i[1]} Z: {i[2]}\n")
            #file.write(f"Dane przeliczone z {podanytyp} na układ {obliczany}:\n")
            #for i in gotneu:
            #    file.write(f"n: {i[0]} e: {i[1]} u: {i[2]}\n")
            file.write(f"Dane przeliczone z elipsoidy {elipsoida} na układ 2000:\n")
            for i in gotxy2000:
                file.write(f"X2000: {i[0]} Y2000: {i[1]}\n")
            file.write(f"Dane przeliczone z elipsoidy {elipsoida} na układ 1992:\n")
            for i in gotxy1992:
                file.write(f"X1992: {i[0]} Y1992: {i[1]}\n")