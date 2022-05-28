import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def parse_if_number(s):
    try: return float(s)
    except: return True if s=="true" else False if s=="false" else s if s else None

def parse_ndarray(s):
    return np.fromstring(s, sep=' ') if s else None
####################################################################################
#	Plotting della simulazione Pure ALOHA - Throughput 			   #
####################################################################################

# Prendo il csv convertendo i campi stringa in float se possibile
# e le stringhe separate da uno spazio in array di interi
aloha = pd.read_csv('aloha.csv', converters = {
    'attrvalue': parse_if_number,
    'binedges': parse_ndarray,
    'binvalues': parse_ndarray,
    'vectime': parse_ndarray,
    'vecvalue': parse_ndarray})

# Filtro la colonna type per i valori indicati
scalars = aloha[(aloha.type=='scalar') | (aloha.type=='itervar')]  
# Creo una nuova colonna in cui il valore inserito sarà uguale al nome del nodo (modulo) + nome del valore dello scalare
scalars = scalars.assign(qname = scalars.attrname.combine_first(scalars.module + '.' + scalars.name))  
# Passo i valori di attrvalue in fp all'interno della colonna 'value'
scalars.value = scalars.value.combine_first(scalars.attrvalue.astype('float64'))  

# Costruiamo una tabella in cui per ogni simulazione idichiamo tutti i suoi attributi, disposti nelle varie colonne
scalars_wide = scalars.pivot('run', columns='qname', values='value')

# Redisposizione della tabella in cui usiamo la funzione di aggregazione per channelUtilization
aloha_pivot = scalars_wide.pivot_table(index='iaMean', columns='numHosts', values='Aloha.server.channelUtilization:last')  # note: aggregation function = mean (that's the default)
aloha_pivot.plot(marker='o',linestyle="-")
plt.ylabel('Throughput ALOHA')
plt.xlabel('λ (parametro esponenziale)')
plt.show()
