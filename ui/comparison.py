from country_api import CountryExplorer

class CountryComparator:
    def __init__(self, explorer: CountryExplorer):
        self.explorer = explorer

    def compare(self, country1: str, country2: str) -> dict:
        """
        Returns structured comparison data between two countries.
        No printing here — only computed results.
        """

        c1 = self.explorer.get_country(country1)
        c2 = self.explorer.get_country(country2)

        # Population difference
        pop_diff = abs(c1["population"] - c2["population"])

        # Area difference
        area_diff = abs(c1["area"] - c2["area"])

        # Languages comparison
        c1_lang_count = len(c1["languages"])
        c2_lang_count = len(c2["languages"])

        if c1_lang_count > c2_lang_count:
            more_lang = c1["common_name"]
        elif c2_lang_count > c1_lang_count:
            more_lang = c2["common_name"]
        else:
            more_lang = "Equal"

        return {
            "country1": {
                "name": c1["common_name"],
                "population": c1["population"],
                "area": c1["area"],
                "languages": c1["languages"],
            },
            "country2": {
                "name": c2["common_name"],
                "population": c2["population"],
                "area": c2["area"],
                "languages": c2["languages"],
            },
            "differences": {
                "population": pop_diff,
                "area": area_diff,
                "more_languages": more_lang,
            }
        }
