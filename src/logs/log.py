"""
configuração global de logs
"""

import logging
import sys

# Configuração global do logging
logging.basicConfig(
    level=logging.INFO,  # Define o nível mínimo de captura
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formato da mensagem
    datefmt="%Y-%m-%d %H:%M:%S",  # Formato da data e hora
    handlers=[
        logging.FileHandler("logs/app.log", mode="a", encoding="utf-8"),  # Salva no arquivo
        logging.StreamHandler(sys.stdout)  # Mostra no terminal
    ]
)

logger = logging.getLogger(__name__)