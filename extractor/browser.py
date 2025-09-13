from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
import time

def iniciar_navegador():
    # Instala o ChromeDriver compatível com a versão do Chrome
    chromedriver_autoinstaller.install()

    # Configurações para evitar detecção
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1280,800")

    # Inicia o navegador
    try:
        navegador = webdriver.Chrome(options=options)
        navegador.get("https://www.google.com/maps")
        time.sleep(3)
        return navegador
    except Exception as e:
        print(f"[ERRO] Não foi possível iniciar o navegador: {e}")
        return None
