## Case: RUSH HOUR

Dit project voor het vak 'Heuristieken' richt zich op het oplossen van het Rush Hour -spel. [Uitleg spel.](https://en.wikipedia.org/wiki/Rush_Hour_(board_game))

**Regels van het spel**

* Bordmaten kunnen variëren. (6x6, 9x9 & 12x12)
* Voertuigen kunnen 2 (auto's) of 3 (vrachwagens) vakjes lang zijn
* Wanneer voertuigen horizontaal gepositioneerd staan op het bord, mogen deze alleen of naar links of naar rechts geschoven worden
* Wanneer voertuigen verticaal gepositioneerd staan op het bord, mogen deze alleen of naar boven of naar beneden geschoven worden
* Het spel moet worden opgelost in een zo min mogelijk aantal stappen

**Bestandsformaat van het bord**

* Borden worden gerepresenteerd als .txt-bestanden.

## Installatie

* [Python 3.6.3](https://www.python.org/downloads/release/python-363/)
* [Matplotlib 2.1.0](https://matplotlib.org/2.1.0/users/installing.html)
* [Numpy 1.13.3](https://pypi.python.org/pypi?:action=files&name=numpy&version=1.13.3)

## Terminal command line

**Gebruik van algoritme Breadth First Search (BFS)**

```
python algorithms/bfs.py <BOARD>.txt
```

**Gebruik van algoritme Depth First Search (DFS)**

```
python algorithms/dfs.py <BOARD>.txt
```
**Gebruik van algoritme Random Search**

```
python algorithms/random_search.py <BOARD>.txt
```

## Algoritmen Methode

**Breadth First Search** 
* De BFS is een zoekalgoritme op een graaf dat begint bij de beginknoop van de graaf en dat voor elk van de kinderen (paths) kijkt of het de oplossing is. 


**Depth First Search**
* DFS is een zoekalgoritme voor het doorzoeken van een boomstructuur of een graaf. Het algoritme begint bij de wortel (of eender welke knoop bij een graaf) en kiest een tak en doorzoekt deze zo ver mogelijk, zonder terug te keren op vorige stappen.

**Random Search**
* Random search is een zoekalgoritme op een graaf dat begint bij de begin knoop en berekent de mogelijk borden. Deze worden aan de stack toegevoegd en er wordt random een bord gekozen voor de volgende "ronde". De andere borden worden weggegooid. Zo gaat het algoritme door tot er een oplossing gevonden is.

**State Space Rush Hour**
* De state space kan berekend worden met de volgende formule:  **State Space = a<sup>b</sup> &ast; c<sup>d</sup> <br>**
Hierbij staat "a" voor het **aantal auto's** op het bord en "b" voor het **aantal posities** die een auto kan aannemen wanneer er geen andere voertuigen zich op het bord bevinden. <br>
Hierbij staat "c" voor het **aantal auto's** op het bord en "d" voor het **aantal posities** die een vrachtwagen kan aannemen wanneer er geen andere voertuigen zich op het bord bevinden.

| Board          | State Space                                                                          | 
|:---------------|:-------------------------------------------------------------------------------------|
| Board 1        | 5<sup>6</sup> &ast; 4<sup>3</sup> = 1.000.000 mogelijkheden                          |
| Board 2        | 5<sup>12</sup> &ast; 4<sup>1</sup> = 976.562.500 mogelijkheden                       |
| Board 3        | 5<sup>12</sup> &ast; 4<sup>1</sup> = 976.562.500 mogelijkheden                       |
| Bigger board 1 | 8<sup>12</sup> &ast; 7<sup>10</sup> = 2,77 &ast; 10<sup>18</sup> mogelijkheden       |
| Bigger board 2 | 8<sup>18</sup> &ast; 7<sup>6</sup> = 2,12 &ast; 10<sup>21</sup> mogelijkheden        |
| Bigger board 3 | 8<sup>18</sup> &ast; 7<sup>8</sup> = 1,038 &ast; 10<sup>23</sup> mogelijkheden       |
| Biggest board  | 11<sup>28</sup> &ast; 10<sup>16</sup> = 1,44 &ast; 10<sup>45</sup> mogelijkheden     |

## Visualisatie
* Optioneel kan de gebruiker ervoor kiezen om de visualisatie te zien, de gebruiker krijgt dan na het runnen van het algoritme de vraag of hij/zij de visualisatie wilt runnen. Dit kan worden gedaan door het typen van een "y" op de terminal.
* Het voorbeeld wat wordt weergegeven is de visualisatie van de BFS met board1.txt:
<img src="https://github.com/jimiduiveman/RushHour/blob/master/doc/bfs_demo.gif" width="220" height="220" />

## Algoritme Resultaten
* Grotere borden (9x9, 12x12) kunnen vereisen dat de algoritmen BFS & DFS wat langere tijd gaan draaien (NU langste: 5 uur).
* De runtime wordt aangegeven in seconden:

| Board          | BFS Runtime | DFS Runtime |  Random Runtime<sup>1</sup>  |
|:---------------|:------------|:------------|:-----------------------------|
| Board 1        | 2,9         | 76,8        | < 80                         |
| Board 2        | 0.6         | 1,8         | < 80                         |
| Board 3        | 0.2         | 1,5         | < 80                         |
| Bigger board 1 | 145         | 1064,5      | < 80                         |
| Bigger board 2 | > 18000     | 1172        | < 80                         |
| Bigger board 3 | > 18000     | > 18000     | < 80                         |
| Biggest board  | > 18000     | > 18000     | < 80                         |

* <sup>1</sup>Runtime Random Search varieert omdat het random is, echter is er bijna altijd een oplossing binnen 120 seconden.
 
## Dankwoord
* De mensen van wie wij hun code als inspiratie hebben gebruikt
* Bram van de Heuvel voor de tips en assistentie elke week 

## Studenten
* Jimi Duiveman (11023163)
* Rob Dekker (11020067)
* Andrea Pineda (10590501)

![Logo GASSS](https://github.com/jimiduiveman/RushHour/blob/master/doc/logo2.png)
