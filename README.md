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


