class CountryFormatter:
    def __init__(self):
        pass

    def print_comparison(self, data: dict):
        """
        Takes structured comparison data and prints it cleanly in terminal.
        """

        c1 = data["country1"]
        c2 = data["country2"]
        diff = data["differences"]

        print("\n" + "=" * 70)
        print(f"{c1['name']}  VS  {c2['name']}".center(70))
        print("=" * 70)

        # ───────────────────────── Population ─────────────────────────
        print("\nPOPULATION")
        print("-" * 70)
        print(f"{c1['name']:<20}: {c1['population']:,}")
        print(f"{c2['name']:<20}: {c2['population']:,}")
        print(f"{'Difference':<20}: {diff['population']:,}")

        # ───────────────────────── Area ─────────────────────────
        print("\nAREA (km²)")
        print("-" * 70)
        print(f"{c1['name']:<20}: {c1['area']:,.1f}")
        print(f"{c2['name']:<20}: {c2['area']:,.1f}")
        print(f"{'Difference':<20}: {diff['area']:,.1f}")

        # ───────────────────────── Languages ─────────────────────────
        print("\nLANGUAGES")
        print("-" * 70)
        print(f"{c1['name']:<20}: {len(c1['languages'])}")
        print(f"{c2['name']:<20}: {len(c2['languages'])}")
        print(f"{'More languages':<20}: {diff['more_languages']}")

        # ───────────────────────── Footer ─────────────────────────
        print("\n" + "=" * 70 + "\n")