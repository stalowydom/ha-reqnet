# reQnet

Integracja Home Assistant dla central wentylacyjnych **reQnet** z wykorzystaniem lokalnego API HTTP.

> ⚠️ **Status projektu: Alpha**
>
> Integracja jest rozwijana i testowana. API oraz lista dostępnych encji mogą ulegać zmianom pomiędzy kolejnymi wersjami.

---

# Niezależny projekt społeczności

Ta integracja jest **niezależnym projektem społeczności Open Source**.

Nie jest tworzona, rozwijana ani wspierana przez producenta urządzeń **reQnet** ani firmę **Inprax**.

Projekt wykorzystuje udokumentowane lokalne API HTTP udostępnione przez producenta.

Jeżeli znajdziesz błąd lub masz pomysł na rozwój integracji, zgłoś **Issue** lub **Pull Request**.

---

# Funkcje

Aktualnie integracja udostępnia:

- status pracy centrali
- aktualny nawiew i wywiew
- temperatury:
  - czerpni
  - wyrzutni
  - nawiewu
  - wywiewu
  - wewnętrzną
- wilgotność
- stężenie CO₂
- tryb pracy
- status bypassu
- moc wentylatorów
- stopień wysterowania wentylatorów
- opory instalacji
- liczbę dni do wymiany filtrów

Dodatkowo dostępne są encje diagnostyczne:

- firmware
- kod błędu

---

# Wymagania

- Home Assistant 2026.7 lub nowszy
- Centrala reQnet wyposażona w moduł WiFi
- Dostęp do lokalnego API HTTP urządzenia

---

# Instalacja przez HACS (zalecana)

1. Zainstaluj HACS.
2. Dodaj repozytorium jako **Custom Repository**:

```
https://github.com/stalowydom/ha-reqnet
```

Typ:

```
Integration
```

3. Zainstaluj integrację **reQnet**.
4. Uruchom ponownie Home Assistant.
5. Dodaj integrację z poziomu:

```
Ustawienia
→ Urządzenia i usługi
→ Dodaj integrację
→ reQnet
```

6. Podaj adres IP centrali.

---

# Instalacja ręczna

Skopiuj katalog:

```
custom_components/reqnet
```

do:

```
/config/custom_components/
```

Uruchom ponownie Home Assistant.

---

# Dostępne encje

## Pomiary

- Temperatura wewnętrzna
- Temperatura czerpni
- Temperatura nawiewu
- Temperatura wywiewu
- Temperatura wyrzutni
- Wilgotność względna
- Stężenie CO₂
- Wydajność nawiewu
- Wydajność wywiewu
- Opór nawiewu
- Opór wywiewu
- Wysterowanie wentylatora nawiewu
- Wysterowanie wentylatora wywiewu
- Moc wentylatora nawiewu
- Moc wentylatora wywiewu
- Dni do wymiany filtrów

## Status

- Status centrali
- Tryb pracy
- Bypass

## Diagnostyka

- Firmware
- Kod błędu

---

# Roadmap

## v0.2

- sterowanie centralą
- wybór trybu pracy
- sterowanie bypass
- obsługa większej liczby funkcji API

## v0.3

- gotowe dashboardy Home Assistant
- automatyczne wykrywanie modelu urządzenia
- pełne tłumaczenia

## v1.0

- kompletna obsługa API
- stabilna wersja produkcyjna
- dokumentacja użytkownika
- dokumentacja dla programistów

---

# Zgłaszanie błędów

Jeżeli zauważysz problem lub masz pomysł na nową funkcję:

👉 GitHub Issues

Opisując problem podaj:

- model centrali
- wersję firmware
- wersję Home Assistanta
- wersję integracji
- log błędu (jeżeli występuje)

---

# Wsparcie

Producent urządzeń **reQnet** nie świadczy wsparcia technicznego dla tej integracji.

Wszelkie pytania i zgłoszenia dotyczące integracji należy kierować poprzez GitHub.

---

# Autor

Projekt rozwijany przez społeczność.

Autor projektu:

**Krzysztof Skibicki**

https://stalowydom.com

---

# Licencja

MIT License