from extractor.scraper import rolar_resultados, coletar_estabelecimentos
from extractor.data_extractor import extrair_dados_dos_estabelecimentos
import time

def executar_extracao_em_massa(navegador, atualizar_resultado_callback=None, atualizar_log_callback=None):
    # início do ciclo
    if atualizar_log_callback:
        atualizar_log_callback("[INFO] Iniciando rolagem dos resultados...\n")

    rolar_resultados(navegador, atualizar_log_callback)
    time.sleep(2)

    if atualizar_log_callback:
        atualizar_log_callback("[INFO] Coletando links dos estabelecimentos...\n")

    estabelecimentos = coletar_estabelecimentos(navegador)
    if not estabelecimentos:
        if atualizar_log_callback:
            atualizar_log_callback("[AVISO] Nenhum estabelecimento encontrado.\n")
        return

    total = len(estabelecimentos)

    if atualizar_log_callback:
        for el in estabelecimentos:
            try:
                nome = el.get_attribute("aria-label") or "Desconhecido"
            except Exception:
                nome = "Desconhecido"
            atualizar_log_callback(f"[OK] Link encontrado para: {nome}\n")
        atualizar_log_callback(f"[INFO] Total de links coletados: {total}\n")
        atualizar_log_callback("[INFO] Iniciando extração detalhada dos dados...\n")

    # loop principal
    for i, el in enumerate(estabelecimentos, 1):
        try:
            # tenta obter o nome antes do clique (mais estável)
            try:
                nome = el.get_attribute("aria-label") or f"Estabelecimento {i}"
            except Exception:
                nome = f"Estabelecimento {i}"

            # clique no card e aguardo leve
            navegador.execute_script("arguments[0].click();", el)
            time.sleep(3)

            # log de progresso no formato esperado pelo HUD/ProgressBar
            if atualizar_log_callback:
                atualizar_log_callback(f"Visitando: {nome} ({i}/{total})\n")

            # extração
            dados = extrair_dados_dos_estabelecimentos(navegador)

            if dados:
                if atualizar_resultado_callback:
                    try:
                        atualizar_resultado_callback(dados)
                    except Exception as cb_err:
                        if atualizar_log_callback:
                            atualizar_log_callback(f"[ERRO] Falha ao atualizar interface com item {i}: {cb_err}\n")
                else:
                    if atualizar_log_callback:
                        atualizar_log_callback("[AVISO] Nenhum callback de resultado fornecido.\n")
            else:
                if atualizar_log_callback:
                    atualizar_log_callback(f"[AVISO] Nenhum dado retornado para: {nome}\n")

        except Exception as e:
            if atualizar_log_callback:
                atualizar_log_callback(f"[ERRO] Falha ao visitar card {i}: {e}\n")
            # continua para o próximo item

    if atualizar_log_callback:
        atualizar_log_callback("[OK] Extração finalizada com sucesso.\n")
