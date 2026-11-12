# uz-relative-date 🇺🇿📅

A lightweight, zero-dependency Python NLP utility for parsing natural Uzbek relative date and time expressions (e.g., *"kecha"*, *"3 kundan keyin"*, *"o'tgan dushanba"*) into standard Python `datetime` objects.

Built for chatbots, financial trackers, task schedulers, and AI assistants operating in the Uzbek language.

## Features
- **Zero external dependencies:** Uses pure Python standard library (`datetime`, `re`).
- **Natural sentence extraction:** Detects relative date expressions embedded inside conversational Uzbek text.
- **Weekday resolution:** Accurately calculates upcoming and past weekdays relative to a base date.

## Quick Usage

```python
from datetime import datetime
from uz_date_parser import parse_uz_date

base = datetime(2026, 11, 11)

print(parse_uz_date("Kecha hisobotni topshirdim", base_date=base))
# Output: 2026-11-10 00:00:00

print(parse_uz_date("Qarzni 5 kundan keyin qaytaraman", base_date=base))
# Output: 2026-11-16 00:00:00

print(parse_uz_date("Keyingi juma uchrashamiz", base_date=base))
# Output: 2026-11-13 00:00:00
