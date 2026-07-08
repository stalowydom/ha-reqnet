# reQnet dla Home Assistant

Integracja Home Assistant dla central wentylacyjnych reQnet.

> ⚠️ Projekt znajduje się w fazie **Alpha**.
> Integracja jest rozwijana i testowana. API oraz lista encji mogą ulegać zmianom.

---

## Funkcje

Aktualnie integracja udostępnia:

- Status pracy centrali
- Aktualny nawiew i wyciąg
- Temperaturę:
  - czerpni
  - wyrzutni
  - nawiewu
  - wyciągu
  - wewnętrzną
- Wilgotność
- Stężenie CO₂
- Tryb pracy
- Status bypassu
- Moc wentylatorów
- Dni do wymiany filtrów

---

## Wymagania

- Home Assistant 2026.x lub nowszy
- Centrala reQnet z modułem WiFi
- Dostęp do lokalnego API HTTP

---

## Instalacja

### 1. Pobierz repozytorium

```bash
git clone https://github.com/stalowydom/ha-reqnet.git
```

lub pobierz archiwum ZIP.

### 2. Skopiuj integrację

Skopiuj katalog:

```
custom_components/reqnet
```

do:

```
config/custom_components/
```

Powinieneś otrzymać:

```
config/
└── custom_components/
    └── reqnet/
```

### 3. Restart Home Assistanta

Po restarcie przejdź do:

```
Ustawienia
→ Urządzenia i usługi
→ Dodaj integrację
```

i wybierz:

```
reQnet
```

### 4. Podaj adres IP

Przykład:

```
192.168.1.133
```

---

## Test API

Przed instalacją możesz sprawdzić działanie API:

```bash
curl "http://192.168.1.133/API/RunFunction?name=CurrentWorkParameters"
```

Jeżeli odpowiedź zawiera:

```json
"CurrentWorkParametersResult": true
```

to integracja powinna połączyć się poprawnie.

---

## Roadmapa

### v0.1

- komunikacja HTTP
- Config Flow
- podstawowe sensory

### v0.2

- Binary Sensors
- pełne tłumaczenia PL
- diagnostyka

### v0.3

- sterowanie trybami pracy
- bypass
- reset filtrów

### v1.0

- publikacja w HACS
- pełna dokumentacja
- obsługa wszystkich funkcji API

---

## Zgłaszanie błędów

Jeżeli znajdziesz problem lub masz pomysł na rozwój integracji, utwórz Issue:

https://github.com/stalowydom/ha-reqnet/issues

---

## Licencja

MIT