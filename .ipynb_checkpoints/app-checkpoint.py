import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st
import pandas as pd
import numpy as np
import descartes

def main():
    st.title('Exploración de resultados del plebiscito para una nueva constitución en Chile :balloon:')
    st.write('Ojo, sacaremos Isla de Pascua y Juan Fernandez para hacer mejor los mapitas')
    df = cargamos_datos_consolidados()
    #st.write(df[df.columns[:-1]].head())
    gdf = gpd.GeoDataFrame(df,geometry='geometry')
    
    with st.beta_expander('Miramos el mapa nacional'):
        plot_mapita(gdf, regional=False)
    

    with st.beta_expander('Miramos una región en particular'):
        lista_regiones = gdf.region.unique()
        region_seleccionada = st.selectbox('Seleccionamos una región', lista_regiones)
        
        gdf_regional = gdf.query(f'region=="{region_seleccionada}"')
        plot_mapita(gdf_regional, figsize=(10,20))
    

def plot_mapita(gdf : gpd.GeoDataFrame,
                figsize=(20,40),
                regional=True):
    fig, ax = plt.subplots(figsize=figsize)
    gdf.plot(column='apruebo', ax=ax)
    if regional:
        gdf.apply(lambda x: ax.annotate(s=x.comuna, xy=x.geometry.centroid.coords[0], ha='center', color='white'),axis=1);

    ax.set_axis_off()
    st.pyplot(fig)
    
    

    
    
    
@st.cache
def cargamos_datos_votacion():
    df = pd.read_csv('BBDD Plebiscito 2020 - CPE UDLA en base a SERVEL, 2020 - 2020.csv')
    df.rename(columns={col: col.lower() for col in df.columns}, inplace=True)
    return df

@st.cache
def cargamos_datos_comuna():
    gdf_comunas = gpd.read_file('./Comunas/comunas.shp')
    gdf_comunas.rename(columns= {'cod_comuna': 'cod_com'}, inplace=True)
    gdf_comunas.rename(columns={col: col.lower() for col in gdf_comunas.columns}, inplace=True)
    return gdf_comunas

@st.cache
def cargamos_datos_consolidados(sacamos_islas : int = True):
    df = cargamos_datos_votacion()
    gdf = cargamos_datos_comuna()
    df_consolidado = df.merge(gdf[['region', 'provincia', 'geometry','cod_com']], on=['cod_com'])
    
    if sacamos_islas:
        islas = ['JUAN FERNANDEZ', 'ISLA DE PASCUA']
        df_consolidado = df_consolidado.query(f'comuna not in {islas}')
    return df_consolidado

    
    
main()