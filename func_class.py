from selectorlib import Extractor as ext
import requests as req
from fpdf import FPDF

'''Libreria para parcial 1, lenguajes de programacion 2'''
class Population:
    '''La clase ciudad tiene metodos para conocer la poblacion, el pais, y temperatura de una
    ciudad especificada'''
    def __init__(self, city):
        self.headers = { 'pragma': 'no-cache', 'cache-control': 'no-cache', 'dnt': '1', 
        'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36', 
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8', }
        self.city = city
        self.url = 'https://worldpopulationreview.com/world-cities/' + self.city + '-population' 
        r = req.get(self.url, self.headers)
        self.content = r.text

    def get_population(self):
        '''Este metodo de la clase population retorna la cantidad de habitantes de la ciudad solicitada'''
        x_path2 = './population.yaml'
        extractor = ext.from_yaml_file(x_path2)
        self.result_population = extractor.extract(self.content)
        return self.result_population['data']
        
    def get_country(self):
        '''Este metodo de la clase Population retorna el pais al cual pertenece la ciudad solicitada'''        
        x_path = './country.yaml'
        extractor = ext.from_yaml_file(x_path)
        self.result_country = extractor.extract(self.content)
        return self.result_country['data']

    def grados_celsius(self):
        '''este metodo de la clase population retorna la temperatura de la ciudad solicitada'''
        country = self.get_country()
        if country == 'United Kingdom':
            country = 'uk'
        elif country == 'United States':
            country= 'usa'
        self.url2 = 'https://www.timeanddate.com/weather/' + country + '/' + self.city.lower()
        r2 = req.get(self.url2, self.headers)
        self.content2 = r2.text
        x_path3 = './temperature.yaml'
        extractor3 = ext.from_yaml_file(x_path3)
        self.result_temp = extractor3.extract(self.content2)
        return self.result_temp['data']  

def verificar_numero():
    '''Esta funcion pide cantidad de ciudades y la verifica, tiene que ser un numero, 
    no permite numeros menores de 0 '''
    numero = input('Ingrese la cantidad de ciudades que desea consultar: ') # recibe la edad como str
    if not numero.isnumeric() == True: # si el str no es solo numerico alerta de error
        print('Cantidad no valida, vuelva a intentarlo...')
        return 0
    else:
        numero = int(numero)    #convierte a entero 
        try:
            if numero >= 0: #fuera de rango
                print('-'*60)
                return numero # retorna la edad en caso de que cumpla todas las condiciones

        except ValueError:
                print('Cantidad no valida, vuelva a intentarlo...')
                return 0

def ppal():
    '''Esta funcion usa la clase utiliza los metodos y los atibutos de la clase population
    para extraer de la web la informacion requerida, con las librerias requests y selectorlib,
    finalmente hace uso de la funcion reporte_pdf() para generar el pdf con la informacion recibida'''
    numero_ciudades = verificar_numero()
    while numero_ciudades == 0:
        numero_ciudades = verificar_numero()

    cities = []
    countries = []
    temperatures = []
    pop = []
    pop_str = []
    for i in range(numero_ciudades):
        ciudad = input(f'Ingresa la ciudad numero {i + 1}: ')
        clase = Population(ciudad)
        while clase.get_population() == None:                
            if clase.get_population() == None:
                print('Ciudad no encontrada, ingrese una ciudad valida...')
                ciudad = input(f'Ingresa la ciudad numero {i + 1}: ')
                clase = Population(ciudad)

        aux = clase.get_population().replace(',', '', 1000)
        pop.append(int(aux))
        pop_str.append(clase.get_population())
        cities.append(clase.city)
        countries.append(clase.get_country())
        temperatures.append(clase.grados_celsius())
    print('-'*60)
    for j in range(len(temperatures)):
        print(f'Informacion actual de {cities[j].capitalize()} / {countries[j].capitalize()} a esta hora:')
        print(f'Temperatura {temperatures[j]}')
        print(f'Poblacion {pop_str[j]}')
        print('-'*60)

    print(f'La diferencia poblacional entre la ciudad con mas\nhabitantes y la de menos habitantes es:  {max(pop) - min(pop)}')
    print('-'*60)
    diference_population = max(pop) - min(pop)
    
    reporte_pdf(cities, countries, pop_str, temperatures, pop)

class reporte_pdf(FPDF):
    ''' Esta clase crea un objeto del tipo FPDF y recibe en su metodo contructor los 
    parametros de entrada de lo que va a imprimir, genera un archivo pdf con la informacion
    recibida'''
    def __init__(self, cities, countries, pop_str, temperatures, pop):
        pdf = FPDF()
        y = 20
        pdf.add_page()
        pdf.set_font('Times', 'B', 20)
        pdf.set_y(y)
        pdf.cell(0,0, 'DATOS DE LAS CIUDADES DEL MUNDO', ln = 1, align = 'C')
        cont = 0
        y = 0
        for i in range(len(cities)):
            pdf.set_font('Times', 'B', 12)
            pdf.set_y(y + 40)
            pdf.cell(0, 0, f'La informacion de {cities[i].capitalize()} / {countries[i]} a esta hora es: ')
            pdf.set_y(y + 45)
            pdf.set_x(20)
            pdf.cell(0, 0, f'- Poblacion: {pop_str[i]}')
            pdf.set_y(y + 50)
            pdf.set_x(20)
            pdf.cell(0, 0, f'- Temperatura: {temperatures[i]}')
            pdf.set_y(y + 55)
            pdf.cell(0, 0, '-'*130)
            cont = cont + 20
            y = cont
                
        pdf.set_y(y + 35)
        pdf.cell(0, 10, f'La diferencia poblacional entre la ciudad con mas\nhabitantes y la de menos habitantes es:  {max(pop) - min(pop)}')
        pdf.output('parcial.pdf', 'F')