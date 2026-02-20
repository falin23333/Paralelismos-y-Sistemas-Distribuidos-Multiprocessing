from time import sleep
from curl_cffi import requests
from datetime import datetime
import pandas as pd
import asyncio
from time import time, sleep
import multiprocessing
from multiprocessing import Queue
sleep_time = 0.1

def intro():
    print("""
          
┏┓      ┓  ┓•             ┏┓•            ┳┓•    •┓   • ┓   
┃┃┏┓┏┓┏┓┃┏┓┃┓┏┏┳┓┏┓┏  ┓┏  ┗┓┓┏╋┏┓┏┳┓┏┓┏  ┃┃┓┏╋┏┓┓┣┓┓┏┓┏┫┏┓┏
┣┛┗┻┛ ┗┻┗┗ ┗┗┛┛┗┗┗┛┛  ┗┫  ┗┛┗┛┗┗ ┛┗┗┗┻┛  ┻┛┗┛┗┛ ┗┗┛┗┻┗┗┻┗┛┛
                       ┛                                   

          Actividad 4 Rafael Cañada Abolafia
          
2. Modificar el programa de análisis de mercados para ejecutar todas las funciones
    paralelas en un proceso.
""")
    
def descargar_informacion(simbolo,proceso):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/" + simbolo
    params = {
        "formatted": "true",
        "interval": "1d",
        "includeAdjustedClose": "false",
        "period1": "1201824000",
        "period2": "1735603200",
        "symbol": simbolo,
    }
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, params=params, impersonate="chrome")

    if response.status_code == 200:
        response_json = response.json()
        timestamps = response_json["chart"]["result"][0]["timestamp"]
        formatted_timestamps = list(map(lambda x: datetime.utcfromtimestamp(x), timestamps))
        high = response_json["chart"]["result"][0]["indicators"]["quote"][0]["high"]
        volume = response_json["chart"]["result"][0]["indicators"]["quote"][0]["volume"]
        open = response_json["chart"]["result"][0]["indicators"]["quote"][0]["open"]
        close = response_json["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        low = response_json["chart"]["result"][0]["indicators"]["quote"][0]["low"] # Print the JSON response
    else:
        raise Exception("Se ha producido un error en la descarga del simbolo " + str(simbolo))
    dataframe_actual = pd.DataFrame(
        {
            "max": high,
            "min": low,
            "apertura": open,
            "clausura": close,
            "vol": volume,
            "day": formatted_timestamps
        }
    )

    # Add time features
    dataframe_actual["year"] = dataframe_actual["day"].dt.year
    dataframe_actual["week"] = dataframe_actual["day"].dt.isocalendar().week
    dataframe_actual["month"] = dataframe_actual["day"].dt.month
    dataframe_actual["symbol"] = simbolo

     
    proceso.put(dataframe_actual)



def agregar(dataframe, filters):
    aggregated_df = dataframe.groupby(filters).agg({
        "max": "max",
        "min": "min",
        "apertura": "first",
        "clausura": "last",
        "vol": "sum"
    }).reset_index()
    return aggregated_df




def Multiprocessin():

    procesos = []
    colas = []

    simbolos = ["AMZN", "GOOG", "F", "AAPL", "OSCR",
                "NVO", "V", "PFE", "MSFT", "META"]

    
    for sim in simbolos:
        cola = Queue()
        proceso = multiprocessing.Process(
            target=descargar_informacion,
            args=(sim, cola)
        )

        procesos.append(proceso)
        colas.append(cola)

        proceso.start()

    ###### Recuperamos datos ########
    dataframes = []
    for q in colas:
        resultado = q.get()
        dataframes.append(resultado)
    #### me aseguro de que el proceso termina, a veces al hacer .get() en la cola, recupera los datos, pero el proceso prodria seguir vivo
    for p in procesos:
        p.join()
    ###############################
    merged_df = pd.concat(dataframes, ignore_index=True)

    return merged_df

    
    
if __name__ == "__main__":
    intro()

    
    inicio = time()
    merged_df2 = Multiprocessin()
    print(f"Tiempo Multiprocessin : {time() - inicio}")
    print(merged_df2)
