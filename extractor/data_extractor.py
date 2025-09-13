from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException
)
import time

def extrair_dados_dos_estabelecimentos(navegador):
    """
    Extrai os dados diretamente da visualização lateral do Google Maps (sem abrir nova aba).
    """
    time.sleep(2)
    try:
        nome = navegador.find_element(By.CLASS_NAME, "DUwDvf.lfPIob").text
    except:
        nome = "Não disponível"

    try:
        endereco = navegador.find_element(By.CLASS_NAME, "Io6YTe.fontBodyMedium.kR99db").text
    except:
        endereco = "Não disponível"

    try:
        telefone_element = navegador.find_element(By.CSS_SELECTOR, "button[data-tooltip*='telefone']")
        telefone = telefone_element.text.encode('ascii', 'ignore').decode().strip()
    except:
        telefone = "Não disponível"

    try:
        site = navegador.find_element(By.CSS_SELECTOR, "a[data-tooltip*='site']").get_attribute("href")
    except:
        site = "Não disponível"

    try:
        email_element = navegador.find_element(By.XPATH, "//a[contains(@href, 'mailto:')]")
        email = email_element.get_attribute("href").replace("mailto:", "")
    except:
        email = "Não disponível"

    return {
        "nome": nome,
        "endereco": endereco,
        "telefone": telefone,
        "site": site,
        "email": email
    }
