import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st
import pandas as pd
import numpy as np
import descartes

def main():
    st.title('Exploración de resultados del plebiscito para una nueva constitución en Chile :balloon:')
    st.subheader('Para ello utilizaremos la base de datos generada por ')
    st.write('Ojo, sacaremos Isla de Pascua y Juan Fernandez para hacer mejor los mapitas')
    
    
    df = cargamos_datos_consolidados()
    gdf = gpd.GeoDataFrame(df,geometry='geometry')
    
    
    st.markdown('**Seleccionamos una variable a mirar**')
    col1, col2 = st.beta_columns(2)
    with col1:
        columnas_posibles = ['apruebo','rechazo', 'blancos', 'nulos', 'p_apruebo', 'p_rechazo', 'part_2020', 'part_2017']
        col = st.selectbox('', columnas_posibles, index=4)
        
    
    with st.beta_expander('Miramos el mapa nacional'):
        plot_mapita(gdf, col, regional=False)
    

    with st.beta_expander('Miramos una región en particular'):
        lista_regiones = gdf.region.unique()
        region_seleccionada = st.selectbox('Seleccionamos una región', lista_regiones, index=12)
        
        gdf_regional = gdf.query(f'region=="{region_seleccionada}"')
        provincias = list(gdf_regional.provincia.unique())
        provincia_seleccionada = st.selectbox('Seleccionamos una provincia', ['todas'] + provincias)
        if provincia_seleccionada == 'todas':
            plot_mapita(gdf_regional, col, figsize=(10,20))
        else:
            gdf_provincial = gdf_regional.query(f'provincia=="{provincia_seleccionada}"')
            plot_mapita(gdf_provincial, col, figsize=(10,20))

    

def plot_mapita(gdf : gpd.GeoDataFrame,
                col : str,
                figsize=(20,40),
                regional=True):
    fig, ax = plt.subplots(figsize=figsize)
    gdf.plot(column=col, ax=ax, cmap='RdBu')
    if regional:
        gdf.apply(lambda x: ax.annotate(s=x.comuna, xy=x.geometry.centroid.coords[0], ha='center', color='white', ),axis=1);

    ax.set_axis_off()
    st.pyplot(fig)
    
    
    
    
@st.cache
def cargamos_datos_votacion():
    df = pd.read_csv('BBDD Plebiscito 2020 - CPE UDLA en base a SERVEL, 2020 - 2020.csv')
    df.rename(columns={col: col.lower() for col in df.columns}, inplace=True)
    for col in ['p_apruebo','p_rechazo', 'part_2017','part_2020']:
        df[col] = df[col].apply(lambda x: x.replace(',','.')).astype(float)
    for col in ['comuna']:
        df[col] = df[col].apply(lambda x: x.lower())
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
        islas = ['juan fernandez', 'isla de pascuaq']
        df_consolidado = df_consolidado.query(f'comuna not in {islas}')
    return df_consolidado

    
    
main()