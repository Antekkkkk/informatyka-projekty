# Informatyka-projekt-1
Projekt został napisany w ramach zajęć z Informatyki na 4 semestrze na kierunku Geodezja i Kartografia.

Działanie kodu opiera się na podanym przez użytkownika pliku w formacie txt. Pierwsza linijka powinna zawierać rodzaj danych, czyli jedno z dwóch: 'XYZ', albo 'flh'. Kolejna 
linijka powinna zawierać nazwę elipsoidy. Obsługiwane są 3: 'GRS80', 'WGS84' i 'Krasowski'.

Następnie należy podać dane. W jednym wierszu powinny znajdować się kolejno dane x y z, albo f l h, oddzielone od siebie spacją. Przykład:
![image](https://user-images.githubusercontent.com/129069654/235513210-5f12e9cc-0e6e-4cf3-bb84-977f53752102.png)


Wynikiem będą przeliczone dane, które będą odpowiednio poopisywane. Gotowy plik zapisze się w folderzee w którym znajduje się kod, pod nazwą 'otrzymane wyniki.txt'


Program należy odpalić za pomocą wiersza poleceń w pythonie. najpierw należy wpisać 'python', potem ścieżke kodu, a potem ścieżkępliku z danymi.
![image](https://user-images.githubusercontent.com/129069654/235513886-d61a3c17-9968-4d05-b9ba-6d584b99a5ad.png)

Uwaga: program został napisany w pythonie 3.8, a użyte biblioteki to numpy, os, argparse, math. W folderze z kodem powinien znajdować się także plik gw, zawierający funkcje dokonujących obliczeń. 

Przykład pliku z wynikami:

![image](https://user-images.githubusercontent.com/129069654/235519692-d4a05175-6a06-42b9-885e-f099e78311b0.png)

lub

![image](https://user-images.githubusercontent.com/129069654/235516816-a1b9a33f-6271-4834-ac9e-b69ff7fc76b2.png)

Kod ten umożliwia przeliczanie współrzędnych na kolejno:
 - Z danych XYZ na fi lambda h oraz układ neu
 - Z danych fi lambda h na XYZ, oraz z danej elipsoidy na układ 2000 i 1992.


Znane błędy:
 - Błąd, gdy w podanym pliku liczby po przecinku podane są z przecinkiem a nie kropką.
 - Jeśli w nazwie podanej elipsoidy znajdą się naraz pewne znaki, np 8 i 0, program i tak je obsłuży ale wyniki będą złe. 
 - Plik otrzymany wyświetla komunikat o podanych danych. Czasem wyświetla się niepoprawnie, choć można rozczytać co program miał na myśli. Błąd bardziej estetyczny.
