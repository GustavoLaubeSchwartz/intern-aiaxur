from .setup_logger import setup_logger

# Configura o logger quando o pacote é importado
logger = setup_logger()

# Expõe o logger para importação direta
__all__ = ['logger']