# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 13:43:40 2025

@author: Enzo
"""

###############################################################################
# SCRIPT PARA UNA CARACTERIZACIÓN DE PROGRAMAS DE DOCTORADO
###############################################################################

#################################################################################
# OBJETIVO: REALIZAR UNA CARACTERIZACIÓN DE LOS PROGRAMAS DE DOCTORADO EN EL PERU
#################################################################################

# Se importan las librerias que serán usadas
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas
from shapely.geometry import Point, Polygon

# Se carga la base de datos sobre programas de doctorado
programa = pd.read_excel("BBDD_doctorados_sunedu.xlsx", sheet_name="BBDD", header=0)

# Se renombran algunos atributos del dataframe programa
programa.rename(columns=({"ÁREA OCDE":"AREA_OECD"}), inplace=True)
programa.rename(columns=({"Unnamed: 51":"egresado_docto"}), inplace=True)


# Se calculan las dimensiones de la base de datos
programa.shape
programa.columns

# Se analiza el número de programas de doctorado financiados por el Prociencia
a = programa["Financiamiento PROCIENCIA"].count()
print(f"El número de programas de doctorado financiados por el Prociencia fue {a}")

# Se analiza el número de programas de doctorado impartidos por universidades públicas financiados por el
# Prociencia

publico = programa[programa["TIPO_GESTION"]=="Público"]

b = publico["Financiamiento PROCIENCIA"].count()
print("El Número de programas de doctorado impartidos por instituciones públicas financiadas por Prociencia es", b)

# Se analizan los programas de doctorado impartidos por universidades públicas que se ubican en departamentos
# diferentes de Lima

nolima = programa.loc[(programa["TIPO_GESTION"]=="Público") & (programa["Departamento"] != "LIMA")]


# Se analiza la distribución de estos programas de doctorado según area OECD
matriz = nolima.AREA_OECD.value_counts()
matriz = matriz.to_frame()
matriz.reset_index(inplace=True)
matriz.rename(columns=({"count":"cantidad"}), inplace=True)

# Se elabora un gráfico de barras para representar lo analizado

# Configurar el tamaño de la figura
plt.figure(figsize=(14, 8))

# Crear una paleta de colores en tonos de azul inverso
palette = sns.color_palette("Blues_r", len(matriz["cantidad"]))

# Crear las barras del gráfico
bars = plt.bar(matriz["AREA_OECD"], matriz["cantidad"], color=palette)

# Etiquetas de los ejes
plt.xlabel("área OECD", fontsize=14)
plt.ylabel("Cantidad de programas de doctorado", fontsize=14)

# Agregar etiquetas de valores a cada barra con mayor tamaño de fuente
for bar in bars:
    plt.annotate(f'{bar.get_height():.0f}', 
                 xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                 xytext=(0, 5),  # Desplazamiento de la etiqueta
                 textcoords="offset points",
                 ha='center', va='bottom',
                 fontsize=12)

# Ajustar los márgenes para que las etiquetas no se corten
plt.xticks(rotation=45, fontsize=14)  # Rotar etiquetas del eje X si es necesario
plt.yticks(fontsize=14)
plt.tight_layout()

# Mostrar el gráfico
plt.show()


# Se analiza la distribución departamental de los programas de doctorado que no son del ambito de las
# Ciencias Sociales

nosocial = nolima[nolima["AREA_OECD"] != "5. Ciencias Sociales"]
nosocial.columns

matriz1 = nosocial.Departamento.value_counts()
matriz1 = matriz1.to_frame()
matriz1.reset_index(inplace=True)


# Se cambia el nombre de algunas filas de la columna Departamento del dataframe matriz1
matriz1["Departamento"] = matriz1["Departamento"].replace({"JUNÍN":"JUNIN",
                                                           "ÁNCASH":"ANCASH",
                                                           "HUÁNUCO":"HUANUCO"})


# Se elabora un gráfico de barras para representar lo analizado

# Configurar el tamaño de la figura
plt.figure(figsize=(14, 8))

# Crear una paleta de colores en tonos de azul inverso
palette = sns.color_palette("viridis", len(matriz["cantidad"]))

# Crear las barras del gráfico
bars = plt.bar(matriz1["Departamento"], matriz1["count"], color=palette)

# Etiquetas de los ejes
plt.xlabel("Región", fontsize=14)
plt.ylabel("Cantidad de programas de doctorado", fontsize=14)

# Agregar etiquetas de valores a cada barra con mayor tamaño de fuente
for bar in bars:
    plt.annotate(f'{bar.get_height():.0f}', 
                 xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                 xytext=(0, 5),  # Desplazamiento de la etiqueta
                 textcoords="offset points",
                 ha='center', va='bottom',
                 fontsize=12)

# Ajustar los márgenes para que las etiquetas no se corten
plt.xticks(rotation=45, fontsize=14)  # Rotar etiquetas del eje X si es necesario
plt.yticks(fontsize=14)
plt.tight_layout()

# Mostrar el gráfico
plt.show()


# Ahora se analiza solo a los programas de doctorado ofertados por universidades públicas
# que se ubican en departamentos diferentes de Lima relacionados exclusivamente con el ambito de la tecnología
tecnologia = nolima[nolima["AREA_OECD"]=="2. Ingeniería y Tecnología"]

matriz2 = tecnologia.Departamento.value_counts()
matriz2 = matriz2.to_frame()
matriz2.reset_index(inplace=True)

# Se cambia el nombre de algunas filas de la columna Departamento del dataframe matriz2
matriz2["Departamento"] = matriz2["Departamento"].replace({"JUNÍN":"JUNIN",
                                                           "ÁNCASH":"ANCASH"})


# Se construye el mapa de Perú, a nivel departamental, usando la información del INEI
peru = geopandas.read_file("INEI_LIMITE_DEPARTAMENTAL_GEOGPSPERU_JUANSUYO_931381206.shp")
peru.columns
peru.rename(columns=({"NOMBDEP":"Departamento"}), inplace=True)


caso = pd.merge(peru, matriz2, on="Departamento")
caso.columns

fig, ax = plt.subplots(1, figsize=(10, 6))
ax.axis('off')
#ax.set_title('Distribución espacial del número de empresas que recibieron financiamiento de Prociencia, 2020-2022', fontdict={'fontsize': '10', 'fontweight' : '3'})

caso.plot(column='count',
            cmap='YlOrRd',
            linewidth=0.9,
            ax=ax,
            edgecolor='1',
            legend=True)


# Se utiliza un archivo que contiene información sobre el índice de competitividad regional y se correlaciona con
# la información del dataframe matriz1

incore = pd.read_excel("BBDD_indice_competitividad_regional.xlsx", sheet_name="INCORE", header=0) 
incore.shape
incore.columns

# Se renombra la columna REGION
incore.rename(columns=({"REGION":"Departamento"}), inplace=True)
incore.rename(columns=({"Media":"incore_media"}), inplace=True)

# Se construye un dataframe considerando incore y matriz1 para la respectiva correlación
corr_incore = pd.merge(matriz1, incore, on="Departamento")
corr_incore.columns

# Se grafica un mapa de correlación para entre la cantidad de programas de doctorado y el Índice promedio
# de Competitividad Regional (INCORE)

correlation_matrix = corr_incore[["count", "incore_media"]].corr()
plt.figure(figsize=(6, 5))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", cbar=True)
#plt.title("Mapa de Correlación")
plt.show()

# Se elabora un gráfico de correlación entre el número de grupos de investigación y el número de programas de doctorado 

plt.figure(figsize=(6, 6))

# Graficar correlación con Seaborn
sns.regplot(x=corr_incore["count"], y=corr_incore["Cantidad_GI"], scatter_kws={"color": "blue"}, line_kws={"color": "red"})

# Agregar nombres a cada punto
for i in range(len(corr_incore)):
    plt.text(corr_incore["count"].iloc[i], corr_incore["Cantidad_GI"].iloc[i], corr_incore["Departamento"].iloc[i], 
             fontsize=7, ha='right', va='bottom', color='black')

# Personalizar el gráfico
plt.xlabel("Número de programas de doctorado")
plt.ylabel("Número de grupos de investigación")


# Se realiza un análisis considerando los egresados de los programas de doctorado ofertados por una determinada universidad
# y el número de publicaciones científicas en donde investigadores consignaron como afiliación a dicha universidad

# Se consideran publicaciones científicas indizadas en la base de datos SCOPUS al 2024 y sus respectivas afiliaciones
scopus_renacyt = pd.read_csv("tbl_ws_api_scopus_detalle_afiliacion_publicaciones_renacyt.csv",encoding='utf-8', delimiter = ",")
scopus_renacyt.shape
scopus_renacyt.info()
scopus_renacyt.dtypes
scopus_renacyt.columns
scopus_renacyt["eid"].nunique()
scopus_renacyt["auth_id"] = scopus_renacyt["auth_id"].apply(lambda x: str(x))
scopus_renacyt["af_id"] = scopus_renacyt["af_id"].apply(lambda x: str(x))

# Solo se consideran las publicaciones científicas cuya afiliación tenga que ver con el Perú
pub_peru = scopus_renacyt[scopus_renacyt["affiliation_country"]=="Peru"]
pub_peru = pub_peru.drop_duplicates(subset=["eid", "af_id"])
tbl_pub_peru = pub_peru.affil_name.value_counts()
tbl_pub_peru = tbl_pub_peru.to_frame()
tbl_pub_peru.reset_index(inplace=True)
tbl_pub_peru.columns
tbl_pub_peru.rename(columns=({"count":"cantidad_pub"}), inplace=True)
tbl_pub_peru.rename(columns=({"affil_name":"NOMBRE_ENTIDAD"}), inplace=True)

# Ahora bien, se calcula la distribución de los egresados por universidad pública que oferta un programa de doctorado
# cuya temática de investigación esta fuera del ambito de las ciencias sociales
tabla1 = pd.pivot_table(nosocial, values="egresado_docto", index="NOMBRE_ENTIDAD",aggfunc="sum")

# Se construye una tabla que almacene información del número de egresados de programa de doctorado y publicaciones científicas
fusion = pd.merge(tabla1, tbl_pub_peru, on="NOMBRE_ENTIDAD", how="left")

# El dataframe fusion se convierte en un archivo xlsx
fusion.to_excel("tabla_egresados_publicaciones.xlsx")


# Considerando el dataframe nosocial, se realiza un análisis entre los ingresantes y los egresados
tabla2 = pd.pivot_table(nosocial, values=["ingresantes", "egresado_docto"], index="NOMBRE_ENTIDAD", aggfunc="sum") 
tabla2.reset_index(inplace=True)
tabla2.columns
tabla2 = tabla2[["NOMBRE_ENTIDAD","ingresantes", "egresado_docto"]]


# Se elabora un gráfico de bombillas para visualizar la relación entre egresados e ingresantes

# Ordenar por número de ingresantes (opcional pero recomendado)
df_plot = tabla2.sort_values("ingresantes")

# Crear figura
plt.figure(figsize=(10, 6))

# Dibujar líneas (la "bombilla")
for i in range(len(df_plot)):
    plt.plot(
        [df_plot["egresado_docto"].iloc[i], df_plot["ingresantes"].iloc[i]],
        [i, i]
    )

# Dibujar puntos
plt.scatter(df_plot["egresado_docto"], range(len(df_plot)), s=80, label="Egresados")
plt.scatter(df_plot["ingresantes"], range(len(df_plot)), s=200, label="Ingresantes")

# Etiquetas del eje Y
plt.yticks(range(len(df_plot)), df_plot["NOMBRE_ENTIDAD"])

# Etiquetas y título
plt.xlabel("Número de personas")
#plt.title("Relación entre Ingresantes y Egresados en Programas de Doctorado")

# Leyenda
plt.legend()

# Ajuste visual
plt.grid(axis="x", linestyle="--", alpha=0.5)
plt.tight_layout()

plt.show()

# Considerando el dataframe nosocial, se elabora una distribución de doctorados para observar el más recurrente
nosocial.NOMBRE_PROGRAMA.value_counts()














