# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""

import matplotlib.pyplot as plt
import pandas as pd
import glob
import os

def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """
    def crear_directorio(directorio):
        if not os.path.exists(directorio):
            os.makedirs(directorio)

    def cargar_datos(directorio_entrada):
        for archivo in glob.glob(os.path.join(directorio_entrada, "*.csv")):
            return pd.read_csv(archivo, sep=",", index_col=0)


    def shipping_per_warehouse(df):
        plt.figure()
        plt.title('Envios por bodega', fontsize = 16)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().axes.get_yaxis().set_visible(False)

        counts = df.Warehouse_block.value_counts()
        counts.plot.bar(
            xlabel='Bodega',
            ylabel='Cantidad de envios',
            color='tab:blue',
            fontsize=18,
        )
        plt.savefig(f'{directorio_salida}/shipping_per_warehouse.png')

    def mode_of_shipment(df):
        plt.figure()
        plt.title('Modo de envio', fontsize = 16)
        counts = df.Mode_of_Shipment.value_counts()
        counts.plot.pie(
            wedgeprops=dict(width=0.35),
            ylabel='',
            color=['tab:blue', 'tab:orange', 'tab:green'],
        )
        plt.savefig(f'{directorio_salida}/mode_of_shipment.png')

    def average_customer_rating(df):
        df = (
            df[["Mode_of_Shipment", "Customer_rating"]]
            .groupby("Mode_of_Shipment")
            .describe()
        )
        df.columns = df.columns.droplevel()
        df = df[["mean", "min", "max"]]
        plt.figure()
        plt.title('Calificación promedio del cliente', fontsize = 16)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_color('dimgray')
        plt.gca().spines['bottom'].set_color('dimgray')
        plt.barh(
            y = df.index.values,
            width = df["max"] - 1,
            left = df["min"].values,
            height=0.9,
            color='lightgray',
            alpha=0.8 
        )
        colores = [
            "tab:green" if v >= 30 else "tab:orange" for v in df["mean"].values
        ]
        plt.barh(
            y = df.index.values,
            width = df["mean"].values - 1,
            left = df["min"].values,
            height=0.5,
            color=colores,
            alpha=1.0
        )


        plt.savefig(f'{directorio_salida}/average_customer_rating.png')

    def weight_distribution(df):
        plt.figure()
        plt.title('Distribución del peso del envío', fontsize = 16)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)

        df.Weight_in_gms.plot.hist(
            color='tab:orange',
            edgecolor='white',
        )
        plt.savefig(f'{directorio_salida}/weight_distribution.png')

    def html_page(direcorio_salida):
        # retorna un string con el contenido del archivo HTML
        pagina = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Dashboard de envios</title>
            </head>
            <body>
                <h1 style="text-align:center">Dashboard de envios</h1>
                <div style = "width:45%;float:left">
                    <img src="shipping_per_warehouse.png" alt=Fig 1>
                    <img src="mode_of_shipment.png" alt=Fig 2>
                </div>
                <div style = "width:45%;float:left">
                    <img src="average_customer_rating.png" alt=Fig 3>
                    <img src="weight_distribution.png" alt=Fig 4>
                </div>
            </body>
        </html>
        """
        with open(f'{directorio_salida}/index.html', 'w') as archivo:
            archivo.write(pagina)
        

    global directorio_salida
    directorio_entrada = "files/input"
    directorio_salida = "docs"

    crear_directorio(directorio_salida)
    data = cargar_datos(directorio_entrada)
    df = data.copy()
    shipping_per_warehouse(df)
    mode_of_shipment(df)
    average_customer_rating(df)
    weight_distribution(df)
    html_page(directorio_salida)

pregunta_01()