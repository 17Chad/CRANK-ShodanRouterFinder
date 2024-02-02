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
    print(colored("Enter country codes WITH COMMAS (US,RU,CN).", 'green'))
    print(colored("Examples: CN,IN,US,ID,PK,BR,NG,BD,RU,MX", 'green'))
    codes = input("Country codes (ex: US,RU,CN): ")
    return codes.split(',')

def get_brand_choice():
    print(colored("Enter 'all' to query all routers or specify a brand (ex: all, mikrotik, tp-link, netis):", 'green'))
    brand_choice = input("All routers or a specific brand?: ").strip()
    return brand_choice

def search_routers(api_key, countries, brand_choice):
    # Initialize the Shodan API client
    api = shodan.Shodan(api_key)

    # Adjust the query based on the brand choice
    if brand_choice.lower() == 'all':
        query = 'product:"*router*"'
    else:
        query = f'product:"*{brand_choice}*"'
    
    if countries:
        query += ' country:{}'.format(','.join(countries))

    try:
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
        print(colored("Top 3 by count:", 'red'))
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
        brand_choice = get_brand_choice()  # Capture the brand choice
        search_routers(API_KEY, target_countries, brand_choice)  # Pass the brand choice as an argument

