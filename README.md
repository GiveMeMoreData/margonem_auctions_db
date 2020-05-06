# Margonem auctions
Ta prosta aplikacja konsolowa ma na celu połaczenie się bazą danych oraz uniemożliwienie podglądu jak i edycji danych. 
Wybraną tematyką jest rynek aukcyjny świecie popularnej (niegdyś) gry Margonem. Tak więc mamy wgląd w aktualne aukcje, przedmioty oraz postacie, które te przedmioty sprzedają. 
Chociaż nie jest to idealne odwzorowanie wszyskich danych z rynku Margonem, jest to baza, której niewiele brakuje do działania na rzeczywistych danych Margonem. Dalej planuje ją połączyć z webscrapperem, który te dane będzie sciągać. 

## Jak uruchomić
1. Należy utwożyć bazę danych Microsoft SQL Server z pliku sql_create.
2. Następnie uzupełnić ja danymi z pliku sql_fill.
3. Aplikacja jest napisana w Pythonie 3 i do pełnego działania potrzebuje biblioteki `pyodbc`, wystarczy w terminalu wpisać `pip install pyodbc`(oryginalnie pisana na wersji *pyodbc 4.0.30*).
4. W pliku `connector.py` należy podac poprawny url i dane do połączenia z bazą danych. 
5. Teraz wsytarczy odpalić plik `main.py`.

*Gdyby jednak trafiły się nieoczekiwane błędy, proszę o kontakt*


## Funkcje aplikacji
* Szybki wgląd w ładnie sformatowane dane 
* Dodanie nowych wierszy
* Edycja wierszy spełniających różne warunki
* Usunięcie wierszy spełniających różne warunki
* Generowanie użytecznego raportu o rynku i użytkownikach 
* Zapis historii raportów do pliku .txt


## Znane ograniczenia
* Dane typu `Date` trzeba wspisywać w jeden okreslony sposób i jest to 'dd/mm:/YYYY HH:MM:SS', czyli np '06/05/2020 14:45:50'
* nie da się wykorzystać daty przy warunkach edycji/usuwania
