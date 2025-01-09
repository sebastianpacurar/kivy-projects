from backend.countries_project.rest_countries import CountriesApi

subregions = ['Antarctic', 'Caribbean', 'Western Europe', 'Western Africa', 'Central Europe', 'Eastern Asia', 'Polynesia', 'Northern Africa', 'Southern Europe', 'South-Eastern Asia', 'Eastern Africa', 'Southern Africa', 'North America',
              'Middle Africa', 'Micronesia', 'Southeast Europe', 'Western Asia', 'Northern Europe', 'Melanesia', 'Central Asia', 'Southern Asia', 'South America', 'Australia and New Zealand', 'Central America', 'Eastern Europe']

regions = ['Antarctic', 'Americas', 'Africa', 'Europe', 'Asia', 'Oceania']

raw_languages = {'afr': 'Afrikaans', 'amh': 'Amharic', 'ara': 'Arabic', 'arc': 'Aramaic', 'aym': 'Aymara', 'aze': 'Azerbaijani', 'bel': 'Belarusian', 'ben': 'Bengali', 'ber': 'Berber', 'bis': 'Bislama', 'bjz': 'Belizean Creole',
                 'bos': 'Bosnian', 'bul': 'Bulgarian', 'bwg': 'Chibarwe', 'cal': 'Carolinian', 'cat': 'Catalan', 'ces': 'Czech', 'cha': 'Chamorro', 'ckb': 'Sorani', 'cnr': 'Montenegrin', 'crs': 'Seychellois Creole', 'dan': 'Danish',
                 'de': 'German', 'deu': 'German', 'div': 'Maldivian', 'dzo': 'Dzongkha', 'ell': 'Greek', 'eng': 'English', 'est': 'Estonian', 'eus': 'Basque', 'fao': 'Faroese', 'fas': 'Persian (Farsi)', 'fij': 'Fijian', 'fil': 'Filipino',
                 'fin': 'Finnish', 'fra': 'French', 'gil': 'Gilbertese', 'glc': 'Galician', 'gle': 'Irish', 'glv': 'Manx', 'grn': 'Guaraní', 'gsw': 'Swiss German', 'hat': 'Haitian Creole', 'heb': 'Hebrew', 'her': 'Herero',
                 'hgm': 'Khoekhoe', 'hif': 'Fiji Hindi', 'hin': 'Hindi', 'hmo': 'Hiri Motu', 'hrv': 'Croatian', 'hun': 'Hungarian', 'hye': 'Armenian', 'ind': 'Indonesian', 'isl': 'Icelandic', 'ita': 'Italian', 'jam': 'Jamaican Patois',
                 'jpn': 'Japanese',
                 'kal': 'Greenlandic', 'kat': 'Georgian', 'kaz': 'Kazakh', 'kck': 'Kalanga', 'khi': 'Khoisan', 'khm': 'Khmer', 'kin': 'Kinyarwanda', 'kir': 'Kyrgyz', 'kon': 'Kikongo', 'kor': 'Korean', 'kwn': 'Kwangali', 'lao': 'Lao',
                 'lat': 'Latin', 'lav': 'Latvian', 'lin': 'Lingala', 'lit': 'Lithuanian', 'loz': 'Lozi', 'ltz': 'Luxembourgish', 'lua': 'Tshiluba', 'mah': 'Marshallese', 'mey': 'Hassaniya', 'mfe': 'Mauritian Creole', 'mkd': 'Macedonian',
                 'mlg': 'Malagasy', 'mlt': 'Maltese', 'mon': 'Mongolian', 'mri': 'Māori', 'msa': 'Malay', 'mya': 'Burmese', 'nau': 'Nauru', 'nbl': 'Southern Ndebele', 'ndc': 'Ndau', 'nde': 'Northern Ndebele', 'ndo': 'Ndonga',
                 'nep': 'Nepali',
                 'nfr': 'Guernésiais', 'niu': 'Niuean', 'nld': 'Dutch', 'nno': 'Norwegian Nynorsk', 'nob': 'Norwegian Bokmål', 'nor': 'Norwegian', 'nrf': 'Jèrriais', 'nso': 'Northern Sotho', 'nya': 'Chewa',
                 'nzs': 'New Zealand Sign Language',
                 'pap': 'Papiamento', 'pau': 'Palauan', 'pih': 'Norfuk', 'pol': 'Polish', 'por': 'Portuguese', 'pov': 'Upper Guinea Creole', 'prs': 'Dari', 'pus': 'Pashto', 'que': 'Quechua', 'rar': 'Cook Islands Māori', 'roh': 'Romansh',
                 'ron': 'Romanian', 'run': 'Kirundi', 'rus': 'Russian', 'sag': 'Sango', 'sin': 'Sinhala', 'slk': 'Slovak', 'slv': 'Slovene', 'smi': 'Sami', 'smo': 'Samoan', 'sna': 'Shona', 'som': 'Somali', 'sot': 'Sotho', 'spa': 'Spanish',
                 'sqi': 'Albanian', 'srp': 'Serbian', 'ssw': 'Swazi', 'swa': 'Swahili', 'swe': 'Swedish', 'tam': 'Tamil', 'tet': 'Tetum', 'tgk': 'Tajik', 'tha': 'Thai', 'tir': 'Tigrinya', 'tkl': 'Tokelauan', 'toi': 'Tonga', 'ton': 'Tongan',
                 'tpi': 'Tok Pisin', 'tsn': 'Tswana', 'tso': 'Tsonga', 'tuk': 'Turkmen', 'tur': 'Turkish', 'tvl': 'Tuvaluan', 'ukr': 'Ukrainian', 'urd': 'Urdu', 'uzb': 'Uzbek', 'ven': 'Venda', 'vie': 'Vietnamese', 'xho': 'Xhosa',
                 'zdj': 'Comorian', 'zho': 'Chinese', 'zib': 'Zimbabwean Sign Language', 'zul': 'Zulu'}

raw_currencies = {
    "AED": {"name": "United Arab Emirates dirham", "symbol": "د.إ"},
    "AFN": {"name": "Afghan afghani", "symbol": "؋"},
    "ALL": {"name": "Albanian lek", "symbol": "L"},
    "AMD": {"name": "Armenian dram", "symbol": "֏"},
    "ANG": {"name": "Netherlands Antillean guilder", "symbol": "ƒ"},
    "AOA": {"name": "Angolan kwanza", "symbol": "Kz"},
    "ARS": {"name": "Argentine peso", "symbol": "$"},
    "AUD": {"name": "Australian dollar", "symbol": "$"},
    "AWG": {"name": "Aruban florin", "symbol": "ƒ"},
    "AZN": {"name": "Azerbaijani manat", "symbol": "₼"},
    "BAM": {"name": "Bosnia and Herzegovina convertible mark", "symbol": "KM"},
    "BBD": {"name": "Barbadian dollar", "symbol": "$"},
    "BDT": {"name": "Bangladeshi taka", "symbol": "৳"},
    "BGN": {"name": "Bulgarian lev", "symbol": "лв"},
    "BHD": {"name": "Bahraini dinar", "symbol": ".د.ب"},
    "BIF": {"name": "Burundian franc", "symbol": "Fr"},
    "BMD": {"name": "Bermudian dollar", "symbol": "$"},
    "BND": {"name": "Brunei dollar", "symbol": "$"},
    "BOB": {"name": "Bolivian boliviano", "symbol": "Bs."},
    "BRL": {"name": "Brazilian real", "symbol": "R$"},
    "BSD": {"name": "Bahamian dollar", "symbol": "$"},
    "BTN": {"name": "Bhutanese ngultrum", "symbol": "Nu."},
    "BWP": {"name": "Botswana pula", "symbol": "P"},
    "BYN": {"name": "Belarusian ruble", "symbol": "Br"},
    "BZD": {"name": "Belize dollar", "symbol": "$"},
    "CAD": {"name": "Canadian dollar", "symbol": "$"},
    "CDF": {"name": "Congolese franc", "symbol": "FC"},
    "CHF": {"name": "Swiss franc", "symbol": "Fr"},
    "CKD": {"name": "Cook Islands dollar", "symbol": "$"},
    "CLP": {"name": "Chilean peso", "symbol": "$"},
    "CNY": {"name": "Chinese yuan", "symbol": "¥"},
    "COP": {"name": "Colombian peso", "symbol": "$"},
    "CRC": {"name": "Costa Rican colón", "symbol": "₡"},
    "CUC": {"name": "Cuban convertible peso", "symbol": "$"},
    "CUP": {"name": "Cuban peso", "symbol": "$"},
    "CVE": {"name": "Cape Verdean escudo", "symbol": "Esc"},
    "CZK": {"name": "Czech koruna", "symbol": "Kč"},
    "DJF": {"name": "Djiboutian franc", "symbol": "Fr"},
    "DKK": {"name": "Danish krone", "symbol": "kr"},
    "DOP": {"name": "Dominican peso", "symbol": "$"},
    "DZD": {"name": "Algerian dinar", "symbol": "دج"},
    "EGP": {"name": "Egyptian pound", "symbol": "E£"},
    "ERN": {"name": "Eritrean nakfa", "symbol": "Nfk"},
    "ETB": {"name": "Ethiopian birr", "symbol": "Br"},
    "EUR": {"name": "Euro", "symbol": "€"},
    "FJD": {"name": "Fijian dollar", "symbol": "$"},
    "FKP": {"name": "Falkland Islands pound", "symbol": "£"},
    "FOK": {"name": "Faroese króna", "symbol": "kr"},
    "GBP": {"name": "British pound", "symbol": "£"},
    "GEL": {"name": "lari", "symbol": "₾"},
    "GGP": {"name": "Guernsey pound", "symbol": "£"},
    "GHS": {"name": "Ghanaian cedi", "symbol": "₵"},
    "GIP": {"name": "Gibraltar pound", "symbol": "£"},
    "GMD": {"name": "dalasi", "symbol": "D"},
    "GNF": {"name": "Guinean franc", "symbol": "Fr"},
    "GTQ": {"name": "Guatemalan quetzal", "symbol": "Q"},
    "GYD": {"name": "Guyanese dollar", "symbol": "$"},
    "HKD": {"name": "Hong Kong dollar", "symbol": "$"},
    "HNL": {"name": "Honduran lempira", "symbol": "L"},
    "HTG": {"name": "Haitian gourde", "symbol": "G"},
    "HUF": {"name": "Hungarian forint", "symbol": "Ft"},
    "IDR": {"name": "Indonesian rupiah", "symbol": "Rp"},
    "ILS": {"name": "Israeli new shekel", "symbol": "₪"},
    "IMP": {"name": "Manx pound", "symbol": "£"},
    "INR": {"name": "Indian rupee", "symbol": "₹"},
    "IQD": {"name": "Iraqi dinar", "symbol": "ع.د"},
    "IRR": {"name": "Iranian rial", "symbol": "﷼"},
    "ISK": {"name": "Icelandic króna", "symbol": "kr"},
    "JEP": {"name": "Jersey pound", "symbol": "£"},
    "JMD": {"name": "Jamaican dollar", "symbol": "$"},
    "JOD": {"name": "Jordanian dinar", "symbol": "د.ا"},
    "JPY": {"name": "Japanese yen", "symbol": "¥"},
    "KES": {"name": "Kenyan shilling", "symbol": "Sh"},
    "KGS": {"name": "Kyrgyzstani som", "symbol": "с"},
    "KHR": {"name": "Cambodian riel", "symbol": "៛"},
    "KID": {"name": "Kiribati dollar", "symbol": "$"},
    "KMF": {"name": "Comorian franc", "symbol": "Fr"},
    "KPW": {"name": "North Korean won", "symbol": "₩"},
    "KRW": {"name": "South Korean won", "symbol": "₩"},
    "KWD": {"name": "Kuwaiti dinar", "symbol": "د.ك"},
    "KYD": {"name": "Cayman Islands dollar", "symbol": "$"},
    "KZT": {"name": "Kazakhstani tenge", "symbol": "₸"},
    "LAK": {"name": "Lao kip", "symbol": "₭"},
    "LBP": {"name": "Lebanese pound", "symbol": "ل.ل"},
    "LKR": {"name": "Sri Lankan rupee", "symbol": "Rs  රු"},
    "LRD": {"name": "Liberian dollar", "symbol": "$"},
    "LSL": {"name": "Lesotho loti", "symbol": "L"},
    "LYD": {"name": "Libyan dinar", "symbol": "ل.د"},
    "MAD": {"name": "Moroccan dirham", "symbol": "DH"},
    "MDL": {"name": "Moldovan leu", "symbol": "L"},
    "MGA": {"name": "Malagasy ariary", "symbol": "Ar"},
    "MKD": {"name": "denar", "symbol": "den"},
    "MMK": {"name": "Burmese kyat", "symbol": "Ks"},
    "MNT": {"name": "Mongolian tögrög", "symbol": "₮"},
    "MOP": {"name": "Macanese pataca", "symbol": "P"},
    "MRU": {"name": "Mauritanian ouguiya", "symbol": "UM"},
    "MUR": {"name": "Mauritian rupee", "symbol": "₨"},
    "MVR": {"name": "Maldivian rufiyaa", "symbol": ".ރ"},
    "MWK": {"name": "Malawian kwacha", "symbol": "MK"},
    "MXN": {"name": "Mexican peso", "symbol": "$"},
    "MYR": {"name": "Malaysian ringgit", "symbol": "RM"},
    "MZN": {"name": "Mozambican metical", "symbol": "MT"},
    "NAD": {"name": "Namibian dollar", "symbol": "$"},
    "NGN": {"name": "Nigerian naira", "symbol": "₦"},
    "NIO": {"name": "Nicaraguan córdoba", "symbol": "C$"},
    "NOK": {"name": "Norwegian krone", "symbol": "kr"},
    "NPR": {"name": "Nepalese rupee", "symbol": "₨"},
    "NZD": {"name": "New Zealand dollar", "symbol": "$"},
    "OMR": {"name": "Omani rial", "symbol": "ر.ع."},
    "PAB": {"name": "Panamanian balboa", "symbol": "B/."},
    "PEN": {"name": "Peruvian sol", "symbol": "S/ "},
    "PGK": {"name": "Papua New Guinean kina", "symbol": "K"},
    "PHP": {"name": "Philippine peso", "symbol": "₱"},
    "PKR": {"name": "Pakistani rupee", "symbol": "₨"},
    "PLN": {"name": "Polish złoty", "symbol": "zł"},
    "PYG": {"name": "Paraguayan guaraní", "symbol": "₲"},
    "QAR": {"name": "Qatari riyal", "symbol": "ر.ق"},
    "RON": {"name": "Romanian leu", "symbol": "lei"},
    "RSD": {"name": "Serbian dinar", "symbol": "дин."},
    "RUB": {"name": "Russian ruble", "symbol": "₽"},
    "RWF": {"name": "Rwandan franc", "symbol": "Fr"},
    "SAR": {"name": "Saudi riyal", "symbol": "ر.س"},
    "SBD": {"name": "Solomon Islands dollar", "symbol": "$"},
    "SCR": {"name": "Seychellois rupee", "symbol": "₨"},
    "SDG": {"name": "Sudanese pound", "symbol": "ج.س"},
    "SEK": {"name": "Swedish krona", "symbol": "kr"},
    "SGD": {"name": "Singapore dollar", "symbol": "$"},
    "SHP": {"name": "Saint Helena pound", "symbol": "£"},
    "SLL": {"name": "Sierra Leonean leone", "symbol": "Le"},
    "SOS": {"name": "Somali shilling", "symbol": "Sh"},
    "SRD": {"name": "Surinamese dollar", "symbol": "$"},
    "SSP": {"name": "South Sudanese pound", "symbol": "£"},
    "STN": {"name": "São Tomé and Príncipe dobra", "symbol": "Db"},
    "SYP": {"name": "Syrian pound", "symbol": "£"},
    "SZL": {"name": "Swazi lilangeni", "symbol": "L"},
    "THB": {"name": "Thai baht", "symbol": "฿"},
    "TJS": {"name": "Tajikistani somoni", "symbol": "ЅМ"},
    "TMT": {"name": "Turkmenistan manat", "symbol": "m"},
    "TND": {"name": "Tunisian dinar", "symbol": "د.ت"},
    "TOP": {"name": "Tongan paʻanga", "symbol": "T$"},
    "TRY": {"name": "Turkish lira", "symbol": "₺"},
    "TTD": {"name": "Trinidad and Tobago dollar", "symbol": "$"},
    "TVD": {"name": "Tuvaluan dollar", "symbol": "$"},
    "TWD": {"name": "New Taiwan dollar", "symbol": "$"},
    "TZS": {"name": "Tanzanian shilling", "symbol": "Sh"},
    "UAH": {"name": "Ukrainian hryvnia", "symbol": "₴"},
    "UGX": {"name": "Ugandan shilling", "symbol": "Sh"},
    "USD": {"name": "United States dollar", "symbol": "$"},
    "UYU": {"name": "Uruguayan peso", "symbol": "$"},
    "UZS": {"name": "Uzbekistani soʻm", "symbol": "so'm"},
    "VES": {"name": "Venezuelan bolívar soberano", "symbol": "Bs.S."},
    "VND": {"name": "Vietnamese đồng", "symbol": "₫"},
    "VUV": {"name": "Vanuatu vatu", "symbol": "Vt"},
    "WST": {"name": "Samoan tālā", "symbol": "$"},
    "XAF": {"name": "CFA franc (Central Africa)", "symbol": "Fr"},
    "XCD": {"name": "East Caribbean dollar", "symbol": "$"},
    "XOF": {"name": "CFA franc (West Africa)", "symbol": "Fr"},
    "XPF": {"name": "CFP franc", "symbol": "Fr"},
    "YER": {"name": "Yemeni rial", "symbol": "ر.ي"},
    "ZAR": {"name": "South African rand", "symbol": "R"},
    "ZMK": {"name": "Zambian kwacha", "symbol": "K"},
    "ZWL": {"name": "Zimbabwean dollar", "symbol": "$"}
}

"""
  formatted_currencies example: {
    "AED": "[AED] United Arab Emirates dirham",
    "ALL": "[ALL] Albanian lek",
    ...
    }
"""
formatted_currencies = {k: f"{v['name']} [{k}]" for k, v in sorted(raw_currencies.items(), key=lambda item: item[1]['name'])}
formatted_currencies = {'all': 'All', **formatted_currencies}

sorted_languages = {k: v for k, v in sorted(raw_languages.items(), key=lambda item: item[1])}
sorted_languages = {'all': 'All', **sorted_languages}


def get_all_currencies():
    # example: {'currencies': {'GBP': {'name': 'British pound', 'symbol': '£'}, 'GGP': {'name': 'Guernsey pound', 'symbol': '£'}}}
    data = CountriesApi().get_countries_data(['currencies'], debug=True)
    currencies_dict = {}
    for i in data:
        curr_currency = i['currencies']
        for k, v in curr_currency.items():
            currencies_dict.update({k: v})
    print(currencies_dict)


def get_all_languages():
    # example: {'languages': {'fra': 'French', 'gsw': 'Swiss German', 'ita': 'Italian', 'roh': 'Romansh'}}
    data = CountriesApi().get_countries_data(['languages'], debug=True)
    langs_dict = {}
    for i in data:
        curr_lang = i['languages']
        for k, v in curr_lang.items():
            langs_dict.update({k: v})
    print(langs_dict)


def get_all_regions():
    data = CountriesApi().get_countries_data(['region'], debug=True)
    reg = set()
    for i in data:
        reg.add(i['region'])
    print(list(reg))


def get_all_subregions():
    data = CountriesApi().get_countries_data(['subregion'], debug=True)
    subreg = set()
    for i in data:
        subreg.add(i['subregion'])
    print(list(subreg))


if __name__ == '__main__':
    get_all_currencies()
    get_all_languages()
    get_all_regions()
    get_all_subregions()
