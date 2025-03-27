import requests
import os

PROPERTIES_API = os.getenv("PROPERTIES_API")

def fetch_houses():
    url = f"{PROPERTIES_API}"
    headers = {
        "authority": os.getenv('AUTHORITY'),
        "accept":  os.getenv('ACCEPT'),
        "accept-language": "en-US,en;q=0.7",
        "distinct-id": os.getenv('DISTINCT_ID'),
        "domain": os.getenv('DOMAIN'),
        "origin": os.getenv('ORIGIN'),
        "priority": "u=1, i",
        "referer": os.getenv('REFERER'),
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
        "sec-ch-ua-mobile": os.getenv('SEC_CH_UA_MOBILE'),
        "sec-ch-ua-platform": os.getenv('SEC_CH_UA_PLATFORM'),
        "sec-fetch-dest": os.getenv('SEC_FETCH_DEST'),
        "sec-fetch-mode": os.getenv('SEC_FETCH_MODE'),
        "sec-fetch-site": os.getenv('SEC_FETCH_SITE'),
        "sec-gpc": os.getenv('SEC_GPC'),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch data", "status_code": response.status_code}
    
    response = response.json()
    property_data = []

    for property in response['results']:
        listing_type = property.get('listing_type', [{}])[0].get('listing', '')
        if listing_type == 'Venta':
            property_info = {
                "name": property.get("name"),
                "category_name": property.get("category", {}).get("name"),
                "room": property.get("room"),
                "bathroom": property.get("bathroom"),
                "half_bathrooms": property.get("half_bathrooms"),
                "parkinglot": property.get("parkinglot"),
                "listing_type": listing_type,
                "featured_image": property.get("featured_image"),
                "currency_sale": property.get("currency_sale"),
                "sale_price": property.get("sale_price"),
                "property_area": property.get("property_area"),
                "property_area_measurer": property.get("property_area_measurer"),
                "province": property.get("province"),
                "city": property.get("city"),
                "sector": property.get("sector")
            }
            property_data.append(property_info)
    
    return {"data": property_data, "status_code": 200}