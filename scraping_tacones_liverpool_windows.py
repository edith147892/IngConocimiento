
import csv
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Lista de estados de México
estados_mexico = [
    "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas", "Chihuahua",
    "Ciudad de México", "Coahuila", "Colima", "Durango", "Estado de México", "Guanajuato", "Guerrero",
    "Hidalgo", "Jalisco", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla",
    "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", "Tamaulipas",
    "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
]

# Inicializar WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)

# Guardar resultados
resultados = []

try:
    for estado in estados_mexico:
        print(f"=== Buscando en: {estado} ===")
        driver.get("https://www.liverpool.com.mx/tienda/home")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Cambiar ciudad
        try:
            ubicacion_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='delivery']"))
            )
            ubicacion_btn.click()

            input_ciudad = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[class*='autocomplete']"))
            )
            input_ciudad.clear()
            input_ciudad.send_keys(estado)
            time.sleep(1)
            input_ciudad.send_keys(Keys.DOWN, Keys.RETURN)

            WebDriverWait(driver, 10).until(EC.invisibility_of_element(ubicacion_btn))
        except Exception as e:
            print(f"No se pudo cambiar la ciudad a {estado}: {e}")
            continue

        # Buscar tacones
        try:
            buscador = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "mainSearchbar"))
            )
            buscador.clear()
            buscador.send_keys("tacones", Keys.RETURN)

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-fs-product-card]"))
            )

            productos = driver.find_elements(By.CSS_SELECTOR, "div[data-fs-product-card]")

            for producto in productos:
                try:
                    nombre = producto.find_element(By.CSS_SELECTOR, "p.name").text
                    precio = producto.find_element(By.CSS_SELECTOR, "span.main-price").text
                    resultados.append([estado, nombre, precio])
                except:
                    continue
        except Exception as e:
            print(f"No se pudo completar la búsqueda en {estado}: {e}")

finally:
    driver.quit()

# Guardar CSV en el Escritorio de Windows
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
archivo_csv = os.path.join(desktop, "tacones_liverpool_por_estado.csv")

with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Estado", "Nombre del Producto", "Precio"])
    writer.writerows(resultados)

print(f"Archivo CSV guardado en: {archivo_csv}")
