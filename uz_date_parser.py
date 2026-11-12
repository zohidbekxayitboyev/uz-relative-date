import re
from datetime import datetime, timedelta
from typing import Optional


class UzbekDateParser:
    """
    A lightweight NLP parser for converting Uzbek relative date expressions
    (e.g., 'kecha', 'bugun', '3 kun oldin', 'keyingi hafta') into datetime objects.
    """

    WEEKDAYS = {
        "dushanba": 0,
        "seshanba": 1,
        "chorshanba": 2,
        "payshanba": 3,
        "juma": 4,
        "shanba": 5,
        "yakshanba": 6,
    }

    def __init__(self, base_date: Optional[datetime] = None):
        self.base_date = base_date or datetime.now()

    def parse(self, text: str) -> Optional[datetime]:
        """
        Parses an Uzbek string containing a relative date expression and returns
        the resolved datetime object.
        """
        cleaned = text.lower().strip()

        # 1. Direct relative day matches
        if "o'tgan kecha" in cleaned or "avvalgi kun" in cleaned:
            return self.base_date - timedelta(days=2)
        if "kecha" in cleaned:
            return self.base_date - timedelta(days=1)
        if "bugun" in cleaned or "hozir" in cleaned:
            return self.base_date
        if "indinga" in cleaned or "indin" in cleaned:
            return self.base_date + timedelta(days=2)
        if "ertaga" in cleaned:
            return self.base_date + timedelta(days=1)

        # 2. Numeric offsets: "X kun/hafta/oy oldin/avval"
        past_match = re.search(r"(\d+)\s*(kun|hafta|oy)\s*(oldin|avval|ilgari)", cleaned)
        if past_match:
            amount = int(past_match.group(1))
            unit = past_match.group(2)
            return self._apply_offset(-amount, unit)

        # 3. Numeric offsets: "X kun/hafta/oy keyin" or "X kundan/haftadan keyin"
        future_match = re.search(r"(\d+)\s*(kun|hafta|oy)(?:dan)?\s*(keyin|so'ng)", cleaned)
        if future_match:
            amount = int(future_match.group(1))
            unit = future_match.group(2)
            return self._apply_offset(amount, unit)

        # 4. Last / Next week or month
        if "o'tgan hafta" in cleaned:
            return self.base_date - timedelta(weeks=1)
        if "keyingi hafta" in cleaned or "kelasi hafta" in cleaned:
            return self.base_date + timedelta(weeks=1)
        if "o'tgan oy" in cleaned:
            return self.base_date - timedelta(days=30)
        if "keyingi oy" in cleaned or "kelasi oy" in cleaned:
            return self.base_date + timedelta(days=30)

        # 5. Weekday resolution (e.g., "keyingi juma", "o'tgan dushanba", or standalone weekday)
        for day_name, day_idx in self.WEEKDAYS.items():
            if day_name in cleaned:
                current_idx = self.base_date.weekday()
                if "o'tgan" in cleaned or "avvalgi" in cleaned:
                    days_behind = (current_idx - day_idx) % 7
                    days_behind = 7 if days_behind == 0 else days_behind
                    return self.base_date - timedelta(days=days_behind)
                else:
                    days_ahead = (day_idx - current_idx) % 7
                    days_ahead = 7 if days_ahead == 0 else days_ahead
                    return self.base_date + timedelta(days=days_ahead)

        return None

    def _apply_offset(self, amount: int, unit: str) -> datetime:
        if unit == "kun":
            return self.base_date + timedelta(days=amount)
        elif unit == "hafta":
            return self.base_date + timedelta(weeks=amount)
        elif unit == "oy":
            return self.base_date + timedelta(days=amount * 30)
        return self.base_date


def parse_uz_date(text: str, base_date: Optional[datetime] = None) -> Optional[datetime]:
    """Helper function to quickly parse an Uzbek date expression."""
    parser = UzbekDateParser(base_date=base_date)
    return parser.parse(text)
