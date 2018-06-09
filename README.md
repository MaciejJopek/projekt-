# Projekt
Raport 1

Planuję zrobić robota na Raspberry sterowanego przy pomocy aplikacji napisanej w pythone. Chcę, aby przekazywał ona dane takie jak temperature oraz ciśnienie do pythona, które będą pokazywane w czasie rzeczywistym. Robot zostanie dodatkowo wyposażony w czujnik odległości, który umozliwi robotowi odnajdowanie sie w otoczeniu. Wykorzystam do tego między innymi biblieke, RPi.GPIO. Aplikacja zostanie prawdopodobnie wykonana z użyciem biblioteki Tkinter. 

Raport 2

Zrobione: Powstał juz zarys aplikacji okienkowej przy pomocy biblioteki PyQt5, możliwe jest juz reczne sterowanie robotem przy jej użyciu. Robot jest juz wstanie odczytać odległość dzielącą go od przeszkody przy wykorzystaniu czujnika odległości. Gdy znajdzie sie zbyt blisko niej sam zatrzyma prace silnikow.

Do zrobienia: Całkowicie automatyczne poruszanie się robota, dodanie czujnika temperatury oraz ciśnienia oraz przedstawienie wyników w postaci wykresu w czasie rzeczywistym.

Raport 3

Zrobione: Dodano losowe wybieranie drogi przez robota ( początkowo skręcał tylko w jedą stronę). Dodatkowo możliwy jest zapis danych odebranych z czujnika temperatury do pliku w celu jego ewentualnej późniejszej analizy. Wprowadzono wysyłanie danych z termometru do serwisu Domoticz, któru umożliwia generowanie wykresów. 

Dodano możliowść kontrolowania mocy samochodu, umożliwiając zmiane jego predkosci.