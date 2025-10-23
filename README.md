# POP-Voyager

Search and optimization Project -> Find the most efficient route for spaceship collecting resources from planets.

### Zadanie 12.

Jesteś kapitanem statku USS Voyager i próbujesz powrócić na Ziemię z Kwadrantu Delta, ale przed wyruszeniem w drogę z planety \(P\) musisz zgromadzić odpowiednią ilość deuteru. Możesz odwiedzić \(n\) stacji kosmicznych — odwiedzając stację kosmiczną \(s*i\) zyskujesz \(d_i\) jednostek deuteru. Podróż między stacjami kosmicznymi \(s_i\) i \(s_j\) kosztuje Cię \(k*{ij} > 0\) jednostek deuteru.

Zaprojektuj eksperyment, w którym wykorzystasz algorytmy heurystyczne w celu znalezienia trasy cyklicznej między planetą \(P\), a stacjami kosmicznymi, która zapewni Ci maksymalny stosunek zysków do strat.

### Interpretacja

- Problem znalezienia cyklu w grafie (każdy wierzchołek połączony z każdym).
  - Do generowania tego można np. użyć koordynatów xyz, koszt liczyć na podstawie odległości między stacjami i zrobić z tego graf (wtedy pewnie jakaś wizualizacja by mogła być), (P to mogłoby być (0, 0, 0))
- Optymalizujemy stosunek sumy zysków do sumy kosztów.
- Odwiedzając wierzchołek tylko przy pierwszej wizycie otrzymujemy nagrodę.

### Ograniczenia

- Dana maksymalna liczba wierzchołków możliwych do odwiedzenia \(n\).
- Początek i koniec w wierzchołku \(P\) (n + 1 przebytych krawędzi)

https://home.ttic.edu/~avrim/Papers/orienteering-sicomp.pdf?utm_source=chatgpt.com
