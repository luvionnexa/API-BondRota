"""
Arquivo para definições de tempo com a biblioteca datetime
"""

import ntplib
import time
from datetime import datetime

class TimeService:
    _cache_date = None
    _last_sync = 0
    TTL = 600  # Cache de 10 minutos (600 segundos)

    @staticmethod
    def _fetch_ntp_date():
        """Lógica original de consulta NTP com fallback seguro."""
        try:
            cliente_ntp = ntplib.NTPClient()
            # Timeout curto para não travar a API se o NTP estiver lento
            resposta = cliente_ntp.request('pool.ntp.org', version=4, timeout=2)
            return datetime.fromtimestamp(resposta.tx_time).date()
        except Exception as e:
            # Em caso de erro, usa a data do servidor local para não parar o sistema
            print(f"Aviso: Erro NTP ({e}). Usando data local.")
            return datetime.now().date()

    @classmethod
    def obter_data_valida(cls):
        """Retorna a data NTP cacheada ou atualiza se expirou."""
        agora = time.time()
        if cls._cache_date is None or (agora - cls._last_sync) > cls.TTL:
            cls._cache_date = cls._fetch_ntp_date()
            cls._last_sync = agora
        return cls._cache_date

def validar_data_nao_futura(valor_data, nome_campo="Data"):
    """Função utilitária para ser usada em qualquer modelo."""
    if valor_data:
        data_oficial = TimeService.obter_data_valida()
        if valor_data > data_oficial:
            raise ValueError(f"{nome_campo} não pode ser superior à data atual ({data_oficial}).")
    return valor_data

"""
import ntplib
from datetime import datetime
import time

def obter_data_ntp():
    try:
        cliente_ntp = ntplib.NTPClient()
        # Consulta o servidor do projeto ntp.br (muito estável no Brasil)
        resposta = cliente_ntp.request('pool.ntp.org', version=4)
        
        # Transforma o timestamp em um objeto datetime
        data_atual = datetime.fromtimestamp(resposta.tx_time).date()
        
        return data_atual
    except Exception as e: 
        return f"Erro ao consultar servidor NTP: {e}"

print(f"Data oficial (via NTP): {obter_data_ntp()}")
"""