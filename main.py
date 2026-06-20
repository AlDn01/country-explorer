from country_api import CountryExplorer
from ui.comparison import CountryComparator
from ui.formatting import CountryFormatter


def main():
    explorer = CountryExplorer()
    comparator = CountryComparator(explorer)
    formatter = CountryFormatter()

    while True:
        print("\n" + "=" * 50)
        print("COUNTRY EXPLORER")
        print("=" * 50)
        print("1. Search country")
        print("2. Compare two countries")
        print("3. Top 5 by region")
        print("4. Exit")

        choice = input("\nChoose option: ").strip()

        # ───────────────────────── SEARCH ─────────────────────────
        if choice == "1":
            name = input("Enter country name: ").strip()

            try:
                c = explorer.get_country(name)

                print("\n" + "-" * 50)
                print(f"{c['common_name']} ({c['official_name']})")
                print("-" * 50)
                print(f"Capital     : {c['capital']}")
                print(f"Region      : {c['region']}")
                print(f"Population  : {c['population']:,}")
                print(f"Area        : {c['area']:,.1f} km²")
                print(f"Languages   : {', '.join(c['languages']) or 'None'}")
                print(f"Currencies   : {', '.join(c['currencies']) or 'None'}")

            except Exception as e:
                print(f"Error: {e}")

        # ───────────────────────── COMPARE ─────────────────────────
        elif choice == "2":
            c1 = input("First country: ").strip()
            c2 = input("Second country: ").strip()

            try:
                result = comparator.compare(c1, c2)
                formatter.print_comparison(result)

            except Exception as e:
                print(f"Error: {e}")

        # ───────────────────────── TOP 5 ─────────────────────────
        elif choice == "3":
            region = input("Region (Africa, Americas, Asia, Europe, Oceania): ").strip()

            try:
                top5 = explorer.get_top5_by_region(region)

                print("\n" + "=" * 50)
                print(f"TOP 5 — {region.upper()}")
                print("=" * 50)

                for i, c in enumerate(top5, 1):
                    print(f"{i}. {c['common_name']:<20} {c['population']:,}")

            except Exception as e:
                print(f"Error: {e}")

        # ───────────────────────── EXIT ─────────────────────────
        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()