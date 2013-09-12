'''
Created on May 23, 2012

@author: th
'''
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

ES_source_CHOICES=(('Select a source','Select a source'),('a','NatureServe'),('b','IUCN Red List'),('c','US FWD Critical Habitat')) 
Crop_CHOICES=(('','Select a source'),('Barley','Barley'),('Beans','Beans'),('Canola','Canola'),('Corn','Corn'),('Cotton','Cotton'),
              ('Flaxseed','Flaxseed'),('Hay','Hay'),('Oats','Oats'),('Peanuts','Peanuts'),('Rice','Rice'),
              ('Sorghum','Sorghum'),('Soybeans','Soybeans'),('Sugarbeets','Sugarbeets'),('Sugarcane','Sugarcane'),
              ('Sunflowers','Sunflowers'),('Sweet Potatoes','Sweet Potatoes'),('Tobacco','Tobacco'),
              ('Tomatoes','Tomatoes'),('Wheat','Wheat'))
NS_CHOICES=(('','Select an animal type'),('a1','NatureServe Mammals'),('a2','NatureServe Birds'),('a3','NatureServe Fish'))
NSM_CHOICES=(('', 'Scientific Name (Common Name)'), ('1', 'Physeter macrocephalus (Sperm Whale)'), ('2', 'Monachus schauinslandi (Hawaiian Monk Seal)'), ('3', 'Mustela nigripes (Black-footed Ferret)'), ('4', 'Reithrodontomys raviventris (Salt-marsh Harvest Mouse)'), ('5', 'Leopardus wiedii (Margay)'), ('6', 'Balaenoptera physalus (Fin Whale)'), ('7', 'Eumetopias jubatus (Steller Sea Lion)'), ('8', 'Vulpes velox (Swift Fox)'), ('9', 'Myotis grisescens (Gray Myotis)'), ('10', 'Eschrichtius robustus (Gray Whale)'), ('11', 'Dipodomys ingens (Giant Kangaroo Rat)'), ('12', 'Leopardus pardalis (Ocelot)'), ('13', 'Megaptera novaeangliae (Humpback Whale)'), ('14', 'Canis lupus (Gray Wolf)'), ('15', 'Canis rufus (Red Wolf)'), ('16', 'Eubalaena glacialis (North Atlantic Right Whale)'), ('17', "Dipodomys stephensi (Stephens's Kangaroo Rat)"), ('18', 'Orcinus orca (Killer Whale)'), ('19', 'Balaenoptera borealis (Sei Whale)'), ('20', 'Leptonycteris nivalis (Mexican Long-nosed Bat)'), ('21', 'Trichechus manatus (West Indian Manatee)'), ('22', 'Balaena mysticetus (Bowhead)'), ('23', 'Ovis aries (Red Sheep)'), ('24', 'Eubalaena japonica (North Pacific Right Whale)'), ('25', 'Leptonycteris yerbabuenae (Lesser Long-nosed Bat)'), ('26', 'Myotis sodalis (Indiana Myotis)'), ('27', 'Panthera onca (Jaguar)'), ('28', 'Lynx rufus (Bobcat)'), ('29', 'Balaenoptera musculus (Blue Whale)'))
NSF_CHOICES=(('','Select a fish type'),('Acantharchus_pomotis','Acantharchus pomotis'),('Acipenser_brevirostrum','Acipenser brevirostrum'),('Acipenser_fulvescens','Acipenser fulvescens'),('Acipenser_medirostris','Acipenser medirostris'),('Acipenser_oxyrinchus','Acipenser oxyrinchus'),('Acipenser_transmontanus','Acipenser transmontanus'))

NSB_CHOICES=(('', 'Scientific Name (Common Name)'), ('1', "Loxops coccineus ochraceus (Maui 'Akepa)"), ('2', 'Numenius borealis (Eskimo Curlew)'), ('3', "Hemignathus lucidus hanapepe (Kauai Nukupu'u)"), ('4', 'Myadestes lanaiensis rutha (Molokai Thrush)'), ('5', 'Pterodroma sandwichensis (Hawaiian Petrel)'), ('6', 'Himantopus mexicanus knudseni (Hawaiian Stilt)'), ('7', 'Anas wyvilliana (Hawaiian Duck)'), ('8', 'Colinus virginianus ridgwayi (Masked Bobwhite)'), ('9', 'Gymnogyps californianus (California Condor)'), ('10', "Psittirostra psittacea ('O'u)"), ('11', 'Fulica alai (Alae Keokeo)'), ('12', "Dendroica kirtlandii (Kirtland's Warbler)"), ('13', "Melamprosops phaeosoma (Po'Ouli)"), ('14', 'Sterna dougallii dougallii (Roseate Tern)'), ('15', 'Phoebastria albatrus (Short-tailed Albatross)'), ('16', 'Paroreomyza maculata (Oahu Alauahio)'), ('17', 'Grus americana (Whooping Crane)'), ('18', 'Myadestes palmeri (Puaiohi)'), ('19', "Hemignathus lucidus (Nukupu'u)"), ('20', 'Telespiza cantans (Laysan Finch)'), ('21', 'Ammodramus maritimus mirabilis (Cape Sable Sparrow)'), ('22', 'Sternula antillarum browni (California Least Tern)'), ('23', "Vireo bellii pusillus (Least Bell's Vireo)"), ('24', "Loxops coccineus coccineus (Hawaii 'Akepa)"), ('25', 'Dendroica chrysoparia (Golden-cheeked Warbler)'), ('26', 'Rostrhamus sociabilis plumbeus (Snail Kite)'), ('27', 'Hemignathus munroi (Akiapolaau)'), ('28', "Tympanuchus cupido attwateri (Attwater's Greater Prairie Chicken)"), ('29', 'Grus canadensis pulla (Mississippi Sandhill Crane)'), ('30', 'Gallinula chloropus sandvicensis (Hawaiian Gallinule)'), ('31', 'Paroreomyza flammea (Kakawahie)'), ('32', 'Branta sandvicensis (Hawaiian Goose)'), ('33', 'Mycteria americana (Wood Stork)'), ('34', 'Charadrius melodus (Piping Plover)'), ('35', 'Falco femoralis septentrionalis (Northern Aplomado Falcon)'), ('36', 'Oreomystis mana (Hawaii Creeper)'), ('37', 'Palmeria dolei (Akohekohe)'), ('38', 'Buteo solitarius (Hawaiian Hawk)'), ('39', 'Lanius ludovicianus mearnsi (San Clemente Loggerhead Shrike)'), ('40', 'Myadestes myadestinus (Kamao)'), ('41', 'Empidonax traillii extimus (Southwestern Willow Flycatcher)'), ('42', 'Vireo atricapilla (Black-capped Vireo)'), ('43', 'Moho braccatus (Kauai Oo)'), ('44', 'Acrocephalus familiaris kingi (Nihoa Millerbird)'), ('45', 'Ammodramus savannarum floridanus (Florida Grasshopper Sparrow)'), ('46', 'Aerodramus bartschi (Mariana Swiftlet)'), ('47', 'Hemignathus ellisianus (Greater Akialoa)'), ('48', 'Oreomystis bairdi (Akikiki)'), ('49', "Hemignathus lucidus lucidus (Oahu Nukupu'u)"), ('50', 'Rallus longirostris yumanensis (Yuma Clapper Rail)'), ('51', 'Rallus longirostris obsoletus (California Clapper Rail)'), ('52', 'Corvus hawaiiensis (Hawaiian Crow)'), ('53', 'Loxops caeruleirostris (Akekee)'), ('54', 'Loxioides bailleui (Palila)'), ('55', 'Campephilus principalis (Ivory-billed Woodpecker)'), ('56', 'Anas laysanensis (Laysan Duck)'), ('57', "Hemignathus lucidus affinis (Maui Nukupu'u)"), ('58', 'Rallus longirostris levipes (Light-footed Clapper Rail)'), ('59', "Chasiempis sandwichensis ibidis (Oahu 'Elepaio)"), ('60', 'Pseudonestor xanthophrys (Maui Parrotbill)'), ('61', 'Picoides borealis (Red-cockaded Woodpecker)'), ('62', 'Telespiza ultima (Nihoa Finch)'), ('63', 'Falco peregrinus (Peregrine Falcon)'), ('64', 'Sternula antillarum (Least Tern)'), ('65', 'Sternula antillarum athalassos (Interior Least Tern)'), ('66', "Vermivora bachmanii (Bachman's Warbler)"))
IUCN_CHOICES=(('', 'Scientific Name (Common Name)'), ('1','Gambelia sila (Blunt-nosed Leopard Lizard)'),('','Thamnophis sirtalis (San Francisco Garter Snake)'))
USFWS_t_CHOICES=(('', 'Select an animal type'), ('c1','USFWS Polygons'), ('c2','USFWS Lines'))
USFWS_p_CHOICES=(('', 'Scientific Name (Common Name)'), ('0', 'Zosterops rotensis (Rota bridled White-eye)'), ('1', 'Gila bicolor ssp. snyderi (Owens tui chub)'), ('2', 'Drosophila substenoptera ([Unnamed] pomace fly)'), ('3', 'Monardella viminea (Willowy monardella)'), ('4', 'Chamaesyce celastroides var. kaenana (`Akoko)'), ('5', 'Chamaesyce halemanui (No common name)'), ('6', 'Plagopterus argentissimus (Woundfin)'), ('7', 'Speoplatyrhinus poulsoni (Alabama cavefish)'), ('8', 'Notropis mekistocholas (Cape Fear shiner)'), ('9', 'Gila elegans (Bonytail chub)'), ('10', 'Gambusia georgei (San Marcos gambusia)'))
USFWS_l_CHOICES=(('', 'Scientific Name (Common Name)'), ('1', 'Leptoxis foremani (Interrupted (=Georgia) Rocksnail)'), ('2', 'Pleurobema hanleyianum (Georgia pigtoe)'), ('3', 'Pleurocera foremani (Rough hornsnail)'), ('4', 'Etheostoma sellare (Maryland darter)'), ('5', 'Scaphirhynchus suttkusi (Alabama sturgeon)'), ('6', 'Noturus baileyi (Smoky madtom)'), ('7', 'Chasmistes liorus (June sucker)'), ('8', 'Catostomus microps (Modoc Sucker)'), ('9', 'Etheostoma chermocki (Vermilion darter)'), ('10', 'Villosa perpurpurea (Purple bean)'), ('11', 'Quadrula cylindrica strigillata (Rough rabbitsfoot)'), ('12', 'Epioblasma brevidens (Cumberlandian combshell)'), ('13', 'Alasmidonta atropurpurea (Cumberland elktoe)'), ('14', 'Epioblasma capsaeformis (Oyster mussel)'), ('15', 'Epioblasma othcaloogensis (Southern acornshell)'), ('16', 'Epioblasma metastriata (Upland combshell)'), ('17', 'Lasmigona decorata (Carolina heelsplitter)'), ('18', 'Pleurobema pyriforme (Oval pigtoe)'), ('19', 'Lampsilis subangulata (Shinyrayed pocketbook)'), ('20', 'Amblema neislerii (Fat three-ridge (mussel))'), ('21', 'Pleurobema perovatum (Ovate clubshell)'), ('22', 'Pleurobema decisum (Southern clubshell)'), ('23', 'Ptychobranchus greenii (Triangular Kidneyshell)'), ('24', 'Medionidus parvulus (Coosa moccasinshell)'), ('25', 'Pleurobema furvum (Dark pigtoe)'), ('26', 'Pleurobema georgianum (Southern pigtoe)'), ('27', 'Medionidus penicillatus (Gulf moccasinshell)'), ('28', 'Medionidus simpsonianus (Ochlockonee moccasinshell)'), ('29', 'Eubalaena glacialis (North Atlantic Right Whale)'), ('30', 'Elliptio spinosa (Altamaha Spinymussel)'), ('31', 'Oncorhynchus (=Salmo) mykiss (Steelhead)'), ('32', 'Oncorhynchus (=Salmo) tshawytscha (Chinook salmon)'))

class esInp(forms.Form):
    ES_source = forms.ChoiceField(choices=ES_source_CHOICES, label='Endangered Species Sources')        
    NS = forms.ChoiceField(choices=NS_CHOICES, label='NatureServe Animal Type')        
    NSM = forms.ChoiceField(choices=NSM_CHOICES, label='NatureServe Mammals')  
    NSB = forms.ChoiceField(choices=NSB_CHOICES, label='NatureServe Birds')  
    NSF = forms.ChoiceField(choices=NSF_CHOICES, label='NatureServe Fish')  
    IUCN = forms.ChoiceField(choices=IUCN_CHOICES, label='IUCN animals')
    USFWS_t = forms.ChoiceField(choices=USFWS_t_CHOICES, label='USFWS Animal Type')
    USFWS_p = forms.ChoiceField(choices=USFWS_p_CHOICES, label='USFWS Polygons')
    USFWS_l = forms.ChoiceField(choices=USFWS_l_CHOICES, label='USFWS Lines')
   
    Crop = forms.ChoiceField(choices=Crop_CHOICES, label='Crop')        
    Year = forms.FloatField(initial=1990)


























            
