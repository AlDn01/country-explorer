"""
country_y.py - Yusuf's Part

Country Explorer CLI
Application structure, menu system, and session cache display logic.

This file uses Asem's API class from country_api.py.
Make sure country_api.py is in the same folder.
"""

from country_api import CountryExplorer, CountryNotFoundError, APIConnectionError
from ui.comparison import CountryComparator
from ui.formatting import CountryFormatter

def format_list(items: list) -> str:
    """Returns a clean string for list values."""
    return ", ".join(items) if items else "None"


def show_country(explorer: CountryExplorer, country: dict) -> None:
    """Displays one country in a simple readable format."""
    border_names = explorer.get_border_names(country["border_codes"])

    print("\n" + "=" * 50)
    print(f"Country: {country['common_name']}")
    print("=" * 50)
    print(f"Official name : {country['official_name']}")
    print(f"Capital       : {country['capital']}")
    print(f"Region        : {country['region']}")
    print(f"Population    : {country['population']:,}")
    print(f"Area          : {country['area']:,.1f} km^2")
    print(f"Currencies    : {format_list(country['currencies'])}")
    print(f"Languages     : {format_list(country['languages'])}")
    print(f"Borders       : {format_list(border_names)}")


def search_country(explorer: CountryExplorer) -> None:
    """Menu option 1: search for a country by name."""
    name = input("Enter country name: ").strip()
    country = explorer.get_country(name)
    show_country(explorer, country)


def compare_countries(explorer: CountryExplorer) -> None:
    """Menu option 2: compare two countries side by side."""

    comparator = CountryComparator(explorer)
    formatter = CountryFormatter()

    first_name = input("Enter first country: ").strip()
    second_name = input("Enter second country: ").strip()

    result = comparator.compare(first_name, second_name)
    formatter.print_comparison(result)


def show_top5_by_region(explorer: CountryExplorer) -> None:
    """Menu option 3: show top 5 countries by population in a region."""
    print("Available regions: Africa, Americas, Asia, Europe, Oceania")
    region = input("Enter region: ").strip()
    countries = explorer.get_top5_by_region(region)

    print("\n" + "=" * 55)
    print(f"Top 5 most populous countries in {region.title()}")
    print("=" * 55)

    for index, country in enumerate(countries, start=1):
        print(f"{index}. {country['common_name']:<25} {country['population']:,}")


def show_cache(explorer: CountryExplorer) -> None:
    """Shows countries saved in the session cache."""
    country_keys = [
        key for key, value in explorer.cache.items()
        if not key.startswith("__alpha_") and isinstance(value, dict)
    ]

    print("\n" + "=" * 45)
    print("Session Cache")
    print("=" * 45)

    if not country_keys:
        print("No countries searched yet.")
        return

    print("Countries already fetched in this run:")
    for index, key in enumerate(country_keys, start=1):
        print(f"{index}. {explorer.cache[key]['common_name']}")


def print_menu() -> None:
    """Prints the main CLI menu."""
    print("\n" + "=" * 45)
    print("Country Explorer CLI")
    print("=" * 45)
    print("1. Search for a country")
    print("2. Compare two countries")
    print("3. Show top 5 countries by region")
    print("4. View session cache")
    print("5. Exit")


def main() -> None:
    """Main application loop."""
    explorer = CountryExplorer()

    while True:
        print_menu()
        choice = input("Choose an option (1-5): ").strip()

        try:
            if choice == "1":
                search_country(explorer)
            elif choice == "2":
                compare_countries(explorer)
            elif choice == "3":
                show_top5_by_region(explorer)
            elif choice == "4":
                show_cache(explorer)
            elif choice == "5":
                print("Thank you for using Country Explorer. Goodbye!")
                break
            else:
                print("Invalid input. Please choose a number from 1 to 5.")

        except (CountryNotFoundError, APIConnectionError, ValueError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
