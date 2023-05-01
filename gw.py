# -*- coding: utf-8 -*-

import numpy as np
from math import *

def dms(x, txt):
    sig = ' '
    if x < 0:
        sig = '-'
        x = abs(x)
    x = x * 180 / pi
    d = int(x)
    m = int(60 * (x - d))
    s = (x - d - m / 60) * 3600
    print(txt, sig, '%3d' % d, '°', '%2d' % m, "'", '%7.5f' % s, '"')


# wspolrzedne geodezyjne -> wspolrzedne prostokatne
def flh2XYZ(f, l, h, a, e2):
    N = Np(f, a, e2)
    X = (N + h) * np.cos(f) * np.cos(l)
    Y = (N + h) * np.cos(f) * np.sin(l)
    Z = (N * (1 - e2) + h) * np.sin(f)
    return (X, Y, Z)


# macierz obrotu
def Rneu(f, l):
    R = np.array([[-np.sin(f) * np.cos(l), -np.sin(l), np.cos(f) * np.cos(l)],
                  [-np.sin(f) * np.sin(l), np.cos(l), np.cos(f) * np.sin(l)],
                  [np.cos(f), 0, np.sin(f)]])
    return (R)


# wektor obserwacji -> wektor neu
def saz2neu(s, alfa, z):
    dneu = np.array([s * np.sin(z) * np.cos(alfa),
                     s * np.sin(z) * np.sin(alfa),
                     s * cos(z)])
    return (dneu)


# neu -> wspolrzednych prostokatnych
def neu2XYZ(dneu, f, l):
    R = Rneu(f, l)
    return (R @ dneu)


# wspolrzedne prostokatne -> wektor neu
def XYZ2neu(dXYZ, f, l):
    R = Rneu(f, l)
    return (R.T @ dXYZ)


# wektor neu -> wektor obserwacji
def neu2saz(dneu):
    s = np.sqrt(dneu @ dneu)
    alfa = np.arctan2(dneu[1], dneu[0])
    z = np.arccos(dneu[2] / s)
    return (s, alfa, z)


def dms2rad(d, m, s):
    kat_rad = radians(d + m / 60 + s / 3600)
    return (kat_rad)


def kivioj(f, l, A, s, a, e2):
    n = int(s / 1000)
    ds = s / n
    for i in range(n):
        M = Mp(f, a, e2)
        N = Np(f, a, e2)
        df = ds * np.cos(A) / M
        dA = ds * np.sin(A) * np.tan(f) / N
        fm = f + df / 2
        Am = A + dA / 2
        Nm = a / np.sqrt(1 - e2 * np.sin(fm) ** 2)
        Mm = a * (1 - e2) / np.sqrt((1 - e2 * np.sin(fm) ** 2)) ** 3
        df = ds * np.cos(Am) / Mm
        dA = ds * np.sin(Am) * np.tan(fm) / Nm
        dl = (ds * np.sin(Am)) / (Nm * np.cos(fm))
        f = f + df
        l = l + dl
        A = A + dA
    A = A + pi
    if A > 2 * pi:
        A = A - 2 * pi
    return (f, l, A)


def vincenty(fa, la, fb, lb, a, e2):
    b = a * np.sqrt(1 - e2)
    # print('b = ', b)
    fl = 1 - (b / a)
    # print('f = ', fl)
    Ua = atan((1 - fl) * tan(fa))
    # print('Ua = ', Ua)
    Ub = atan((1 - fl) * tan(fb))
    # print('Ub = ', Ub)
    dl = lb - la
    # print('dl = ')
    # dms(dl)
    L = dl
    while True:
        ss = np.sqrt(((cos(Ub) * sin(L)) ** 2) + ((cos(Ua) * sin(Ub)) - sin(Ua) * cos(Ub) * cos(L)) ** 2)
        cs = (sin(Ua) * sin(Ub)) + (cos(Ua) * cos(Ub) * cos(L))
        sigma = atan(ss / cs)
        sa = (cos(Ua) * cos(Ub) * sin(L)) / ss
        c2a = 1 - (sa ** 2)
        c2sm = cs - ((2 * sin(Ua) * sin(Ub)) / c2a)
        C = (fl / 16) * c2a * (4 + fl * (4 - 3 * c2a))
        Lp = L
        L = dl + (1 - C) * fl * sa * (sigma + C * ss * (c2sm + C * cs * (-1 + 2 * (c2sm ** 2))))
        if abs(Lp - L) < (0.000001 / 206265):
            break
    u2 = ((a ** 2 - b ** 2) / b ** 2) * c2a
    A = 1 + ((u2 / 16384) * (4096 + u2 * (-768 + u2 * (320 - 175 * u2))))
    B = (u2 / 1024) * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    ds = B * ss * (c2sm + (B / 4) * (
                cs * (-1 + 2 * (c2sm ** 2)) - (B / 6) * c2sm * (-3 + 4 * (ss ** 2)) * (-3 + 4 * (c2sm ** 2))))
    sab = b * A * (sigma - ds)
    Aab = atan2((cos(Ub) * sin(L)), ((cos(Ua) * sin(Ub)) - (sin(Ua) * cos(Ub) * cos(L))))
    Aba = atan2((cos(Ua) * sin(L)), (((- sin(Ua)) * cos(Ub)) + cos(Ua) * sin(Ub) * cos(L))) + pi
    if Aba > 2 * pi:
        Aba = Aba - 2 * pi
    if Aba < 0:
        Aba = Aba + 2 * pi
    return (Aab, Aba, sab)


def A_0(e2):
    A0 = 1 - (e2 / 4) - ((3 * e2 ** 2) / 64) - ((5 * e2 ** 3) / 256)
    return (A0)


def A_2(e2):
    A2 = (3 / 8) * (e2 + (e2 ** 2) / 4 + (15 * e2 ** 3) / 128)
    return (A2)


def A_4(e2):
    A4 = (15 / 256) * (e2 ** 2 + (3 * e2 ** 3) / 4)
    return (A4)


def A_6(e2):
    A6 = (35 * e2 ** 3) / 3072
    return (A6)


def sigma(fi, a, e2):
    A0 = A_0(e2)
    A2 = A_2(e2)
    A4 = A_4(e2)
    A6 = A_6(e2)
    sig = a * ((A0 * fi) - (A2 * sin(2 * fi)) + (A4 * sin(4 * fi)) - (A6 * sin(6 * fi)))
    return (sig)

def Np(f, a, e2):
    N = a / np.sqrt(1 - e2 * np.sin(f) ** 2)
    return (N)


def Mp(f, a, e2):
    M = a * (1 - e2) / np.sqrt((1 - e2 * np.sin(f) ** 2)) ** 3
    return (M)


# wspolrzedne prostokatne -> wspolrzedne geodezyjne
def hirvonen(X, Y, Z, a, e2):
    p = np.sqrt(X ** 2 + Y ** 2)
    # print('p=',p)
    f = np.arctan(Z / (p * (1 - e2)))
    # dms(f)
    while True:
        N = Np(f, a, e2)
        # print('N = ',N)
        h = (p / np.cos(f)) - N
        # print('h = ',h)
        fp = f
        f = np.arctan(Z / (p * (1 - e2 * (N / (N + h)))))
        # dms(f)
        if np.abs(fp - f) < (0.000001 / 206265):
            break
    l = np.arctan2(Y, X)
    return (f, l, h)

def phi1(xgk, a, e2):
    A0 = A_0(e2)
    fi = xgk / (a * A0)
    while True:
        sig = sigma(fi, a, e2)
        fip = fi
        fi = fi + ((xgk - sig) / (a * A0))
        if abs(fip - fi) < (0.000001 / 206265):
            break
    return (fi)


def fl2xygk(fi, lam, lam0, a, e2):
    b2 = (a ** 2) * (1 - e2)
    ep2 = (a ** 2 - b2) / b2
    dl = lam - lam0
    t = tan(fi)
    n2 = ep2 * (cos(fi) ** 2)
    N = Np(fi, a, e2)
    sig = sigma(fi, a, e2)
    xgk = sig + ((dl ** 2 / 2) * N * sin(fi) * cos(fi) * (
                1 + (((dl ** 2) / 12) * (cos(fi) ** 2) * (5 - t ** 2 + 9 * n2 + 4 * n2 ** 2)) + (
                    ((dl ** 4) / 360) * (cos(fi) ** 4) * (
                        61 - 58 * (t ** 2) + t ** 4 + 270 * n2 - 330 * n2 * (t ** 2)))))
    ygk = dl * N * cos(fi) * (1 + (((dl ** 2) / 6) * (cos(fi) ** 2) * (1 - t ** 2 + n2)) + (
                ((dl ** 4) / 120) * (cos(fi) ** 4) * (5 - 18 * t ** 2 + t ** 4 + 14 * n2 - 58 * n2 * t ** 2)))
    return (xgk, ygk)


def xygk2fl(xgk, ygk, lam0, a, e2):
    b2 = (a ** 2) * (1 - e2)
    ep2 = (a ** 2 - b2) / b2
    fi = phi1(xgk, a, e2)
    N = Np(fi, a, e2)
    M = Mp(fi, a, e2)
    t = tan(fi)
    n2 = ep2 * (cos(fi) ** 2)
    f = fi - ((((ygk ** 2) * t) / (2 * M * N)) * (
                1 - ((ygk ** 2) / (12 * N ** 2)) * (5 + 3 * t ** 2 + n2 - 9 * n2 * t ** 2 - 4 * n2 ** 2) + (
                    (ygk ** 4) / (360 * N ** 4)) * (61 + 90 * (t ** 2) + 45 * (t ** 4))))
    l = lam0 + (ygk) / (N * cos(fi)) * (
                1 - ((ygk ** 2) / (6 * N ** 2)) * (1 + 2 * t ** 2 + n2) + ((ygk ** 4) / (120 * N ** 4)) * (
                    5 + 28 * t ** 2 + 24 * t ** 4 + 6 * n2 + 8 * n2 * t ** 2))
    gamma = (ygk / N) * t * (1 - ((ygk ** 2) / (3 * (N ** 2))) * (1 + (t ** 2) - n2 - (2 * (n2 ** 2))) + (
                (ygk ** 4) / (15 * (N ** 4))) * (2 + (5 * (t ** 2)) + 3 * (t ** 4)))
    return (f, l, gamma)


def strefy2000(l):
    lam0 = 0
    n = 0
    if l >= dms2rad(13, 30, 0) and l < dms2rad(16, 30, 0):
        lam0 = lam0 + dms2rad(15, 0, 0)
        n = n + 5
    if l >= dms2rad(16, 30, 0) and l < dms2rad(19, 30, 0):
        lam0 = lam0 + dms2rad(18, 0, 0)
        n = n + 6
    if l >= dms2rad(19, 30, 0) and l < dms2rad(22, 30, 0):
        lam0 = lam0 + dms2rad(21, 0, 0)
        n = n + 7
    if l >= dms2rad(22, 30, 0) and l < dms2rad(25, 30, 0):
        lam0 = lam0 + dms2rad(24, 0, 0)
        n = n + 8
    return (lam0, n)


def xy2000(xgk, ygk, n):
    m = 0.999923
    x = xgk * m
    y = ygk * m + n * 1000000 + 500000
    return (x, y)


def xy1992(xgk, ygk):
    m = 0.9993
    x = xgk * m - 5300000
    y = ygk * m + 500000
    return (x, y)


def xy20002xygk(x2000, y2000):
    m = 0.999923
    n = floor(y2000 / 1000000)
    xgk = x2000 / m
    ygk = (y2000 - n * 1000000 - 500000) / m
    return (xgk, ygk)


def xy19922xygk(x1992, y1992):
    m = 0.9993
    xgk = (x1992 + 5300000) / m
    ygk = (y1992 - 500000) / m
    return (xgk, ygk)


def lambda0(y2000):
    n = floor(y2000 / 1000000)
    lam = 0
    if n == 5:
        lam = lam + dms2rad(15, 0, 0)
    if n == 6:
        lam = lam + dms2rad(18, 0, 0)
    if n == 7:
        lam = lam + dms2rad(21, 0, 0)
    if n == 8:
        lam = lam + dms2rad(24, 0, 0)
    return (lam)


def xy922xy20(x92, y92, a, e2):
    xgk, ygk = xy19922xygk(x92, y92)
    lam092 = dms2rad(19, 0, 0)
    f, l = xygk2fl(xgk, ygk, lam092, a, e2)
    lam0, n = strefy2000(l)
    xgk, ygk = fl2xygk(f, l, lam0, a, e2)
    xgk2, ygk2 = xy2000(xgk, ygk, n)
    return (xgk2, ygk2)


def xy202xy92(x20, y20, a, e2):
    xgk, ygk = xy20002xygk(x20, y20)
    lam = lambda0(y20)
    f, l = xygk2fl(xgk, ygk, lam, a, e2)
    lam092 = dms2rad(19, 00, 00)
    xgk, ygk = fl2xygk(f, l, lam092, a, e2)
    xgk92, ygk92 = xy1992(xgk, ygk)
    return (xgk92, ygk92)


def metry(x, txt):
    print(txt, '%6.3f' % x, 'm')


def skalagk(xgk, ygk, a, e2):
    fi1 = phi1(xgk, a, e2)
    R = np.sqrt(Np(fi1, a, e2) * Mp(fi1, a, e2))
    m = 1 + (ygk ** 2) / (2 * R ** 2) + ygk ** 4 / (24 * R ** 4)
    return (m)


def red_gk(xa, ya, xb, yb, l0, a, e2):
    xm = (xa + xb) / 2
    ym = (ya + yb) / 2
    fm, lm, gamma = xygk2fl(xm, ym, l0, a, e2)
    Rm = np.sqrt(Mp(fm, a, e2) * Np(fm, a, e2))
    sgk = np.sqrt((xa - xb) ** 2 + (ya - yb) ** 2)
    r = sgk * (ya ** 2 + ya * yb + yb ** 2) / (6 * Rm ** 2)
    selip = sgk - r
    return (r, selip, sgk)


def azymut(xa, ya, xb, yb):
    dx = xb - xa
    dy = yb - ya
    Az = atan2(dy, dx)
    if Az < 0:
        Az = Az + 2 * pi
    return (Az)


# def azymut(xa,ya,xb,yb):
#     dxa = xb - xa
#     dya = yb - ya
#     Azab = atan2(dya, dxa)
#     if Azab < 0:
#         Azab = Azab + 2 * pi
#     dxb = xa - xb
#     dyb = ya - yb
#     Azba = atan2(dyb, dxb)
#     if Azba < 0:
#         Azba = Azba + 2 * pi
#     return(Azab,Azba)

def red_elip(xa, ya, xb, yb, l0, selip, a, e2):
    xm = (xa + xb) / 2
    ym = (ya + yb) / 2
    fm, lm = xygk2fl(xm, ym, l0, a, e2)
    Rm = np.sqrt(Mp(fm, a, e2) * Np(fm, a, e2))
    r = selip * (ya ** 2 + ya * yb + yb ** 2) / (6 * Rm ** 2)
    sgk = selip + r
    return (r, sgk)


def delta(xa, ya, xb, yb, l0, a, e2):
    Rm = Rmp(xa, ya, xb, yb, l0, a, e2)
    delab = ((xb - xa) * (2 * ya + yb)) / (6 * Rm ** 2)
    delba = ((xa - xb) * (2 * yb + ya)) / (6 * Rm ** 2)
    return (delab, delba)


def dmsaz(x, txt):
    sig = ' '
    if x < 0:
        sig = '-'
        x = abs(x)
    x = x * 180 / pi
    d = int(x)
    m = int(60 * (x - d))
    s = (x - d - m / 60) * 3600
    print(txt, sig, '%3d' % d, '°', '%2d' % m, "'", '%5.3f' % s, '"')


def spom2selip(xa, ya, xb, yb, ha, hb, spom, l0, a, e2):
    Rm = Rmp(xa, ya, xb, yb, l0, a, e2)
    dh = hb - ha
    s0 = np.sqrt((spom ** 2 - dh ** 2) / ((1 + ha / Rm) * (1 + hb / Rm)))
    selip = 2 * Rm * np.arcsin(s0 / (2 * Rm))
    return (selip, s0)


def Rmp(xa, ya, xb, yb, l0, a, e2):
    xm = (xa + xb) / 2
    ym = (ya + yb) / 2
    fm, lm, gamma = xygk2fl(xm, ym, l0, a, e2)
    Rm = np.sqrt(Mp(fm, a, e2) * Np(fm, a, e2))
    return (Rm)


def Bursa_Wolf(XYp, p):
    A = np.array([[p[0], p[3], -p[2]],
                  [-p[3], p[0], p[1]],
                  [p[2], -p[1], p[0]]])
    T = np.array([p[4], p[5], p[6]])
    Xw = XYp + A @ XYp + T
    return (Xw)


def Xtran(XYp, XYw):
    A = []
    for k in XYp:
        D = [k[0], 0, -k[2], k[1], 1, 0, 0]
        B = [k[1], k[2], 0, -k[0], 0, 1, 0]
        C = [k[2], -k[1], k[0], 0, 0, 0, 1]
        A.append(D)
        A.append(B)
        A.append(C)
    A = np.array(A)
    n, r = A.shape

    L = []
    for w, k in zip(XYw, XYp):
        dx = w[0] - k[0]
        dy = w[1] - k[1]
        dz = w[2] - k[2]
        L.append(dx)
        L.append(dy)
        L.append(dz)
    L = np.array(L)

    X = np.linalg.inv(A.T @ A) @ (A.T @ L)

    V = A @ X - L

    m0 = np.sqrt((V.T @ V) / (n - r))

    mk = m0 * np.sqrt((np.linalg.inv(A.T @ A))[0, 0])
    ma = m0 * np.sqrt((np.linalg.inv(A.T @ A))[1, 1])
    mb = m0 * np.sqrt((np.linalg.inv(A.T @ A))[2, 2])
    mg = m0 * np.sqrt((np.linalg.inv(A.T @ A))[3, 3])
    mx = m0 * np.sqrt((np.linalg.inv(A.T @ A))[4, 4])
    my = m0 * np.sqrt((np.linalg.inv(A.T @ A))[5, 5])
    mz = m0 * np.sqrt((np.linalg.inv(A.T @ A))[6, 6])
    m = [mk, ma, mb, mg, mx, my, mz]

    kp = X[0]
    a = X[1]
    b = X[2]
    g = X[3]
    dx = X[4]
    dy = X[5]
    dz = X[6]
    p = list(X)
    return (p, m0, m)

# AAB=αAB+γA+δAB
# ABA=αBA+γB+δBA