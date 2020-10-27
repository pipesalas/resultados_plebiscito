import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np

def main():
    st.title('Exploración de resultados del plebiscito para una nueva constitución en Chile :balloon:')
    df = cargamos_datos_consolidados()
    st.write('Contamos con los datos: (además de cada polygon)')
    st.write(df[df.columns[:-1]].head())
    #st.write(df.head())
    
    
    
@st.cache
def cargamos_datos_votacion():
    df = pd.read_csv('BBDD Plebiscito 2020 - CPE UDLA en base a SERVEL, 2020 - 2020.csv')
    return df
@st.cache
def cargamos_datos_comuna():
    gdf_comunas = gpd.read_file('./Comunas/comunas.shp')
    gdf_comunas.rename(columns= {'cod_comuna': 'cod_com'}, inplace=True)
    return gdf_comunas

@st.cache
def cargamos_datos_consolidados():
    df = cargamos_datos_votacion()
    gdf = cargamos_datos_comuna()
    df_consolidado = df.merge(gdf, on=['cod_com'])
    return df_consolidado

    
    
main()