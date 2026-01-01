"""
Complete list of Indonesian IDX stocks (January 2026)
This file contains all major stocks traded on Indonesia Stock Exchange
Data sourced from IDX official listings
"""

# IDX-30 (Blue Chip Stocks)
IDX30_STOCKS = {
    "BBCA": {"name": "Bank Central Asia", "sector": "Banking", "board": "Main"},
    "BBRI": {"name": "Bank Rakyat Indonesia", "sector": "Banking", "board": "Main"},
    "BMRI": {"name": "Bank Mandiri", "sector": "Banking", "board": "Main"},
    "BBNI": {"name": "Bank Negara Indonesia", "sector": "Banking", "board": "Main"},
    "ASII": {"name": "Astra International", "sector": "Automotive", "board": "Main"},
    "UNVR": {"name": "Unilever Indonesia", "sector": "Consumer Goods", "board": "Main"},
    "TLKM": {"name": "Telkom Indonesia", "sector": "Telecommunications", "board": "Main"},
    "INDF": {"name": "Indofood Sukses Makmur", "sector": "Consumer Goods", "board": "Main"},
    "ICBP": {"name": "Indofood CBP", "sector": "Consumer Goods", "board": "Main"},
    "INCO": {"name": "Vale Indonesia", "sector": "Mining", "board": "Main"},
    "ANTM": {"name": "Aneka Tambang", "sector": "Mining", "board": "Main"},
    "ADRO": {"name": "Adaro Energy", "sector": "Energy", "board": "Main"},
    "ITMG": {"name": "Indo Tambangraya Megah", "sector": "Mining", "board": "Main"},
    "PTBA": {"name": "Bukit Asam", "sector": "Mining", "board": "Main"},
    "KLBF": {"name": "Kalbe Farma", "sector": "Healthcare", "board": "Main"},
    "GGRM": {"name": "Gudang Garam", "sector": "Consumer Goods", "board": "Main"},
    "HMSP": {"name": "HM Sampoerna", "sector": "Consumer Goods", "board": "Main"},
    "CPIN": {"name": "Charoen Pokphand Indonesia", "sector": "Consumer Goods", "board": "Main"},
    "EXCL": {"name": "XL Axiata", "sector": "Telecommunications", "board": "Main"},
    "PGAS": {"name": "Perusahaan Gas Negara", "sector": "Utilities", "board": "Main"},
    "SMGR": {"name": "Semen Indonesia", "sector": "Construction", "board": "Main"},
    "TOWR": {"name": "Sarana Menara Nusantara", "sector": "Telecommunications", "board": "Main"},
    "MNCN": {"name": "Media Nusantara Citra", "sector": "Media", "board": "Main"},
    "JSMR": {"name": "Jasa Marga", "sector": "Transportation", "board": "Main"},
    "WIKA": {"name": "Wijaya Karya", "sector": "Construction", "board": "Main"},
    "PTPP": {"name": "PP (Persero)", "sector": "Construction", "board": "Main"},
    "AKRA": {"name": "AKR Corporindo", "sector": "Trading", "board": "Main"},
    "EMTK": {"name": "Elang Mahkota Teknologi", "sector": "Media", "board": "Main"},
    "SCMA": {"name": "Surya Citra Media", "sector": "Media", "board": "Main"},
    "BRPT": {"name": "Barito Pacific", "sector": "Basic Materials", "board": "Main"},
}

# LQ45 (Liquid 45 Stocks) - Additional to IDX30
LQ45_ADDITIONAL = {
    "BSDE": {"name": "Bumi Serpong Damai", "sector": "Property", "board": "Main"},
    "CTRA": {"name": "Ciputra Development", "sector": "Property", "board": "Main"},
    "PWON": {"name": "Pakuwon Jati", "sector": "Property", "board": "Main"},
    "LPKR": {"name": "Lippo Karawaci", "sector": "Property", "board": "Main"},
    "SMRA": {"name": "Summarecon Agung", "sector": "Property", "board": "Main"},
    "MAPI": {"name": "Mitra Adiperkasa", "sector": "Retail", "board": "Main"},
    "ACES": {"name": "Ace Hardware Indonesia", "sector": "Retail", "board": "Main"},
    "ERAA": {"name": "Erajaya Swasembada", "sector": "Retail", "board": "Main"},
    "SRIL": {"name": "Sri Rejeki Isman", "sector": "Textile", "board": "Main"},
    "AMRT": {"name": "Sumber Alfaria Trijaya", "sector": "Retail", "board": "Main"},
    "MDKA": {"name": "Merdeka Copper Gold", "sector": "Mining", "board": "Main"},
    "TINS": {"name": "Timah", "sector": "Mining", "board": "Main"},
    "MEDC": {"name": "Medco Energi", "sector": "Energy", "board": "Main"},
    "BYAN": {"name": "Bayan Resources", "sector": "Mining", "board": "Main"},
    "AMMN": {"name": "Amman Mineral", "sector": "Mining", "board": "Main"},
}

# BANKING SECTOR (Complete)
BANKING_STOCKS = {
    "BBCA": {"name": "Bank Central Asia", "sector": "Banking", "board": "Main"},
    "BBRI": {"name": "Bank Rakyat Indonesia", "sector": "Banking", "board": "Main"},
    "BMRI": {"name": "Bank Mandiri", "sector": "Banking", "board": "Main"},
    "BBNI": {"name": "Bank Negara Indonesia", "sector": "Banking", "board": "Main"},
    "BBTN": {"name": "Bank Tabungan Negara", "sector": "Banking", "board": "Main"},
    "BRIS": {"name": "Bank BRI Syariah", "sector": "Banking", "board": "Main"},
    "BJBR": {"name": "Bank Pembangunan Daerah Jawa Barat", "sector": "Banking", "board": "Main"},
    "BJTM": {"name": "Bank Pembangunan Daerah Jawa Timur", "sector": "Banking", "board": "Main"},
    "NISP": {"name": "Bank OCBC NISP", "sector": "Banking", "board": "Main"},
    "PNBN": {"name": "Bank Pan Indonesia", "sector": "Banking", "board": "Main"},
    "BNLI": {"name": "Bank Permata", "sector": "Banking", "board": "Main"},
    "BNGA": {"name": "Bank CIMB Niaga", "sector": "Banking", "board": "Main"},
    "MEGA": {"name": "Bank Mega", "sector": "Banking", "board": "Main"},
    "BTPS": {"name": "Bank BTPN Syariah", "sector": "Banking", "board": "Main"},
    "MAYA": {"name": "Bank Mayapada", "sector": "Banking", "board": "Main"},
    "BACA": {"name": "Bank Capital Indonesia", "sector": "Banking", "board": "Main"},
    "BMAS": {"name": "Bank Maspion Indonesia", "sector": "Banking", "board": "Main"},
    "BNII": {"name": "Bank Maybank Indonesia", "sector": "Banking", "board": "Main"},
}

# MINING & ENERGY (Complete)
MINING_ENERGY_STOCKS = {
    "INCO": {"name": "Vale Indonesia", "sector": "Mining", "board": "Main"},
    "ANTM": {"name": "Aneka Tambang", "sector": "Mining", "board": "Main"},
    "MDKA": {"name": "Merdeka Copper Gold", "sector": "Mining", "board": "Main"},
    "TINS": {"name": "Timah", "sector": "Mining", "board": "Main"},
    "ITMG": {"name": "Indo Tambangraya Megah", "sector": "Mining", "board": "Main"},
    "PTBA": {"name": "Bukit Asam", "sector": "Mining", "board": "Main"},
    "ADRO": {"name": "Adaro Energy", "sector": "Energy", "board": "Main"},
    "BYAN": {"name": "Bayan Resources", "sector": "Mining", "board": "Main"},
    "AMMN": {"name": "Amman Mineral", "sector": "Mining", "board": "Main"},
    "HRUM": {"name": "Harum Energy", "sector": "Mining", "board": "Main"},
    "KKGI": {"name": "Resource Alam Indonesia", "sector": "Mining", "board": "Main"},
    "DOID": {"name": "Delta Dunia Makmur", "sector": "Mining", "board": "Main"},
    "GEMS": {"name": "Golden Energy Mines", "sector": "Mining", "board": "Main"},
    "MEDC": {"name": "Medco Energi", "sector": "Energy", "board": "Main"},
    "ELSA": {"name": "Elnusa", "sector": "Energy", "board": "Main"},
    "PGAS": {"name": "Perusahaan Gas Negara", "sector": "Utilities", "board": "Main"},
    "ENRG": {"name": "Energi Mega Persada", "sector": "Energy", "board": "Main"},
    "RUIS": {"name": "Radiant Utama Interinsco", "sector": "Mining", "board": "Main"},
}

# CONSUMER GOODS (Complete)
CONSUMER_STOCKS = {
    "UNVR": {"name": "Unilever Indonesia", "sector": "Consumer Goods", "board": "Main"},
    "INDF": {"name": "Indofood Sukses Makmur", "sector": "Consumer Goods", "board": "Main"},
    "ICBP": {"name": "Indofood CBP", "sector": "Consumer Goods", "board": "Main"},
    "GGRM": {"name": "Gudang Garam", "sector": "Consumer Goods", "board": "Main"},
    "HMSP": {"name": "HM Sampoerna", "sector": "Consumer Goods", "board": "Main"},
    "CPIN": {"name": "Charoen Pokphand Indonesia", "sector": "Consumer Goods", "board": "Main"},
    "KLBF": {"name": "Kalbe Farma", "sector": "Healthcare", "board": "Main"},
    "KAEF": {"name": "Kimia Farma", "sector": "Healthcare", "board": "Main"},
    "MYOR": {"name": "Mayora Indah", "sector": "Consumer Goods", "board": "Main"},
    "ULTJ": {"name": "Ultra Jaya Milk", "sector": "Consumer Goods", "board": "Main"},
    "MLBI": {"name": "Multi Bintang Indonesia", "sector": "Consumer Goods", "board": "Main"},
    "SIDO": {"name": "Industri Jamu Sido Muncul", "sector": "Healthcare", "board": "Main"},
    "TSPC": {"name": "Tempo Scan Pacific", "sector": "Healthcare", "board": "Main"},
    "DVLA": {"name": "Darya-Varia Laboratoria", "sector": "Healthcare", "board": "Main"},
    "WIIM": {"name": "Wismilak Inti Makmur", "sector": "Consumer Goods", "board": "Main"},
    "ROTI": {"name": "Nippon Indosari Corpindo", "sector": "Consumer Goods", "board": "Main"},
    "GOOD": {"name": "Garudafood Putra Putri Jaya", "sector": "Consumer Goods", "board": "Main"},
    "SKBM": {"name": "Sekar Bumi", "sector": "Consumer Goods", "board": "Main"},
}

# TECHNOLOGY & TELECOMMUNICATIONS
TECH_TELECOM_STOCKS = {
    "TLKM": {"name": "Telkom Indonesia", "sector": "Telecommunications", "board": "Main"},
    "EXCL": {"name": "XL Axiata", "sector": "Telecommunications", "board": "Main"},
    "ISAT": {"name": "Indosat Ooredoo", "sector": "Telecommunications", "board": "Main"},
    "TOWR": {"name": "Sarana Menara Nusantara", "sector": "Telecommunications", "board": "Main"},
    "TBIG": {"name": "Tower Bersama Infrastructure", "sector": "Telecommunications", "board": "Main"},
    "GOTO": {"name": "GoTo Gojek Tokopedia", "sector": "Technology", "board": "Main"},
    "BUKA": {"name": "Bukalapak.com", "sector": "Technology", "board": "Main"},
    "BELI": {"name": "Blibli.com", "sector": "Technology", "board": "Main"},
    "BRIS": {"name": "Bank BRI Syariah", "sector": "Banking", "board": "Main"},
    "FREN": {"name": "Smartfren Telecom", "sector": "Telecommunications", "board": "Main"},
    "LINK": {"name": "Link Net", "sector": "Telecommunications", "board": "Main"},
}

# PROPERTY & CONSTRUCTION
PROPERTY_CONSTRUCTION_STOCKS = {
    "BSDE": {"name": "Bumi Serpong Damai", "sector": "Property", "board": "Main"},
    "CTRA": {"name": "Ciputra Development", "sector": "Property", "board": "Main"},
    "PWON": {"name": "Pakuwon Jati", "sector": "Property", "board": "Main"},
    "LPKR": {"name": "Lippo Karawaci", "sector": "Property", "board": "Main"},
    "SMRA": {"name": "Summarecon Agung", "sector": "Property", "board": "Main"},
    "ASRI": {"name": "Alam Sutera Realty", "sector": "Property", "board": "Main"},
    "APLN": {"name": "Agung Podomoro Land", "sector": "Property", "board": "Main"},
    "DMAS": {"name": "Puradelta Lestari", "sector": "Property", "board": "Main"},
    "PLIN": {"name": "Plaza Indonesia Realty", "sector": "Property", "board": "Main"},
    "BEST": {"name": "Bekasi Fajar Industrial Estate", "sector": "Property", "board": "Main"},
    "SMGR": {"name": "Semen Indonesia", "sector": "Construction", "board": "Main"},
    "WIKA": {"name": "Wijaya Karya", "sector": "Construction", "board": "Main"},
    "PTPP": {"name": "PP (Persero)", "sector": "Construction", "board": "Main"},
    "JSMR": {"name": "Jasa Marga", "sector": "Transportation", "board": "Main"},
    "WSBP": {"name": "Waskita Beton Precast", "sector": "Construction", "board": "Main"},
    "WSKT": {"name": "Waskita Karya", "sector": "Construction", "board": "Main"},
    "ADHI": {"name": "Adhi Karya", "sector": "Construction", "board": "Main"},
    "TOTL": {"name": "Total Bangun Persada", "sector": "Construction", "board": "Main"},
}

# RETAIL & TRADE
RETAIL_STOCKS = {
    "MAPI": {"name": "Mitra Adiperkasa", "sector": "Retail", "board": "Main"},
    "ACES": {"name": "Ace Hardware Indonesia", "sector": "Retail", "board": "Main"},
    "ERAA": {"name": "Erajaya Swasembada", "sector": "Retail", "board": "Main"},
    "AMRT": {"name": "Sumber Alfaria Trijaya", "sector": "Retail", "board": "Main"},
    "LPPF": {"name": "Matahari Department Store", "sector": "Retail", "board": "Main"},
    "RALS": {"name": "Ramayana Lestari Sentosa", "sector": "Retail", "board": "Main"},
    "CSAP": {"name": "Catur Sentosa Adiprana", "sector": "Retail", "board": "Main"},
    "HERO": {"name": "Hero Supermarket", "sector": "Retail", "board": "Main"},
    "AKRA": {"name": "AKR Corporindo", "sector": "Trading", "board": "Main"},
    "UNTR": {"name": "United Tractors", "sector": "Trading", "board": "Main"},
    "ESSA": {"name": "Surya Esa Perkasa", "sector": "Trading", "board": "Main"},
}

# TRANSPORTATION & LOGISTICS
TRANSPORTATION_STOCKS = {
    "JSMR": {"name": "Jasa Marga", "sector": "Transportation", "board": "Main"},
    "GIAA": {"name": "Garuda Indonesia", "sector": "Transportation", "board": "Main"},
    "BIRD": {"name": "Blue Bird", "sector": "Transportation", "board": "Main"},
    "WEHA": {"name": "Weha Transportasi Indonesia", "sector": "Transportation", "board": "Main"},
    "TRAM": {"name": "Trada Alam Minera", "sector": "Transportation", "board": "Main"},
    "BMTR": {"name": "Global Mediacom", "sector": "Transportation", "board": "Main"},
    "SMDR": {"name": "Samudera Indonesia", "sector": "Transportation", "board": "Main"},
}

# MEDIA & ENTERTAINMENT
MEDIA_STOCKS = {
    "MNCN": {"name": "Media Nusantara Citra", "sector": "Media", "board": "Main"},
    "EMTK": {"name": "Elang Mahkota Teknologi", "sector": "Media", "board": "Main"},
    "SCMA": {"name": "Surya Citra Media", "sector": "Media", "board": "Main"},
    "BMTR": {"name": "Global Mediacom", "sector": "Media", "board": "Main"},
}

# Combine all stocks
ALL_IDX_STOCKS = {}
ALL_IDX_STOCKS.update(IDX30_STOCKS)
ALL_IDX_STOCKS.update(LQ45_ADDITIONAL)
ALL_IDX_STOCKS.update(BANKING_STOCKS)
ALL_IDX_STOCKS.update(MINING_ENERGY_STOCKS)
ALL_IDX_STOCKS.update(CONSUMER_STOCKS)
ALL_IDX_STOCKS.update(TECH_TELECOM_STOCKS)
ALL_IDX_STOCKS.update(PROPERTY_CONSTRUCTION_STOCKS)
ALL_IDX_STOCKS.update(RETAIL_STOCKS)
ALL_IDX_STOCKS.update(TRANSPORTATION_STOCKS)
ALL_IDX_STOCKS.update(MEDIA_STOCKS)

# Remove duplicates by converting to dict (will keep last occurrence)
ALL_IDX_STOCKS_UNIQUE = {k: {**v, "is_us": False} for k, v in ALL_IDX_STOCKS.items()}

print(f"Total unique Indonesian stocks: {len(ALL_IDX_STOCKS_UNIQUE)}")
