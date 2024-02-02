import shodan
from collections import defaultdict, Counter
from termcolor import colored

# Set your Shodan API key here
API_KEY = 'HERE'

def print_banner():
    banner = """
 ░░░░░░ ░░░░░░   ░░░░░  ░░░    ░░ ░░   ░░ 
▒▒      ▒▒   ▒▒ ▒▒   ▒▒ ▒▒▒▒   ▒▒ ▒▒  ▒▒  
▒▒      ▒▒▒▒▒▒  ▒▒▒▒▒▒▒ ▒▒ ▒▒  ▒▒ ▒▒▒▒▒   
▓▓      ▓▓   ▓▓ ▓▓   ▓▓ ▓▓  ▓▓ ▓▓ ▓▓  ▓▓  
 ██████ ██   ██ ██   ██ ██   ████ ██   ██ 

 █▀▄ ▄▀▄ █ █ ▀█▀ ██▀ █▀▄   █▀ █ █▄ █ █▀▄ ██▀ █▀▄
 █▀▄ ▀▄▀ ▀▄█  █  █▄▄ █▀▄   █▀ █ █ ▀█ █▄▀ █▄▄ █▀▄

    """
    print(banner)

def get_country_codes():
    print("Enter country codes separated by commas (US,RU,CN).")
    print("Examples: CN,IN,US,ID,PK,BR,NG,BD,RU,MX")
    codes = input("Country codes (ex: US,RU,CN): ")
    return codes.split(',')

def search_routers(api_key, countries):
    # Initialize the Shodan API client
    api = shodan.Shodan(api_key)

    try:
        # Build the Shodan search query with country filter
        query = 'product:"*router*"'
        if countries:
            query += ' country:{}'.format(','.join(countries))

        # Perform a Shodan search based on the query
        results = api.search(query)

        # Create a dictionary to store router brands and their counts
        router_brands = defaultdict(list)

        # Iterate through the results
        for result in results['matches']:
            # Extract the product field, which typically contains the router brand
            product = result.get('product', 'Unknown')
            # Append the IP address and port to the router brand
            router_brands[product].append((result['ip_str'], result['port']))

        # Display router brands, counts, and associated IP addresses and ports
        for brand, ip_port_list in sorted(router_brands.items(), key=lambda x: len(x[1]), reverse=True):
            print(colored(f"{brand}: {len(ip_port_list)} found", 'green'))
            print("List of IP addresses and ports:")
            for ip, port in ip_port_list:
                print(f"IP: {ip}, Port: {port}")
            print("-----")

        # Display the top 3 brands by count
        top_brands = Counter({brand: len(ip_port_list) for brand, ip_port_list in router_brands.items()})
        print(colored("Top 3 Brands by Count:", 'red'))
        for brand, count in top_brands.most_common(3):
            print(colored(f"{brand}: {count}", 'red'))

    except shodan.APIError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    print_banner()
    if API_KEY == 'YOUR_API_KEY':
        print("Please set your Shodan API key.")
    else:
        target_countries = get_country_codes()
        search_routers(API_KEY, target_countries)

