from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def rolar_resultados(navegador, atualizar_log_callback=None):
    try:
        scrollable_div = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
        )
        ultimo_altura = 0
        tentativas_sem_mudanca = 0

        while tentativas_sem_mudanca < 5:
            navegador.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(2)
            nova_altura = navegador.execute_script("return arguments[0].scrollHeight", scrollable_div)
            if nova_altura == ultimo_altura:
                tentativas_sem_mudanca += 1
            else:
                tentativas_sem_mudanca = 0
                ultimo_altura = nova_altura

            try:
                navegador.find_element(By.XPATH, "//*[contains(text(), 'Você chegou ao final da lista')]")
                break
            except:
                continue

    except Exception as e:
        if atualizar_log_callback:
            atualizar_log_callback(f"[ERRO] Erro ao rolar a lista: {e}\n")

def coletar_estabelecimentos(navegador):
    estabelecimentos = []
    try:
        WebDriverWait(navegador, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.hfpxzc"))
        )
        cards = navegador.find_elements(By.CSS_SELECTOR, "a.hfpxzc")
        for card in cards:
            nome = card.get_attribute("aria-label")
            if nome:
                estabelecimentos.append(card)
    except Exception as e:
        print(f"[ERRO] Falha ao coletar elementos: {e}")
    return estabelecimentos
