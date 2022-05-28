import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def parse_if_number(s):
    try:
        return float(s)
    except:
        return True if s == "true" else False if s == "false" else s if s else None


def parse_ndarray(s):
    return np.fromstring(s, sep=' ') if s else None


def get_simulation_id(s):
    return s[-5:]


####################################################################################
#                          Metodo di Welch - ALOHA                                 #
####################################################################################

# Prendo il csv convertendo i campi stringa in float se possibile
aloha = pd.read_csv('aloha.csv', converters={
    'run': get_simulation_id,
    'value': parse_if_number,
    'attrvalue': parse_if_number,
    'binedges': parse_ndarray})

channels_utilizations = aloha[(aloha.type == 'scalar') & (aloha.name == 'channelUtilization:last')][['run', 'value']]
channels_utilizations.rename(columns={'value': 'numHots=15, iaMean=3'}, inplace=True)
simulation_configs = aloha[(aloha.attrname == 't')][['run', 'attrvalue']]
simulation_configs.rename(columns={'attrvalue': 't'}, inplace=True)

numHosts = aloha[(aloha.attrname == 'numHosts')][['run', 'attrvalue']]
numHosts.rename(columns={'attrvalue': 'numHosts'}, inplace=True)
iaMean = aloha[(aloha.attrname == 'iaMean')][['run', 'attrvalue']]
iaMean.rename(columns={'attrvalue': 'iaMean'}, inplace=True)

numHosts_iaMean = pd.merge(numHosts, iaMean, on='run')

throughputs = pd.merge(channels_utilizations, simulation_configs, on='run')

# Usando una finestra con tipo none tutti i valori saranno equamente pesati
# prendo i valori della finestra e ne calcolo la media mobile
throughputs = throughputs.drop(columns='run')
window_10 = throughputs.rolling(10, center=True).mean()
window_20 = throughputs.rolling(20, center=True).mean()
window_30 = throughputs.rolling(30, center=True).mean()

# Plotto i 3 grafici per ognuna delle finestre analizzate
w10 = window_10.pivot_table(index='t', values='numHots=15, iaMean=3')
w10.plot(marker='o', linestyle="-")
w10 = window_10.pivot_table(index='t', values='numHots=15, iaMean=3')
w10.plot(marker='o', linestyle="-")
w10 = window_10.pivot_table(index='t', values='numHots=15, iaMean=3')
w10.plot(marker='o', linestyle="-")

# Segno sull'asse delle y il valore del throughput medio ottenuto dal grafico con l'intervallo di confidenza
plt.axhline(y=0.187, color='r', linestyle='--', label='media throughput')
plt.legend()
plt.ylabel('Throughput ALOHA')
plt.xlabel('λ (parametro esponenziale)')
plt.show()
