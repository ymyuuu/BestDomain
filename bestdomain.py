import os
import requests

def get_ip_list(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.strip().split('\n')

def get_cloudflare_zone(api_token):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    response = requests.get('https://api.cloudflare.com/client/v4/zones', headers=headers)
    response.raise_for_status()
    zones = response.json().get('result', [])
    if not zones:
        raise Exception("No zones found")
    return zones[0]['id'], zones[0]['name']

def delete_existing_dns_records(api_token, zone_id, subdomain, domain):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    record_name = domain if subdomain == '@' else f'{subdomain}.{domain}'
    while True:
        response = requests.get(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={record_name}', headers=headers)
        response.raise_for_status()
        records = response.json().get('result', [])
        if not records:
            break
        for record in records:
            delete_response = requests.delete(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record["id"]}', headers=headers)
            delete_response.raise_for_status()
            print(f"Del {subdomain}:{record['id']}")

def update_cloudflare_dns(ip_list, api_token, zone_id, subdomain, domain):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }
    record_name = domain if subdomain == '@' else f'{subdomain}.{domain}'
    for ip in ip_list:
        data = {
            "type": "A",
            "name": record_name,
            "content": ip,
            "ttl": 1,
            "proxied": False
        }
        response = requests.post(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records', json=data, headers=headers)
        if response.status_code == 200:
            print(f"Add {subdomain}:{ip}")
        else:
            print(f"Failed to add A record for IP {ip} to subdomain {subdomain}: {response.status_code} {response.text}")

if __name__ == "__main__":
    api_token = os.getenv('CF_API_TOKEN')
    
    # 示例URL和子域名对应的IP列表
    subdomain_ip_mapping = {
        'bestcf': 'https://ipdb.030101.xyz/api/bestcf.txt',
        'bestproxy': 'https://ipdb.030101.xyz/api/bestproxy.txt',
        # 添加更多子域名和对应的IP列表URL
    }
    
    try:
        # 获取Cloudflare域区ID和域名
        zone_id, domain = get_cloudflare_zone(api_token)
        
        for subdomain, url in subdomain_ip_mapping.items():
            # 获取IP列表
            ip_list = get_ip_list(url)
            # 删除现有的DNS记录
            delete_existing_dns_records(api_token, zone_id, subdomain, domain)
            # 更新Cloudflare DNS记录
            update_cloudflare_dns(ip_list, api_token, zone_id, subdomain, domain)
            
    except Exception as e:
        print(f"Error: {e}")
