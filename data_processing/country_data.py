'''
Generates dictionary to map from country code to continent.
Adapted from https://gist.github.com/pamelafox/986163
'''


def get_country_to_continent_map():
    code_to_continent = {
        'BD': 'Asia', 'BE': 'Europe', 'BF': 'Africa', 'BG': 'Europe', 'BA': 'Europe', 
        'BB': 'North America', 'BN': 'Asia', 'BO': 'South America', 'BH': 'Asia', 
        'BI': 'Africa', 'BJ': 'Africa', 'BT': 'Asia', 'JM': 'North America', 'BW': 'Africa',
         'WS': 'Oceania', 'BR': 'South America', 'BS': 'North America', 'BY': 'Europe', 
         'BZ': 'North America', 'RU': 'Europe', 'RW': 'Africa', 'RS': 'Europe', 'TL': 'Asia',
         'TM': 'Asia', 'TJ': 'Asia', 'RO': 'Europe', 'GW': 'Africa', 'GT': 'North America', 
         'GR': 'Europe', 'GQ': 'Africa', 'JP': 'Asia', 'GY': 'South America', 'GE': 'Asia', 
         'GD': 'North America', 'GB': 'Europe', 'GA': 'Africa', 'GN': 'Africa', 'GM': 'Africa',
         'GH': 'Africa', 'OM': 'Asia', 'TN': 'Africa', 'JO': 'Asia', 'HR': 'Europe', 
         'HU': 'Europe', 'HN': 'North America', 'VE': 'South America', 'PW': 'Oceania',
         'PT': 'Europe', 'KN': 'North America', 'PY': 'South America', 'PA': 'North America',
         'PG': 'Oceania', 'PE': 'South America', 'PK': 'Asia', 'PH': 'Asia', 'PL': 'Europe',
         'ZM': 'Africa', 'EE': 'Europe', 'EG': 'Africa', 'ZA': 'Africa', 'EC': 'South America',
         'IT': 'Europe', 'VN': 'Asia', 'KZ': 'Asia', 'ET': 'Africa', 'SO': 'Africa', 
         'ZW': 'Africa', 'ES': 'Europe', 'ER': 'Africa', 'ME': 'Europe', 'MD': 'Europe',
         'MG': 'Africa', 'UY': 'South America', 'MC': 'Europe', 'UZ': 'Asia', 'MM': 'Asia',
         'ML': 'Africa', 'MN': 'Asia', 'MH': 'Oceania', 'MK': 'Europe', 'MU': 'Africa', 
         'MT': 'Europe', 'MW': 'Africa', 'MV': 'Asia', 'MR': 'Africa', 'UG': 'Africa', 
         'MY': 'Asia', 'MX': 'North America', 'IL': 'Asia', 'FR': 'Europe', 'MA': 'Africa',
         'FI': 'Europe', 'FJ': 'Oceania', 'FM': 'Oceania', 'NI': 'North America', 
         'NL': 'Europe', 'NO': 'Europe', 'NA': 'Africa', 'VU': 'Oceania', 'NE': 'Africa',
         'NG': 'Africa', 'NZ': 'Oceania', 'NP': 'Asia', 'NR': 'Oceania', 'CI': 'Africa', 
         'CH': 'Europe', 'CO': 'South America', 'CN': 'Asia', 'CM': 'Africa', 
         'CL': 'South America', 'CA': 'North America', 'CG': 'Africa', 'CF': 'Africa', 
         'CD': 'Africa', 'CZ': 'Europe', 'CY': 'Asia', 'CR': 'North America',
         'CV': 'Africa', 'CU': 'North America', 'SZ': 'Africa', 'SY': 'Asia', 
         'KG': 'Asia', 'KE': 'Africa', 'SR': 'South America', 'KI': 'Oceania',
         'KH': 'Asia', 'SV': 'North America', 'KM': 'Africa', 'ST': 'Africa', 
         'SK': 'Europe', 'KR': 'Asia', 'SI': 'Europe', 'KP': 'Asia', 'KW': 'Asia', 
         'SN': 'Africa', 'SM': 'Europe', 'SL': 'Africa', 'SC': 'Africa', 'SB': 'Oceania',
         'SA': 'Asia', 'SG': 'Asia', 'SE': 'Europe', 'SD': 'Africa', 'DO': 'North America',
         'DM': 'North America', 'DJ': 'Africa', 'DK': 'Europe', 'DE': 'Europe', 
         'YE': 'Asia', 'DZ': 'Africa', 'US': 'North America', 'LB': 'Asia', 
         'LC': 'North America', 'LA': 'Asia', 'TV': 'Oceania', 'TT': 'North America',
         'TR': 'Asia', 'LK': 'Asia', 'LI': 'Europe', 'LV': 'Europe', 'TO': 'Oceania',
         'LT': 'Europe', 'LU': 'Europe', 'LR': 'Africa', 'LS': 'Africa', 'TH': 'Asia', 
         'TG': 'Africa', 'TD': 'Africa', 'LY': 'Africa', 'VA': 'Europe', 
         'VC': 'North America', 'AE': 'Asia', 'AD': 'Europe', 'AG': 'North America',
         'AF': 'Asia', 'IQ': 'Asia', 'IS': 'Europe', 'IR': 'Asia', 'AM': 'Asia', 
         'AL': 'Europe', 'AO': 'Africa', 'AR': 'South America', 'AU': 'Oceania', 
         'AT': 'Europe', 'IN': 'Asia', 'TZ': 'Africa', 'AZ': 'Asia', 'IE': 'Europe', 
         'ID': 'Asia', 'UA': 'Europe', 'QA': 'Asia', 'MZ': 'Africa', 'UK': 'Europe',
         'BX': 'Oceania', 'SW': 'Europe', 'PO': 'Europe', 'SP': 'Europe'}
    return code_to_continent
