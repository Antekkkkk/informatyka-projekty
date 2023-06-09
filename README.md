# Informatyka-projekt-1
Projekt został napisany w ramach zajęć z Informatyki na 4 semestrze na kierunku Geodezja i Kartografia.

W skład projektu wchodzą 2 pliki - gw.py i projekt1.py. W pliku gw.py znajdują się funkcje napisane w 3 semestrze studiów, które dokonują geodezyjnych obliczeń. Plik projekt1.py to kod który jest wywoływany, i który za pomocą funkcji z pliku gw.py tworzy plik z wynikami. .

Działanie kodu opiera się na podanym przez użytkownika pliku w formacie txt. Pierwsza linijka powinna zawierać rodzaj danych, czyli jedno z dwóch: 'XYZ', albo 'flh'. Kolejna 
linijka powinna zawierać nazwę elipsoidy. Obsługiwane są 3: 'GRS80', 'WGS84' i 'Krasowski'. W 3 linijce należy wpisać w dowolnej kolejności transformacje, które chcemy wykonać. Dla danych 'XYZ' będą to NEU alb FLH, a dla danych FLH będą to XYZ, 1992, 2000.

UWAGA! Nie zalecane jest korzystanie z obliczeń korzystających z elipsoidy Krasowskiego, gdyż wyniki będą błędne.

Następnie należy podać dane. W jednym wierszu powinny znajdować się kolejno dane x y z (wyrażone w metrach), albo f l h (wyrażone w stopniach dziesiętnych), oddzielone od siebie spacją. Wyniki podane będą w takich samych jednostkach. Przykład:


![image](https://github.com/Antekkkkk/informatyka-projekty/assets/129069654/bf61a1bd-60be-4db9-942a-f6b767970b45)


Uwaga: przy obliczaniu Neu, podczas wywoywania pliku, po sciezce do pliku nalezy wpisac kolejo X0 Y0 i Z0

Wynikiem będą przeliczone dane, które będą odpowiednio poopisywane. Gotowy plik zapisze się w folderzee w którym znajduje się kod, pod nazwą 'otrzymane wyniki.txt'


Program należy odpalić za pomocą wiersza poleceń w pythonie. najpierw należy wpisać 'python', potem ścieżke kodu, a potem ścieżkę pliku z danymi.
![image](https://user-images.githubusercontent.com/129069654/235513886-d61a3c17-9968-4d05-b9ba-6d584b99a5ad.png)

Uwaga: program został napisany w pythonie 3.8, a użyte biblioteki to numpy, os, argparse, math. W folderze z kodem powinien znajdować się także plik gw, zawierający funkcje dokonujących obliczeń. Jednostki danych powinny być albo w metrach (XYZ), albo w stopniach dziesiętnych (flh).

Przykład pliku z wynikami:

![image](https://github.com/Antekkkkk/informatyka-projekty/assets/129069654/23f4b738-bb4e-4216-bb09-1d0cb904fc4e)

lub

![image](https://user-images.githubusercontent.com/129069654/235516816-a1b9a33f-6271-4834-ac9e-b69ff7fc76b2.png)

Kod ten umożliwia przeliczanie współrzędnych na kolejno:
 - Z danych XYZ na fi lambda h oraz układ neu
 - Z danych fi lambda h na XYZ, oraz z danej elipsoidy na układ 2000 i 1992.


Znane błędy:
 - Błąd, gdy w podanym pliku liczby po przecinku podane są z przecinkiem a nie kropką.
 - Jeśli w nazwie podanej elipsoidy znajdą się naraz pewne znaki, np 8 i 0, program i tak je obsłuży ale wyniki będą złe. 
 - Plik otrzymany wyświetla komunikat o podanych danych. Czasem wyświetla się niepoprawnie, choć można rozczytać co program miał na myśli. Błąd bardziej estetyczny.
 - UWAGA! Nie zalecane jest korzystanie z obliczeń korzystających z elipsoidy Krasowskiego, gdyż wyniki będą błędne.
