# LEADSPRO — Google Maps Extractor (GUI)

Aplicativo desktop (Tkinter + Selenium) que abre o Google Maps, coleta estabelecimentos da lista de resultados e exporta **Nome, Endereço, Telefone, Site, Email** para **CSV/Excel/JSON/PDF**.

> ⚠️ Aviso legal: o uso de automação pode violar os Termos de Serviço do Google. Use por sua conta e risco. Para uso comercial/escala, avalie a **Google Places API**.

## Demo
![screenshot](assets/screenshot.png)

## Recursos
- GUI amigável (Tkinter, tema escuro)
- Barra de progresso, HUD (coletados/erros/tempo/velocidade)
- Logs em tempo real
- Exporta CSV/Excel/JSON/
- Atalhos de teclado (Ctrl+I, Ctrl+E, Ctrl+S, Ctrl+C)
- Ordenar por coluna, zebra striping, menu de contexto

## Requisitos
- Windows 10/11
- Python 3.10+ (testado com 3.11/3.12)
- Google Chrome instalado

## Instalação (dev)
```bash
git clone https://github.com/<seu-usuario>/leadspro-maps-extractor.git
cd leadspro-maps-extractor
python -m venv .venv
.\.venv\Scripts\activate  # Windows
python -m pip install -U pip
python -m pip install -r requirements.txt
python main.py
