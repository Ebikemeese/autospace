import logging
import random
from django.db import transaction
from django.conf import settings
from django.contrib.auth.hashers import make_password
from authentication.models import User, UserRole, Admin
from companies.models import Company
from managers.models import Manager
from valets.models import Valet
from garages.models import Garage
from addresses.models import Address
from verification.models import Verification
from slots.models import Slot, SlotType
from services.models import Service
from customers.models import Customer
from reviews.models import Review

logger = logging.getLogger(__name__)

# List of 100 Major Global Cities with Lat/Lng & Address info
CITIES = [
    # North America
    ("New York City", "USA", 40.7128, -74.0060, ["Broadway", "Wall St", "5th Ave", "Madison Ave", "Lexington Ave", "Park Ave", "7th Ave", "Canal St", "42nd St", "Houston St"]),
    ("Los Angeles", "USA", 34.0522, -118.2437, ["Grand Ave", "Wilshire Blvd", "Sunset Blvd", "Hollywood Blvd", "Santa Monica Blvd", "Figueroa St", "Hope St", "Olympic Blvd", "Spring St", "Main St"]),
    ("Chicago", "USA", 41.8781, -87.6298, ["Michigan Ave", "State St", "Wacker Dr", "Clark St", "LaSalle St", "Grand Ave", "Adams St", "Monroe St", "Jackson Blvd", "Randolph St"]),
    ("Houston", "USA", 29.7604, -95.3698, ["Main St", "Texas Ave", "Louisiana St", "Travis St", "Fannin St", "Capitol St", "Walker St", "McKinney St", "Lamar St", "Dallas St"]),
    ("Phoenix", "USA", 33.4484, -112.0740, ["Central Ave", "Washington St", "Jefferson St", "Van Buren St", "Monroe St", "Adams St", "1st Ave", "7th St", "Camelback Rd", "Indian School Rd"]),
    ("Philadelphia", "USA", 39.9526, -75.1652, ["Market St", "Chestnut St", "Walnut St", "Broad St", "Arch St", "Race St", "Spruce St", "Pine St", "Locust St", "JFK Blvd"]),
    ("San Antonio", "USA", 29.4241, -98.4936, ["Houston St", "Commerce St", "Navarro St", "St Mary's St", "Soledad St", "Flores St", "Market St", "Alamo St", "Broadway", "Dolorosa St"]),
    ("San Diego", "USA", 32.7157, -117.1611, ["Broadway", "Harbor Dr", "Pacific Hwy", "4th Ave", "5th Ave", "6th Ave", "C St", "Ash St", "Beech St", "Market St"]),
    ("Dallas", "USA", 32.7767, -96.7970, ["Main St", "Elm St", "Commerce St", "Pacific Ave", "Jackson St", "Wood St", "Akard St", "Ervay St", "St Paul St", "Harwood St"]),
    ("San Jose", "USA", 37.3382, -121.8863, ["First St", "Second St", "Santa Clara St", "San Fernando St", "San Carlos St", "Market St", "Almaden Blvd", "Notre Dame Ave", "Julian St", "St John St"]),
    ("Austin", "USA", 30.2672, -97.7431, ["Congress Ave", "6th St", "Lamar Blvd", "Guadalupe St", "Lavaca St", "Colorado St", "Brazos St", "San Jacinto Blvd", "Trinity St", "Neches St"]),
    ("San Francisco", "USA", 37.7749, -122.4194, ["Market St", "Post St", "Geary St", "Sutter St", "Bush St", "California St", "Pine St", "Sacramento St", "Montgomery St", "Sansome St"]),
    ("Seattle", "USA", 47.6062, -122.3321, ["Pike St", "Pine St", "1st Ave", "2nd Ave", "3rd Ave", "4th Ave", "5th Ave", "Stewart St", "Virginia St", "Lenora St"]),
    ("Miami", "USA", 25.7617, -80.1918, ["Biscayne Blvd", "Flagler St", "Brickell Ave", "SE 1st Ave", "NE 2nd Ave", "Ocean Dr", "Collins Ave", "Washington Ave", "Lincoln Rd", "Alton Rd"]),
    ("Boston", "USA", 42.3601, -71.0589, ["Boylston St", "Newbury St", "Tremont St", "Beacon St", "Washington St", "Congress St", "Atlantic Ave", "State St", "Summer St", "Franklin St"]),
    ("Atlanta", "USA", 33.7490, -84.3880, ["Peachtree St", "Piedmont Ave", "Spring St", "West Peachtree St", "Marietta St", "Decatur St", "Ivan Allen Jr Blvd", "North Ave", "Ponce de Leon Ave", "Baker St"]),
    ("Toronto", "Canada", 43.6532, -79.3832, ["Yonge St", "Bay St", "King St W", "Queen St W", "Front St W", "Adelaide St W", "Richmond St W", "Dundas St W", "University Ave", "Bremner Blvd"]),
    ("Vancouver", "Canada", 49.2827, -123.1207, ["Georgia St", "Robson St", "Burrard St", "Granville St", "Howe St", "Hornby St", "Dunsmuir St", "Pender St", "Hastings St", "Alberni St"]),
    ("Montreal", "Canada", 45.5017, -73.5673, ["Sainte-Catherine St", "Sherbrooke St", "René-Lévesque Blvd", "Saint-Laurent Blvd", "Saint-Denis St", "Peel St", "Crescent St", "Bleury St", "McGill St", "Notre-Dame St"]),
    ("Mexico City", "Mexico", 19.4326, -99.1332, ["Paseo de la Reforma", "Av. Insurgentes", "Av. Juárez", "Calle de Madero", "Av. Hidalgo", "Av. Chapultepec", "Calle Liverpool", "Av. Álvaro Obregón", "Av. Universidad", "Eje Central"]),

    # Europe
    ("London", "UK", 51.5074, -0.1278, ["Oxford St", "Regent St", "Piccadilly", "Strand", "Fleet St", "Baker St", "Bond St", "Mayfair Pl", "Victoria St", "Whitehall"]),
    ("Manchester", "UK", 53.4808, -2.2426, ["Deansgate", "Market St", "Portland St", "Mosley St", "King St", "Cross St", "Corporation St", "Peter St", "Oxford Rd", "Princess St"]),
    ("Birmingham", "UK", 52.4862, -1.8904, ["Corporation St", "New St", "Colmore Row", "Broad St", "Bull St", "Hurst St", "Paradise St", "Suffolk St", "High St", "Digbeth"]),
    ("Edinburgh", "UK", 55.9533, -3.1883, ["Princes St", "George St", "Royal Mile", "Queen St", "Lothian Rd", "Rose St", "Haymarket", "Leith Walk", "Chambers St", "Moray Pl"]),
    ("Paris", "France", 48.8566, 2.3522, ["Champs-Élysées", "Rue de Rivoli", "Boulevard Haussmann", "Boulevard Saint-Germain", "Avenue Montaigne", "Rue Royale", "Rue de la Paix", "Boulevard Sébastopol", "Rue du Faubourg Saint-Honoré", "Avenue de l'Opéra"]),
    ("Lyon", "France", 45.7640, 4.8357, ["Rue de la République", "Rue Édouard Herriot", "Cours Lafayette", "Boulevard Vivier-Merle", "Rue Victor Hugo", "Grande Rue de la Croix-Rousse", "Rue Garibaldi", "Cours Gambetta", "Rue de Brest", "Quai Saint-Antoine"]),
    ("Marseille", "France", 43.2965, 5.3698, ["La Canebière", "Rue Saint-Ferréol", "Rue de Rome", "Boulevard Prado", "Avenue du Prado", "Rue Paradis", "Corniche Kennedy", "Rue de la République", "Cours Julien", "Quai des Belges"]),
    ("Berlin", "Germany", 52.5200, 13.4050, ["Unter den Linden", "Kurfürstendamm", "Friedrichstraße", "Potsdamer Platz", "Karl-Liebknecht-Straße", "Alexanderstraße", "Leipziger Straße", "Schönhauser Allee", "Kastanienallee", "Torstraße"]),
    ("Munich", "Germany", 48.1351, 11.5820, ["Kaufingerstraße", "Maximilianstraße", "Theatinerstraße", "Sendlinger Straße", "Brienner Straße", "Ludwigstraße", "Leopoldstraße", "Sonnenstraße", "Bayerstraße", "Karlsplatz"]),
    ("Frankfurt", "Germany", 50.1109, 8.6821, ["Zeil", "Goethestraße", "Kaiserstraße", "Mainzer Landstraße", "Neue Mainzer Straße", "Taunusanlage", "Bockenheimer Landstraße", "Eschersheimer Landstraße", "Berliner Straße", "Fressgass"]),
    ("Hamburg", "Germany", 53.5511, 9.9937, ["Mönckebergstraße", "Jungfernstieg", "Neuer Wall", "Spitalerstraße", "Reeperbahn", "Wandsbeker Chaussee", "Ballindamm", "Glockengießerwall", "Alsterufer", "Hafencity"]),
    ("Amsterdam", "Netherlands", 52.3676, 4.9041, ["Damrak", "Rokin", "Kalverstraat", "Leidsestraat", "P.C. Hooftstraat", "Prinsengracht", "Keizersgracht", "Herengracht", "Singel", "Overtoom"]),
    ("Rotterdam", "Netherlands", 51.9244, 4.4777, ["Coolsingel", "Lijnbaan", "Weena", "Meent", "Westblaak", "Hoogstraat", "Blaak", "Witte de Withstraat", "Schiedamse Vest", "Van Oldenbarneveltstraat"]),
    ("Brussels", "Belgium", 50.8503, 4.3517, ["Rue Neuve", "Avenue Louise", "Boulevard Anspach", "Rue de la Loi", "Rue Royale", "Boulevard du Régent", "Avenue Montjoie", "Chaussée de Wavre", "Rue Antoine Dansaert", "Place du Grand Sablon"]),
    ("Madrid", "Spain", 40.4168, -3.7038, ["Gran Vía", "Calle de Alcalá", "Paseo de la Castellana", "Paseo del Prado", "Calle de Serrano", "Calle de Velázquez", "Calle de Goya", "Calle de Fuencarral", "Calle Mayor", "Calle de Preciados"]),
    ("Barcelona", "Spain", 41.3851, 2.1734, ["La Rambla", "Passeig de Gràcia", "Avinguda Diagonal", "Rambla de Catalunya", "Gran Via de les Corts Catalanes", "Carrer de Balmes", "Carrer d'Aragó", "Carrer de Mallorca", "Via Laietana", "Carrer de Pelai"]),
    ("Rome", "Italy", 41.9028, 12.4964, ["Via del Corso", "Via Nazionale", "Via del Tritone", "Via Veneto", "Via Condotti", "Via Cola di Rienzo", "Corso Vittorio Emanuele II", "Via Appia Nuova", "Via Casilina", "Via Tiburtina"]),
    ("Milan", "Italy", 45.4642, 9.1900, ["Corso Vittorio Emanuele II", "Via Montenapoleone", "Corso Buenos Aires", "Via Dante", "Corso Como", "Via Torino", "Via Manzoni", "Corso Magenta", "Via Brera", "Via Solferino"]),
    ("Zurich", "Switzerland", 47.3769, 8.5417, ["Bahnhofstrasse", "Rennweg", "Limmatquai", "Lowenstrasse", "Gotthardstrasse", "Bellerivestrasse", "Talstrasse", "Bleicherweg", "Seefeldstrasse", "Stampfenbachstrasse"]),
    ("Vienna", "Austria", 48.2082, 16.3738, ["Kärntner Straße", "Graben", "Mariahilfer Straße", "Ringstraße", "Rotenturmstraße", "Wollzeile", "Herrengasse", "Opernring", "Schottenring", "Favoritenstraße"]),
    ("Copenhagen", "Denmark", 55.6761, 12.5683, ["Strøget", "Vesterbrogade", "Nørrebrogade", "Amagertorv", "Østerbrogade", "Gammel Kongevej", "Bredgade", "Store Kongensgade", "Købmagergade", "Nyhavn"]),
    ("Stockholm", "Sweden", 59.3293, 18.0686, ["Drottninggatan", "Biblioteksgatan", "Hamngatan", "Kungsgatan", "Sveavägen", "Birger Jarlsgatan", "Götgatan", "Hornsgatan", "Odengatan", "Valhallavägen"]),
    ("Oslo", "Norway", 59.9139, 10.7522, ["Karl Johans gate", "Bogstadveien", "Grensen", "Prinsens gate", "Stortingsgata", "Torggata", "Bygdøy allé", "Drammensveien", "Aker Brygge", "Vika"]),
    ("Dublin", "Ireland", 53.3498, -6.2603, ["Grafton St", "Henry St", "O'Connell St", "Nassau St", "Dawson St", "Dame St", "Bagot St", "George's St", "Parnell St", "Capel St"]),
    ("Lisbon", "Portugal", 38.7223, -9.1393, ["Avenida da Liberdade", "Rua Augusta", "Rua Garrett", "Rua do Carmo", "Avenida Fontes Pereira de Melo", "Rua da Prata", "Rua do Ouro", "Avenida Almirante Reis", "Rua de São Bento", "Campo Grande"]),
    ("Warsaw", "Poland", 52.2297, 21.0122, ["Nowy Świat", "Marszałkowska", "Aleje Jerozolimskie", "Krakowskie Przedmieście", "Chmielna", "Świętokrzyska", "Mokotowska", "Towarowa", "Prosta", "Aleja Jana Pawła II"]),
    ("Prague", "Czech Republic", 50.0755, 14.4378, ["Wenceslas Square", "Na Příkopě", "Pařížská", "Národní", "Celetná", "Karlova", "Jindřišská", "Vodičkova", "Revoluční", "Vinohradská"]),
    ("Budapest", "Hungary", 47.4979, 19.0402, ["Váci utca", "Andrássy út", "Nagykörút", "Rákóczi út", "Kiskörút", "Király utca", "Károly körút", "Bajcsy-Zsilinszky út", "Teréz körút", "Erzsébet körút"]),
    ("Athens", "Greece", 37.9838, 23.7275, ["Ermou St", "Panepistimiou St", "Stadiou St", "Akadalias St", "Vasilissis Sofias Ave", "Patision St", "Athinas St", "Solonos St", "Syngrou Ave", "Kifissias Ave"]),

    # Asia & Middle East
    ("Tokyo", "Japan", 35.6762, 139.6503, ["Ginza Dori", "Chuo Dori", "Meiji Dori", "Yasukuni Dori", "Shinjuku Dori", "Roppongi Dori", "Omotesando", "Harajuku St", "Aoyama Dori", "Sotobori Dori"]),
    ("Osaka", "Japan", 34.6937, 135.5023, ["Midosuji", "Shinsaibashisuji", "Dotonbori", "Sakuraisuji", "Naniwasuji", "Yotsubashisuji", "Nagahoridori", "Honmachi", "Umeda", "Tenjinbashi"]),
    ("Yokohama", "Japan", 35.4437, 139.6380, ["Minato Mirai", "Bashamichi", "Isezakicho", "Motomachi", "Nihon Odori", "Kannai", "Sakuragicho", "Honcho", "Yamashitacho", "Chinatown"]),
    ("Kyoto", "Japan", 35.0116, 135.7681, ["Shijo Dori", "Kawaramachi Dori", "Karasuma Dori", "Sanjo Dori", "Oike Dori", "Gion Dori", "Higashiyama Dori", "Horikawa Dori", "Imadegawa Dori", "Marutamachi Dori"]),
    ("Seoul", "South Korea", 37.5665, 126.9780, ["Teheran-ro", "Gangnam-daero", "Jong-ro", "Eulji-ro", "Sejong-daero", "Myeongdong-gil", "Itaewon-ro", "Mapo-daero", "Yeoui-daero", "Dosan-daero"]),
    ("Busan", "South Korea", 35.1796, 129.0756,["Haeundae-ro", "Seomyon-ro", "Jungang-daero", "Gwangan-ro", "Nampo-gil", "Centum-ro", "Guyeong-daero", "Sasang-ro", "Dongnae-ro", "Gamcheon-ro"]),
    ("Shanghai", "China", 31.2304, 121.4737, ["Nanjing Rd", "Huaihai Rd", "Sichuan Rd", "Yan'an Rd", "Zhongshan Rd", "Century Ave", "Lujiazui Ring Rd", "Beijing Rd", "Henan Rd", "Tianshan Rd"]),
    ("Beijing", "China", 39.9042, 116.4074, ["Chang'an Ave", "Wangfujing St", "Xidan St", "Qianmen St", "Chaoyangmen St", "Dongdan St", "Jianguomen Ave", "Fuxingmen Ave", "Zhongguancun St", "Sanlitun Rd"]),
    ("Shenzhen", "China", 22.5431, 114.0579, ["Shennan Ave", "Babin Rd", "Huaqiang North Rd", "Renmin South Rd", "Keyuan Rd", "Nanshan Ave", "Bao'an Ave", "Futian Ave", "Binhai Ave", "Longgang Ave"]),
    ("Guangzhou", "China", 23.1291, 113.2644, ["Tianhe Rd", "Beijing Rd", "Zhongshan Rd", "Huanzhi Rd", "Huasui Rd", "Linhe East Rd", "Jianxhe Rd", "Dongfeng Rd", "Guangzhou Ave", "Huangpu Ave"]),
    ("Hong Kong", "Hong Kong", 22.3193, 114.1694, ["Nathan Rd", "Queen's Rd Central", "Des Voeux Rd", "Hennessy Rd", "Canton Rd", "Lockhart Rd", "Gloucester Rd", "Connaught Rd", "King's Rd", "Sai Yeung Choi St"]),
    ("Singapore", "Singapore", 1.3521, 103.8198, ["Orchard Rd", "Marina Blvd", "Raffles Ave", "Shenton Way", "Beach Rd", "Bridge Rd", "Bras Basah Rd", "Victoria St", "Scotts Rd", "Tanglin Rd"]),
    ("Bangkok", "Thailand", 13.7563, 100.5018, ["Sukhumvit Rd", "Silom Rd", "Sathorn Rd", "Rama I Rd", "Rama IV Rd", "Phetchaburi Rd", "Ratchadamri Rd", "Asok Montri Rd", "Thong Lo", "Ekkamai"]),
    ("Kuala Lumpur", "Malaysia", 3.1390, 101.6869, ["Jalan Bukit Bintang", "Jalan Ampang", "Jalan Sultan Ismail", "Jalan Raja Chulan", "Jalan Tun Razak", "Jalan Tuanku Abdul Rahman", "Jalan P Ramlee", "Jalan Imbi", "Jalan Bangsar", "Jalan Pinang"]),
    ("Jakarta", "Indonesia", -6.2088, 106.8456, ["Jalan MH Thamrin", "Jalan Jendral Sudirman", "Jalan HR Rasuna Said", "Jalan Gatot Subroto", "Jalan Gajah Mada", "Jalan Hayam Wuruk", "Jalan Satrio", "Jalan Kemang Raya", "Jalan Asia Afrika", "Jalan Senopati"]),
    ("Manila", "Philippines", 14.5995, 120.9842, ["Ayala Ave", "EDSA", "Roxas Blvd", "Taft Ave", "Makati Ave", "Paseo de Roxas", "Bonifacio High St", "Ortigas Ave", "Quezon Ave", "España Blvd"]),
    ("Mumbai", "India", 19.0760, 72.8777, ["Marine Drive", "Linking Rd", "Hill Rd", "Colaba Causeway", "Dr DN Rd", "SV Rd", "LBS Marg", "Pedder Rd", "Altamount Rd", "Senapati Bapat Marg"]),
    ("New Delhi", "India", 28.6139, 77.2090, ["Connaught Place", "Janpath", "Rajpath", "Barakhamba Rd", "Kasturba Gandhi Marg", "Ring Rd", "Outer Ring Rd", "Lodhi Rd", "Mathura Rd", "Sardar Patel Marg"]),
    ("Bengaluru", "India", 12.9716, 77.5946, ["MG Road", "Brigade Road", "100 Feet Road", "Commercial Street", "Indiranagar Double Road", "Residency Road", "Richmond Road", "Hosur Road", "Outer Ring Road", "Airport Road"]),
    ("Dubai", "UAE", 25.2048, 55.2708, ["Sheikh Zayed Rd", "Financial Centre Rd", "Jumeirah Beach Rd", "Al Alsayel St", "Al Wasl Rd", "Marina Promenade", "Al Khail Rd", "Corniche Rd", "Al Maktoum Rd", "Zabeel Rd"]),
    ("Abu Dhabi", "UAE", 24.4539, 54.3773, ["Corniche Rd", "Sheikh Rashid Bin Saeed St", "Hamdan St", "Zayed the First St", "Electra St", "Al Falah St", "Sultan Bin Zayed St", "Al Reem St", "Yas Island Dr", "Saadiyat St"]),
    ("Doha", "Qatar", 25.2854, 51.5310, ["Corniche St", "C Ring Rd", "Salwa Rd", "Al Majd Rd", "Lusail Expressway", "Al Sadd St", "Diplomatic St", "Pearl Blvd", "Katara St", "West Bay Dr"]),
    ("Riyadh", "Saudi Arabia", 24.7136, 46.6753, ["King Fahd Rd", "Olaya St", "Tahlia St", "King Abdullah Rd", "Makkah Al Mukarramah Rd", "King Khalid Rd", "Northern Ring Rd", "Eastern Ring Rd", "Prince Turki Rd", "Dabab St"]),
    ("Tel Aviv", "Israel", 32.0853, 34.7818, ["Rothschild Blvd", "Dizengoff St", "Ibn Gabirol St", "Allenby St", "Shenkin St", "Hayarkon St", "Herbert Samuel St", "Ben Yehuda St", "King George St", "Yigal Alon St"]),

    # South America, Australia & Africa
    ("Sydney", "Australia", -33.8688, 151.2093, ["George St", "Pitt St", "Castlereagh St", "Macquarie St", "Elizabeth St", "Bridge St", "Alfred St", "Martin Pl", "York St", "Clarence St"]),
    ("Melbourne", "Australia", -37.8136, 144.9631, ["Collins St", "Bourke St", "Flinders St", "Swanston St", "Elizabeth St", "Lonsdale St", "La Trobe St", "Spring St", "Exhibition St", "Russell St"]),
    ("Brisbane", "Australia", -27.4705, 153.0260, ["Queen St", "Adelaide St", "Ann St", "Mary St", "Charlotte St", "Edward St", "Albert St", "Eagle St", "Turbot St", "George St"]),
    ("Perth", "Australia", -31.9505, 115.8605, ["St Georges Terrace", "Hay St", "Murray St", "Adelaide Terrace", "William St", "Barrack St", "King St", "Mounts Bay Rd", "Milligan St", "Perth CBD Rd"]),
    ("Auckland", "New Zealand", -36.8485, 174.7633, ["Queen St", "Hobson St", "Nelson St", "Albert St", "Customs St", "Quay St", "Victoria St", "Wellesley St", "K Road", "Ponsonby Rd"]),
    ("São Paulo", "Brazil", -23.5505, -46.6333, ["Av. Paulista", "Av. Faria Lima", "Av. Rebouças", "Rua Augusta", "Av. Brasil", "Av. 9 de Julho", "Av. das Nações Unidas", "Rua Oscar Freire", "Av. Ibirapuera", "Av. Engenheiro Luís Carlos Berrini"]),
    ("Rio de Janeiro", "Brazil", -22.9068, -43.1729, ["Av. Atlântica", "Av. Rio Branco", "Av. Presidente Vargas", "Av. Nossa Senhora de Copacabana", "Rua Visconde de Pirajá", "Av. Brasil", "Av. das Américas", "Rua Jardim Botânico", "Av. Niemeyer", "Av. Mem de Sá"]),
    ("Buenos Aires", "Argentina", -34.6037, -58.3816, ["Av. 9 de Julio", "Av. Corrientes", "Av. Santa Fe", "Av. de Mayo", "Calle Florida", "Av. Córdoba", "Av. Alvear", "Av. Belgrano", "Av. Callao", "Av. Libertador"]),
    ("Santiago", "Chile", -33.4489, -70.6693, ["Av. Libertador Bernardo O'Higgins", "Av. Providencia", "Av. Apoquindo", "Av. Vitacura", "Calle Ahumada", "Calle Estado", "Av. Alonso de Córdova", "Av. Andrés Bello", "Av. El Bosque", "Av. Santa María"]),
    ("Bogota", "Colombia", 4.7110, -74.0721, ["Carrera 7", "Carrera 15", "Calle 72", "Calle 100", "Avenida El Dorado", "Carrera 30", "Calle 26", "Avenida Caracas", "Carrera 11", "Calle 116"]),
    ("Johannesburg", "South Africa", -26.2041, 28.0473, ["Commissioner St", "Fox St", "Main St", "Rivonia Rd", "Sandton Dr", "Oxford Rd", "Jan Smuts Ave", "Empire Rd", "William Nicol Dr", "Grayston Dr"]),
    ("Cape Town", "South Africa", -33.9249, 18.4241, ["Long St", "Buitengracht St", "Strand St", "Adderley St", "St George's Mall", "Somerset Rd", "Main Rd", "Kloof St", "Bree St", "Breakwater Blvd"]),
    ("Cairo", "Egypt", 30.0444, 31.2357, ["Tahrir Square", "Talat Harb St", "26th of July St", "Corniche El Nile", "Kasr El Nile St", "Ramses St", "Salah Salem St", "El Merghany St", "Pyramids Rd", "Al Thawra St"]),
    ("Lagos", "Nigeria", 6.5244, 3.3792, ["Adeola Odeku St", "Admiralty Way", "Bourdillon Rd", "Ahmadu Bello Way", "Awolowo Rd", "Ikorodu Rd", "Allen Ave", "Isaac John St", "Ozumba Mbadiwe Ave", "Broad St"]),
    ("Nairobi", "Kenya", -1.2921, 36.8219, ["Kenyatta Ave", "Moi Ave", "Haile Selassie Ave", "Uhuru Hwy", "Waiyaki Way", "Ngong Rd", "Argwings Kodhek Rd", "Limuru Rd", "Mombasa Rd", "Westlands Rd"])
]

GARAGE_PREFIXES = [
    "Grand", "Apex", "Metro", "Central", "CitySpace", "Royal", "Imperial", "Executive",
    "Plaza", "Tower", "Harbourfront", "Skyline", "Premier", "Express", "Ultra", "Crown",
    "Parkade", "Automated Vault", "EcoPark", "Vanguard", "Heritage", "Capital", "Starlight",
    "Horizon", "Metropolis", "Pinnacle", "Titan", "Olympus", "Beacon"
]

GARAGE_SUFFIXES = [
    "Valet & Garage", "Car Park", "Auto Deck", "Underground Vault", "Parking Center",
    "Multi-Storey Parkade", "EV & Auto Hub", "Parking Plaza", "Executive Deck", "Smart Park",
    "Mobility Hub", "Auto Sanctuary", "VIP Parking Lounge", "Automated Tower"
]

IMAGE_URLS = [
    "https://images.unsplash.com/photo-1506521781263-d8422e82f27a?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1573348722427-f1d6819fdf98?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1617886322168-72b886573c35?auto=format&fit=crop&w=1000&q=80",
    "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1000&q=80"
]

VALET_IMAGES = [
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
    "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=400&q=80"
]

DEFAULT_HASH = make_password('Pass123!')

def seed_global_parking_data(target_garages=4050, force=False, batch_size=500):
    """
    High-performance seed function that inserts 4,000+ premier garages
    along with slots, valets, companies, addresses, services, and reviews
    into Neon PostgreSQL database in committed batches.
    """
    current_count = Garage.objects.count()
    if not force and current_count >= target_garages:
        msg = f"Database already contains {current_count} garages. Skipping seed."
        logger.info(msg)
        print(msg, flush=True)
        return False

    print(f"Starting ultra-fast seed process for {target_garages} premier garages to Neon DB...", flush=True)

    # 1. Admin
    admin_user, _ = User.objects.get_or_create(
        username='admin_global',
        defaults={
            'email': 'admin@autospace.global',
            'uid': 'admin_global_001',
            'display_name': 'Global System Admin',
            'role': UserRole.ADMIN,
            'password': DEFAULT_HASH,
            'is_staff': True,
            'is_superuser': True
        }
    )

    admin_obj, _ = Admin.objects.get_or_create(
        uid=admin_user.uid,
        defaults={'display_name': admin_user.display_name}
    )

    # 2. Companies (33 Companies)
    company_names = [
        "Metro Park Global", "Apex Valet Solutions", "CitySpace Systems", "EuroPark International",
        "TransConti Parking", "Pacific Gateway Garages", "Emirates VIP Parking", "Nippon Smart Hubs",
        "AfriPark Vaults", "Starlight Parking Co", "Vanguard Auto Parks", "Metropolis Mobility",
        "Crown Parkades", "EcoPark Networks", "Titan Vaults & Valet", "Olympus Car Parks",
        "Pinnacle Garage Mgmt", "Beacon Auto Services", "Heritage Parking Group", "Capital Auto Hubs",
        "Skyline Parking Corp", "Urban Motion Garages", "Velox Valet Systems", "OmniPark Global",
        "Pronto Valet & Deck", "Zenith Parking Solutions", "AeroPark International", "Harbour Parking Network",
        "Orion Auto Decks", "Centurion Garages", "Prestige Valet Group", "Matrix Parking Systems", "Atlas Car Parks"
    ]

    companies = []
    for cname in company_names:
        comp, _ = Company.objects.get_or_create(
            display_name=cname,
            defaults={'description': "Leading global provider of premier parking, valet, and automotive services."}
        )
        companies.append(comp)

    # 3. Managers
    for idx, comp in enumerate(companies[:30], start=1):
        mgr_uid = f"mgr_{idx:03d}"
        mgr_user, _ = User.objects.get_or_create(
            username=f"manager_{idx}",
            defaults={
                'email': f"manager{idx}@autospace.global",
                'uid': mgr_uid,
                'display_name': f"Manager {comp.display_name.split()[0]}",
                'password': DEFAULT_HASH,
                'role': UserRole.MANAGER
            }
        )
        Manager.objects.get_or_create(
            uid=mgr_uid,
            defaults={'display_name': mgr_user.display_name, 'company': comp}
        )

    # 4. Valets (100 Valets)
    first_names = ["James", "Sophia", "Alexander", "Elena", "David", "Isabella", "Kenji", "Tariq", "Chidi", "Liam", "Emma", "Noah", "Lucas", "Mia", "Ethan"]
    last_names = ["Wright", "Martinez", "Chen", "Rostova", "O'Connor", "Takahashi", "Al-Mansoor", "Okafor", "Rossi", "Hemsworth", "Smith", "Johnson", "Williams", "Brown", "Jones"]

    for v_idx in range(1, 101):
        v_uid = f"valet_{v_idx:03d}"
        full_name = f"{first_names[v_idx % len(first_names)]} {last_names[(v_idx * 3) % len(last_names)]}"
        comp = companies[v_idx % len(companies)]

        v_user, _ = User.objects.get_or_create(
            username=f"valet_{v_idx}",
            defaults={
                'email': f"valet{v_idx}@autospace.global",
                'uid': v_uid,
                'display_name': full_name,
                'password': DEFAULT_HASH,
                'role': UserRole.VALET
            }
        )
        Valet.objects.get_or_create(
            uid=v_uid,
            defaults={
                'display_name': full_name,
                'company': comp,
                'licence_id': f"V-LIC-GLOBAL-{1000 + v_idx}",
                'image': VALET_IMAGES[v_idx % len(VALET_IMAGES)]
            }
        )

    # 5. Customers (100 Customers)
    customers = []
    for c_idx in range(1, 101):
        c_uid = f"cust_{c_idx:03d}"
        full_name = f"{first_names[(c_idx * 2) % len(first_names)]} {last_names[(c_idx * 5) % len(last_names)]}"

        c_user, _ = User.objects.get_or_create(
            username=f"customer_{c_idx}",
            defaults={
                'email': f"customer{c_idx}@example.com",
                'uid': c_uid,
                'display_name': full_name,
                'password': DEFAULT_HASH,
                'role': UserRole.CUSTOMER
            }
        )
        cust_obj, _ = Customer.objects.get_or_create(
            uid=c_uid,
            defaults={'display_name': full_name}
        )
        customers.append(cust_obj)

    # 6. Generate Data Specification across 100 Global Cities
    all_specs = []
    garages_per_city = (target_garages // len(CITIES)) + 1
    g_count = 0

    rng = random.Random(42)

    for city, country, base_lat, base_lng, streets in CITIES:
        if g_count >= target_garages:
            break

        for i in range(garages_per_city):
            if g_count >= target_garages:
                break

            g_count += 1
            prefix = GARAGE_PREFIXES[g_count % len(GARAGE_PREFIXES)]
            suffix = GARAGE_SUFFIXES[g_count % len(GARAGE_SUFFIXES)]
            street = streets[i % len(streets)]
            street_num = rng.randint(10, 990)
            company = companies[g_count % len(companies)]

            display_name = f"{city} {prefix} {suffix} #{g_count}"
            address_str = f"{street_num} {street}, {city}, {country}"
            
            lat_offset = (rng.random() - 0.5) * 0.06
            lng_offset = (rng.random() - 0.5) * 0.06
            lat = round(base_lat + lat_offset, 6)
            lng = round(base_lng + lng_offset, 6)

            desc = f"Premier multi-storey auto garage and valet facility located in central {city}, offering 24/7 camera security, EV charging stations, and seamless digital entry."
            img_sample = [IMAGE_URLS[g_count % len(IMAGE_URLS)], IMAGE_URLS[(g_count + 1) % len(IMAGE_URLS)]]
            base_price = round(rng.uniform(12.0, 35.0), 2)

            all_specs.append({
                'display_name': display_name,
                'company': company,
                'description': desc,
                'images': img_sample,
                'address': address_str,
                'lat': lat,
                'lng': lng,
                'base_price': base_price,
                'g_index': g_count
            })

    review_comments = [
        (5, "Exceptional parking experience! Clean facilities, super easy valet drop-off and instant entry."),
        (5, "Very smooth process and felt extremely secure leaving my vehicle here all day."),
        (4, "Great central location, friendly valet attendants and convenient EV charging!"),
        (5, "Top notch garage. The automated entry worked flawlessly and the car wash was pristine."),
        (4, "Spacious parking bays and clear signage throughout the facility. Highly recommended."),
        (5, "Prime location and state-of-the-art security setup. Will definitely use again!"),
        (5, "Very impressed with the valet efficiency and clean parking deck.")
    ]

    total_items = len(all_specs)
    print(f"Beginning rapid batch commits for {total_items} garages to Neon DB...", flush=True)

    for offset in range(0, total_items, batch_size):
        chunk = all_specs[offset:offset + batch_size]

        with transaction.atomic():
            garages_to_create = []
            for spec in chunk:
                garages_to_create.append(Garage(
                    display_name=spec['display_name'],
                    company=spec['company'],
                    description=spec['description'],
                    images=spec['images']
                ))

            created_garages = Garage.objects.bulk_create(garages_to_create)

            addresses_to_create = []
            verifications_to_create = []
            slots_to_create = []
            services_to_create = []
            reviews_to_create = []

            for i, garage in enumerate(created_garages):
                spec = chunk[i]
                bp = spec['base_price']
                g_idx = spec['g_index']

                addresses_to_create.append(Address(
                    garage=garage, address=spec['address'], lat=spec['lat'], lng=spec['lng']
                ))

                verifications_to_create.append(Verification(
                    garage=garage, verified=True, admin=admin_obj
                ))

                slots_to_create.append(Slot(
                    garage=garage, display_name="Slot A-101 (Standard Car)", price_per_hour=bp,
                    type=SlotType.CAR, length=5, width=2, height=2
                ))
                slots_to_create.append(Slot(
                    garage=garage, display_name="Slot A-102 (EV Supercharge)", price_per_hour=round(bp * 1.25, 2),
                    type=SlotType.CAR, length=5, width=2, height=2
                ))
                slots_to_create.append(Slot(
                    garage=garage, display_name="Slot M-01 (Motorbike Dock)", price_per_hour=round(bp * 0.4, 2),
                    type=SlotType.BIKE, length=3, width=1, height=2
                ))
                slots_to_create.append(Slot(
                    garage=garage, display_name="Slot H-01 (Heavy Truck Bay)", price_per_hour=round(bp * 1.8, 2),
                    type=SlotType.HEAVY, length=10, width=4, height=4
                ))
                slots_to_create.append(Slot(
                    garage=garage, display_name="Slot B-01 (Bicycle Rack)", price_per_hour=max(2.0, round(bp * 0.15, 2)),
                    type=SlotType.BICYCLE, length=2, width=1, height=1
                ))

                services_to_create.append(Service(
                    garage=garage, name="Deluxe Hand Wash & Shine",
                    description="Complete exterior foam wash, tire dressing, and micro-fiber drying.",
                    price=int(bp * 1.5), duration=45
                ))
                services_to_create.append(Service(
                    garage=garage, name="EV Supercharging Session",
                    description="High-speed DC fast charging up to 80% battery level while parked.",
                    price=int(bp * 1.2), duration=60
                ))

                c1 = customers[g_idx % len(customers)]
                c2 = customers[(g_idx + 3) % len(customers)]
                r1_rating, r1_text = review_comments[g_idx % len(review_comments)]
                r2_rating, r2_text = review_comments[(g_idx + 2) % len(review_comments)]

                reviews_to_create.append(Review(garage=garage, customer=c1, rating=r1_rating, comment=r1_text))
                reviews_to_create.append(Review(garage=garage, customer=c2, rating=r2_rating, comment=r2_text))

            Address.objects.bulk_create(addresses_to_create)
            Verification.objects.bulk_create(verifications_to_create)
            Slot.objects.bulk_create(slots_to_create)
            Service.objects.bulk_create(services_to_create)
            Review.objects.bulk_create(reviews_to_create)

        current_total = offset + len(chunk)
        print(f"Batch committed to Neon DB: {current_total}/{total_items} garages written.", flush=True)

    db_garages = Garage.objects.count()
    db_slots = Slot.objects.count()
    print(f"SUCCESS! Fully seeded Neon PostgreSQL: {db_garages} Garages, {db_slots} Slots!", flush=True)
    return True
