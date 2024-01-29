import requests
import json


def get_aws_service_pricing(service_code, region='eu-west-1'):
    url = f'https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/{service_code}/current/{region}/index.json'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching data for {service_code}: HTTP {response.status_code}")
        return
    try:
        pricing_data = response.json()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for {service_code}: {e}")
        return
    # Define product family for each service
    product_families = {
        'AmazonRDS': 'Database Instance',
        'AmazonES': 'Amazon OpenSearch Service Instance',
        'AmazonEC2': 'Compute Instance',
        'AmazonElastiCache': 'Cache Instance'
    }
    product_family = product_families.get(service_code, 'Unknown')
    for sku, details in pricing_data['products'].items():
        if 'productFamily' in details and details['productFamily'] == product_family:
            attributes = details['attributes']
            instance_type = attributes.get('instanceType')
            if instance_type:
                for term_type in pricing_data['terms']:
                    for term in pricing_data['terms'][term_type].get(sku, {}).values():
                        for price_data in term['priceDimensions'].values():
                            price_per_hour = price_data['pricePerUnit']['USD']
                            if term_type != 'OnDemand':
                                term_attributes = term['termAttributes']
                                lease_contract_length = term_attributes.get('LeaseContractLength')
                                offering_class = term_attributes.get('OfferingClass')
                                purchase_option = term_attributes.get('PurchaseOption')
                                print(
                                    f'Service: {service_code}, Term Type: {term_type}, Instance Type: {instance_type}, '
                                    f'Contract Length: {lease_contract_length}, Offering Class: {offering_class}, '
                                    f'Purchase Option: {purchase_option}, Reservation: {term_type}, '
                                    f'Price per hour: ${price_per_hour}')
                            else:
                                print(
                                    f'Service: {service_code}, Term Type: {term_type}, Instance Type: {instance_type}, '
                                    f'Reservation: {term_type}, Price per hour: ${price_per_hour}')


def main():
    services = ['AmazonRDS', 'AmazonES', 'AmazonEC2', 'AmazonElastiCache']
    region = 'eu-west-1'  # You can change the region as needed
    for service in services:
        print(f"Fetching pricing for {service} in region {region}...")
        get_aws_service_pricing(service, region)
        print("\n")


if __name__ == "__main__":
    main()
