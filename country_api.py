"""
country_api.py — Asem's Part (API Calls, JSON Parsing & Error Handling)
Country Explorer CLI — Week 3 Internship Task
Team: Yusuf (CLI + cache), Asem (API layer), Allaa (comparison + formatting)

API: REST Countries v5  →  https://api.restcountries.com/countries/v5
Docs: https://restcountries.com/docs
"""

import requests

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

BASE_URL = "https://api.restcountries.com/countries/v5"
API_KEY  = "rc_live_bb01ce1cb6334194bdcaac7e6622c065"   # ← paste your full key from restcountries.com/api-keys
TIMEOUT  = 5                     # seconds — required by the task spec

HEADERS  = {"Authorization": f"Bearer {API_KEY}"}


# ─────────────────────────────────────────────
# CUSTOM EXCEPTIONS
# ─────────────────────────────────────────────

class CountryNotFoundError(Exception):
    """Raised when the API returns no results for a given country name."""
    pass


class APIConnectionError(Exception):
    """Raised when there is no internet connection or the request times out."""
    pass


# ─────────────────────────────────────────────
# MAIN CLASS — CountryExplorer
# ─────────────────────────────────────────────

class CountryExplorer:
    """
    Wraps all REST Countries v5 API calls.
    Includes a session cache so the same country is never fetched twice.
    """

    def __init__(self):
        # Session cache: { "egypt": { ...parsed country data... } }
        self.cache = {}

    # ─── PRIVATE: raw HTTP fetch ───────────────

    def _get(self, endpoint: str, params: dict = None) -> list:
        """
        Internal method. Makes a GET request to the given endpoint.
        Always uses a 5-second timeout and sends the API key in the header.
        Returns a parsed JSON list on success.
        Raises CountryNotFoundError or APIConnectionError on failure.
        """
        url = f"{BASE_URL}/{endpoint}"

        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT)

            # 404 means the API found nothing for that query
            if response.status_code == 404:
                raise CountryNotFoundError(
                    "No country matched your search. Please check the spelling and try again."
                )

            # 401 means the API key is wrong or missing
            if response.status_code == 401:
                raise APIConnectionError(
                    "API key is invalid or missing. Please check your key in country_api.py."
                )

            # Any other non-200 status is an unexpected API error
            response.raise_for_status()

            # v5 wraps results in { "data": { "objects": [...] } }
            result = response.json()
            objects = result.get("data", {}).get("objects", [])
            if not objects:
                raise CountryNotFoundError("No country matched your search. Please check the spelling and try again.")
            return objects

        except requests.exceptions.ConnectionError:
            raise APIConnectionError(
                "Could not reach the internet. Please check your connection and try again."
            )
        except requests.exceptions.Timeout:
            raise APIConnectionError(
                "The request timed out after 5 seconds. The server may be slow — please try again."
            )
        except requests.exceptions.HTTPError as e:
            raise APIConnectionError(f"Unexpected HTTP error: {e}")

    # ─── PRIVATE: parse a single country dict ──

    def _parse_country(self, raw: dict) -> dict:
        """
        Extracts and structures only the fields we need from the raw v5 API response.

        v5 JSON structure (key differences from v3.1):
          - Name     →  raw["names"]["common"] / raw["names"]["official"]
          - Capital  →  raw["capitals"][0]["name"]
          - Area     →  raw["area"]["kilometers"]
          - Currencies → raw["currencies"] is a LIST of {code, name, symbol}
          - Languages  → raw["languages"] is a LIST of {name, bcp47}
          - Borders    → raw["borders"] is a LIST of alpha_3 codes (strings)
          - Population → raw["demographics"]["population"]  OR  raw["population"]
        """

        # --- Name ---
        names        = raw.get("names", {})
        official_name = names.get("official", raw.get("name", {}).get("official", "N/A"))
        common_name   = names.get("common",   raw.get("name", {}).get("common",   "N/A"))

        # --- Capital ---
        capitals_list = raw.get("capitals", raw.get("capital", []))
        if capitals_list and isinstance(capitals_list[0], dict):
            capital = capitals_list[0].get("name", "N/A")
        elif capitals_list and isinstance(capitals_list[0], str):
            capital = capitals_list[0]
        else:
            capital = "N/A"

        # --- Region ---
        region = raw.get("region", "N/A")

        # --- Population (v5 may nest it under demographics) ---
        demographics = raw.get("demographics", {})
        population   = demographics.get("population", raw.get("population", 0)) or 0

        # --- Area (v5 nests it under area.kilometers) ---
        area_field = raw.get("area", 0)
        if isinstance(area_field, dict):
            area = area_field.get("kilometers", 0.0)
        else:
            area = area_field or 0.0

        # --- Currencies ---
        # v5: list of {code, name, symbol}
        # v3.1 fallback: dict of code → {name, symbol}
        currencies_raw = raw.get("currencies", [])
        currencies = []
        if isinstance(currencies_raw, list):
            for c in currencies_raw:
                name   = c.get("name", "Unknown")
                symbol = c.get("symbol", "")
                code   = c.get("code", "")
                currencies.append(f"{name} ({symbol}) [{code}]" if symbol else f"{name} [{code}]")
        elif isinstance(currencies_raw, dict):
            for code, info in currencies_raw.items():
                name   = info.get("name", "Unknown")
                symbol = info.get("symbol", "")
                currencies.append(f"{name} ({symbol}) [{code}]" if symbol else f"{name} [{code}]")

        # --- Languages ---
        # v5: list of {name, bcp47}
        # v3.1 fallback: dict of code → name
        languages_raw = raw.get("languages", [])
        if isinstance(languages_raw, list):
            languages = [lang.get("name", "Unknown") for lang in languages_raw]
        elif isinstance(languages_raw, dict):
            languages = list(languages_raw.values())
        else:
            languages = []

        # --- Border codes ---
        border_codes = raw.get("borders", [])

        return {
            "common_name":   common_name,
            "official_name": official_name,
            "capital":       capital,
            "region":        region,
            "population":    population,
            "area":          area,
            "currencies":    currencies,
            "languages":     languages,
            "border_codes":  border_codes,
        }

    # ─── PUBLIC: fetch one country by name ─────

    def get_country(self, name: str) -> dict:
        """
        Fetches and returns parsed data for a single country.
        Uses the session cache — if already fetched this run, no HTTP call is made.

        Parameters
        ----------
        name : str
            The country name as typed by the user (case-insensitive).

        Returns
        -------
        dict
            Parsed country data (see _parse_country for keys).

        Raises
        ------
        CountryNotFoundError  — if the country does not exist.
        APIConnectionError    — if the network fails or times out.
        ValueError            — if name is empty/blank.
        """
        name = name.strip()
        if not name:
            raise ValueError("Country name cannot be empty.")

        cache_key = name.lower()

        # Return from cache if available
        if cache_key in self.cache:
            print(f"  [cache] Using saved data for '{name}'.")
            return self.cache[cache_key]

        # v5 search by name uses query param: ?q=<name>
        raw_list = self._get("names.common", params={"q": name})

        # Take the first (closest) match
        parsed = self._parse_country(raw_list[0])

        # Save to cache
        self.cache[cache_key] = parsed

        return parsed

    # ─── PUBLIC: resolve border codes to full names ──

    def get_border_names(self, border_codes: list) -> list:
        """
        Converts a list of 3-letter country codes (e.g. ["EGY", "LBY"])
        into full common names (e.g. ["Egypt", "Libya"]).

        Uses ?codes=XX,YY,ZZ to batch-fetch all borders in one request.
        Codes that fail to resolve are replaced with the raw code string.
        """
        if not border_codes:
            return []

        # Check if all codes are already cached
        uncached = [c for c in border_codes if f"__alpha_{c.lower()}" not in self.cache]

        if uncached:
            try:
                # Batch fetch all border countries in one API call
                codes_filter = ",".join(uncached)
                raw_list = self._get(f"code?q={codes_filter}")
                for country_raw in raw_list:
                    names = country_raw.get("names", country_raw.get("name", {}))
                    common = names.get("common", "Unknown") if isinstance(names, dict) else "Unknown"
                    codes_block = country_raw.get("codes", {})
                    alpha3 = codes_block.get("alpha_3", "")
                    if alpha3:
                        self.cache[f"__alpha_{alpha3.lower()}"] = common
            except (CountryNotFoundError, APIConnectionError):
                pass  # Fall through — we'll use raw codes as fallback

        # Build result list preserving original order
        names = []
        for code in border_codes:
            cache_key = f"__alpha_{code.lower()}"
            names.append(self.cache.get(cache_key, code))

        return names

    # ─── PUBLIC: fetch top-5 most populous in a region ──

    def get_top5_by_region(self, region: str) -> list:
        """
        Returns the 5 most populous countries in the given region.

        Parameters
        ----------
        region : str
            One of: Africa, Americas, Asia, Europe, Oceania (case-insensitive).

        Returns
        -------
        list[dict]
            Up to 5 parsed country dicts, sorted by population descending.

        Raises
        ------
        ValueError            — if the region name is not recognised.
        CountryNotFoundError  — if the API returns nothing for that region.
        APIConnectionError    — on network/timeout errors.
        """
        valid_regions = {"africa", "americas", "asia", "europe", "oceania"}
        region_clean  = region.strip().lower()

        if region_clean not in valid_regions:
            raise ValueError(
                f"'{region}' is not a valid region. "
                f"Choose from: Africa, Americas, Asia, Europe, Oceania."
            )

        # v5 filters by region using query param: ?region=<region>
        raw_list = self._get(f"region/{region_clean.capitalize()}", params={"limit": 100})
        # Parse every country, sort by population, return top 5
        parsed_list = [self._parse_country(c) for c in raw_list]
        top5 = sorted(parsed_list, key=lambda c: c["population"], reverse=True)[:5]

        return top5


# ─────────────────────────────────────────────
# DEMO / QUICK TEST
# ─────────────────────────────────────────────

if __name__ == "__main__":
    explorer = CountryExplorer()

    # --- Test 1: Search a country ---
    print("=" * 50)
    print("TEST 1 — Search: Egypt")
    print("=" * 50)
    try:
        country = explorer.get_country("Egypt")
        print(f"Official name : {country['official_name']}")
        print(f"Capital       : {country['capital']}")
        print(f"Region        : {country['region']}")
        print(f"Population    : {country['population']:,}")
        print(f"Area          : {country['area']:,.1f} km²")
        print(f"Currencies    : {', '.join(country['currencies'])}")
        print(f"Languages     : {', '.join(country['languages'])}")
        border_names = explorer.get_border_names(country["border_codes"])
        print(f"Borders       : {', '.join(border_names) if border_names else 'None'}")
    except (CountryNotFoundError, APIConnectionError, ValueError) as e:
        print(f"Error: {e}")

    # --- Test 2: Cache hit ---
    print("\nTEST 2 — Same search again (should use cache)")
    try:
        explorer.get_country("Egypt")
        print("  Cache working correctly.")
    except Exception as e:
        print(f"Error: {e}")

    # --- Test 3: Top 5 in Asia ---
    print("\nTEST 3 — Top 5 most populous in Asia")
    try:
        top5 = explorer.get_top5_by_region("Asia")
        for i, c in enumerate(top5, 1):
            print(f"  {i}. {c['common_name']} — {c['population']:,}")
    except (CountryNotFoundError, APIConnectionError, ValueError) as e:
        print(f"Error: {e}")

    # --- Test 4: Invalid country ---
    print("\nTEST 4 — Invalid country name")
    try:
        explorer.get_country("Fakeland123")
    except CountryNotFoundError as e:
        print(f"Caught correctly → {e}")
    except APIConnectionError as e:
        print(f"Network error → {e}")

    # --- Test 5: Invalid region ---
    print("\nTEST 5 — Invalid region")
    try:
        explorer.get_top5_by_region("Westeros")
    except ValueError as e:
        print(f"Caught correctly → {e}")