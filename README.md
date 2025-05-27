# Pasjans Gigathon

## Sposób uruchomienia projektu

Aby uruchomić grę, wykonaj następujące kroki:

1. Upewnij się, że masz zainstalowanego Pythona w wersji 3.12 lub nowszej
2. Zainstaluj wymagane pakiety:

``` bash
    pip install -r .\requirements.txt
```

1. Uruchom grę za pomocą komendy, będąc w głównym folderze (PasjansGigathon) (testowane w Windows PowerShell oraz Command Prompt):

``` bash
   py main.py
```

## Instrukcje rozgrywki

### Klawisze

- **n** - Nowa gra
- **u** - Undo
- **?** - Pomoc
- **q** - Wyjście
- **c** - Zmiana Motywu

### Sterowanie

- Kliknij na ukrytą kartę ze stosu, aby odkryć karty
- Kliknij kartę z wierzchu, aby ją zaznaczyć.
- Kliknij kartę spod wierzchu, aby zaznaczyć wszystkie karty od wierzchniej do obecnej
- Gdy jest zaznaczona jedna karta, jeśli pozwalają na to reguły, można przenieść ją:
    - do stosu końcowego, klikając na niego
    - na inną kartę z innego stosu, klikając na wierzchnią kartę
- Gdy jest zaznaczone wiele kart, można przenieść je jedynie do innej kolumny, klikając na wierzchnią kartę

### Zasady gry

Celem gry jest ułożenie wszystkich kart w czterech stosach finałowych według kolorów i wartości (od asa do króla). Karty
można układać w kolumnach tablicy w malejącej kolejności i naprzemiennych kolorach.

## Opis modułów i klas

### Główne klasy

- **Game** - główna klasa aplikacji, zarządzająca całą grą
- **GameGrid** - klasa odpowiedzialna za wyświetlanie planszy
- **Card** - reprezentacja karty do gry
- **CardHolder** - puste miejsce na kartę
- **Tableau** - klasa reprezentująca główną tablicę gry
- **Foundation** - klasa reprezentująca stosy finałowe
- **StashWaste** - klasa reprezentująca talię i stos odrzuconych kart

### System stylowania

Projekt wykorzystuje bibliotekę Textual CSS do stylowania interfejsu użytkownika. Plik `pasjans.tcss` zawiera definicje
stylów dla wszystkich elementów interfejsu.
Projekt został zaimplementowany jako aplikacja konsolowa z wykorzystaniem biblioteki Textual, która zapewnia
interaktywny interfejs użytkownika w terminalu.
