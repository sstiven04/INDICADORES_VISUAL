import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd


st.set_page_config(layout='wide')
st.title("Indicador de Bienestar")
bienestar = pd.read_csv('bienestar.csv')
bienestardf2 = gpd.read_file('bienestar.csv')



tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Exploración Estadistica', 'Exploración gráfica', 'Pruebas de hipótesis', 'Análisis georreferenciado', 'Desarrollo de las Variables', 'Creado por:'])

with tab1:
    st.dataframe(bienestar.describe())

    t= """
    El valor promedio de cada variable refleja el desempeño de la 
    variable seleccionada en la región a lo largo del tiempo, tomando 
    en cuenta los 17 años y los 15 años estudiados. La tasa
    promedio de la prevalencia de desnutrición es del 7,27% de la población total,
    el porcentaje cultivable del área de tierra es del 6,94%, el acceso a la electricidad
    de acuerdo al porcetaje de la población es del 96,77%  y el desempleo sobre el 
    porcentaje de la población activa total es del 6,87%.
    Finalmente, la tasa de crecimiento promedio sobre la población total es del 32,05%.
    """
    st.text(t)

    resumen = {}

    resumen['Medias hambre'] = bienestar.groupby(['pais']).agg({'hambre':'mean'})
    resumen['Medias cultivos'] = bienestar.groupby(['año']).agg({'cultivos':'mean'})
    resumen['Medias electricidad'] = bienstar.groupby(['año']).agg({'electricidad':'mean'})
    resumen['Medias desempleo'] = bienestar.groupby(['pais']).agg({'desempleo':'mean'})
    resumen['Medias poblacion'] = bienestar.groupby(['pais']).agg({'poblacion':'mean'})
    num_tables = len(resumen)
    num_columns = 5
    num_rows = (num_tables + num_columns - 1) // num_columns
    for i in range(num_rows):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            index = i * num_columns + j
            if index < num_tables:
                titulo, serie = list(resumen.items())[index]
                with cols[j]:
                    st.subheader(f"{titulo}")
                    st.dataframe(serie.reset_index())
    Textot="""
    Se observa que para la variable de cultivos que evalua la cantidad de terrenos cultivables 
    para cada país, presenta un incremento año tras año en el periodo de tiempo evaluado (2002 - 2019);
    se evidencia también que es Bolivia uno de lo paises con mayor tasa de desnutrición del 19.7% sobre 
    el total de su población y los países con menor las tasas más bajas de desnutrición son Canada y 
    Estados unidos con el 2.50% sobre el total de la de cada uno. 

    En terminos de energía electrica, se evidencia que para el periodo en estudio hubo un incremento en el 
    porcentaje de la población con acceso a la electricidad pasando de una media del 93.09% en el año 2002 
    a una media estimada del 99.12% en el año 2019, adicionalmente se observó que los pises con mayor 
    incemento en la población en la región fueron Costa Rica (90.73%), seguido de Ecuador (60.9%) y 
    Colombia (40.60%). Es importante mencionar que aunque durante dicho periodo aumentó la población 
    para estos países el desempleo atacó a otros como fue el caso de Colombia, Brasil, Venezuela y Argentina.
    """
    st.text(Textot)

    st.subheader('Mosaico de Mapas de Calor')

    years = bienestar['año'].unique()
    
    columnas_numericas = bienestar.select_dtypes(include=['number'])
    num_columns = 4 
    num_rows = (len(years) + num_columns - 1) // num_columns
    for i in range(num_rows):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            index = i * num_columns + j
            if index < len(years):
                year = years[index]
                with cols[j]:
                    st.subheader(f"Mapa de Calor para el Año {year}")
                    bienestar_year = columnas_numericas[columnas_numericas['año'] == year]
                    corr_matrix = bienestar_year.corr()
                    fig, ax = plt.subplots()
                    sns.heatmap(corr_matrix, annot=True, cmap="Spectral", linewidths=0.5)
                    st.pyplot(fig)
    x= """
    El gráfico de calor muestra cómo las variables elegidas han interactuado a lo largo de 
    los años. Es evidente que estas interacciones han sido consistentes durante los 17 años,
    y en su mayoría, las correlaciones entre ellas son bajas. La excepción es la relación 
    entre el acceso de la población a la electricidad  y al desempleo, que ha mantenido una 
    correlación más alta de 0.8 a lo largo de todos los años.
    """
    st.text(x)
    
with tab2:   
    st.subheader('Análisis gráfico')
     
    fig_1 = px.scatter(bienestar, x="año", y="hambre", color="pais",
                 size='poblacion', hover_data=['hambre'])
    st.plotly_chart(fig_1)
    x= """
    En el gráfico anterior, se evidencia que en el caso de Venezuela, a pesar de ser un país 
    cuya población ha disminuido, la desnutricón ha aumentado exponencialmente desde el año 2014, 
    mientras que en el caso de Bolivia, un país el cual ha tenido una población bastante reducida 
    durante el periodo evaluado, ha logrado disminuir sus índices de desnutricón de forma significativa. 
    """

    fig_2 = px.box(bienestar, x="año", y="electricidad")
    fig_2.show()
    st.plotly_chart(fig_2)

    x= """ 
    En el presente gráfico podemos evidenciar que entre los años 2002 al 2007 existia una gran diferencia 
    en el acceso a la electricicdad entre los países evaludos, lo que quiere decir que mientras unos hasta 
    estaban empezando a implementar y mejorar sistemas de electricidad habian otros que probablemente ya 
    llevaban varios años haciendo uso de esta.
    """

    fig_3 = px.box(bienestar, x="año", y="desempleo")
    fig_3.show()
    st.plotly_chart(fig_3)

    x= """ 
    En el presente diagrama de cajas y bigotes en el cual se busca analizar el desempleo por años, se 
    encuentra una particularidad para el año 2002, pues se logra examinar que mientras unos países cuentan 
    con una tasa de desempleo baja, otros registran tasas significativamente altas. 
    """

    fig_7 = px.scatter(bienestar, x="año", y="cultivos", color="pais",
                 size='poblacion', hover_data=['cultivos'])
    fig_7.show()
    st.plotly_chart(fig_7)

    x= """ 
    En el gráfico de cultivos, es posible considerar que la tendencia de la mayoría de los países a cultivar 
    no cuenta con mayores variaciones, es decir que puede presentarse alguna actividad estable en las tierras 
    cultivables. Sin embargo, Uruguay y Paraguay son los países que más presentan variaciones en cultivos con los años.
    """
    fig_8 = px.scatter(bienestar, x="año", y="electricidad", color="pais", symbol="pais")
    fig_8.show()
    st.plotly_chart(fig_8)
    
    x= """ 
    Para el diagrama de dispersión en electricidad, es importante identificar que el porcentaje mínimo alcanzado hasta 
    el último año (2019) supone un 95.08% de la población con acceso a electricidad, lo cual brinda un panorama positivo, 
    pues un buen número de la población tiene acceso a este servicio. Por otro lado, Bolivia y Perú son los países que
    más han presentado avances, pues empezaron el 2002 debajo del promedio.
    """

with tab3:   
    st.subheader('Prueba de hipótesis')

    st.subheader('Variable #1: Tasa de desempleo')
    latex_formula = r"H_0: \text{No hay evidencia suficiente para afirmar una diferencia significativa entre los niveles de desempleo entre Colombia y SuramericaExiste una diferencia significativa en cuanto a niveles de desempleo entre Colombia y Suramerica}"
    latex_formula += r", \\ H_1: \text{'Existe una diferencia significativa en cuanto a niveles de desempleo entre Colombia y Suramerica'}"
    st.latex(latex_formula)
    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las 17 pruebas se obtuvo un valor p value menor 
    a 0.05, por lo que se rechaza la hipótesis nula. Con esto se puede decir que 
    no existe una diferencia significativa en las tasas de desempleo 
    entre Colombia y los paises de Suramérica.
    """
    st.text(texto_simple)

    latex_formula = r"H_0: \text{No hay evidencia suficiente para afirmar una diferencia significativa entre los niveles de desempleo entre Colombia y Norteamerica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en cuanto a niveles de desempleo entre Colombia y Norteamerica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las pruebas de 2002 a 2008 y de 2017 a 2019 se obtuvo un valor 
    p value menor a 0.05 por lo que se rechaza la hipótesis nula. Con esto se puede decir que 
    para tales años no existió una diferencia significativa en las tasas de desempleo entre Colombia y los paises de Norteamérica. 

    Sin embargo a partir del año 2009 hasta el 2017 se obtuvo un valor p value mayor a 0.05,
    por lo que no se puede rechazar la hipótesis nula, lo que indica que existe
    diferencia significativa en las tasas de desempleo entre Colombia y Norteamérica para tal 
    periodo de tiempo.
    """
    st.text(texto_simple)

    st.subheader('Variable #2: Electricidad')
    latex_formula = r"H_0: \text{No hay evidencia suficiente para afirmar una diferencia significativa entre los niveles de acceso a la electricidad entre Colombia y Suramerica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en cuanto a los niveles de acceso a la electricidad entre Colombia y Suramerica}"
    st.latex(latex_formula)
    texto_simple = """
    Se arealizó la prueba de hipótesis para cada uno de los años y se obtuvieron p values por encima de 0.05 por esta razón 
    no se rechaza la hipótesis nula lo cual quiere decir que no hubo diferencias significativas entre colombia y suramerica 
    términos de acceso a la alectricidad en la población
    """
    st.text(texto_simple)

    latex_formula = r"H_0: \text{No hay evidencia suficiente para afirmar una diferencia significativa entre los niveles de acceso a la electricidad entre Colombia y Norteamérica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en cuanto a los niveles de acceso a la electricidad entre Colombia y Norteamérica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y de los años 2002 al 2018 las pruebas arrojaron un valor p value menor a 0.05,
    por lo que se rechaza la hipótesis nula lo que indica que hay 
    diferencia significativa en el acceso a la electricidad entre la población de Colombia y Norteamérica para tal perioado. Mientras que 
    para el año 2019 se obtuvo un p value por encima de 0.05 lo cual indica que no se rechaza la hipotesis nula y que 
    para tal año no hubo diferencia significativa en terminos de acceso a la electricidad entre la población de Colombia y los países de Norte América.
    """
    st.text(texto_simple)

    st.subheader('Variable #3: Cultivos')
    latex_formula = r"H_0: \text{No hay evidencia suficiente para afirmar una diferencia significativa en cuanto a hectareas de tierras cualtivables entre Colombia y Suramerica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en cuanto a hectareas de tierras cualtivables entre Colombia y Suramerica}"
    st.latex(latex_formula)
    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las 17 pruebas se obtuvo un valor p value menor a 0.05,
    por lo que se rechaza la hipótesis nula lo que indica que hay evidencia suficiente para afirmar 
    una diferencia significativa en cuanto a hectareas de tierras cualtivables entre Colombia y Suramerica
    """
    st.text(texto_simple)

    latex_formula = r"H_0: \text{No hay evidencia suficiente para afirmar una diferencia significativa en cuanto a hectareas de tierras cualtivables entre Colombia y Norteamérica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en cuanto a hectareas de tierras cualtivables entre Colombia y Norteamérica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las 17 pruebas se obtuvo un valor p value mayor a 0.05,
    por lo que no se puede rechazar la hipótesis nula lo que indica que no hay 
    diferencia significativa en cuanto a hectareas de tierras cualtivables  entre Colombia y Norteamérica.
    """
    st.text(texto_simple)

    st.subheader('Variable #4: Desnutrición')
    latex_formula = r"H_0: \text{No hay evidencia suficiente para afirmar una diferencia significativa entre los niveles de desnutrición entre Colombia y Suramerica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en cuanto a niveles de desnutrición entre Colombia y Suramerica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las pruebas de 2002 a 2009 y de 2013 a 2019
    se obtuvo un valor p value mayor a 0.05,por lo que no se puede rechazar 
    la hipótesis nula lo que indica que no existe una diferencia significativa 
    en cuanto a niveles de desnutrición entre Colombia y Suramerica
    Sin embargo en los años 2010 a 2012 se obtuvo un valor p value menor a 0.05 
    por lo que se rechaza la hipótesis nula. Esto quiere decir que 
    existe una diferencia significativa en cuanto a niveles de desnutrición 
    entre Colombia y Suramerica para ese periodo de tiempo.
    """
    st.text(texto_simple)

    latex_formula = r"H_0: \text{No hay evidencia suficiente para afirmar una diferencia significativa entre los niveles de desnutrición entre Colombia y Norteamérica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en cuanto a niveles de desnutrición entre Colombia y Norteamérica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las 17 pruebas se obtuvo un valor p value mayor a 0.05,
    por lo que no se puede rechazar la hipótesis nula lo que indica que no hay 
    diferencia significativa en la tasa de denutrición entre Colombia y Norteamérica.
    """
    st.text(texto_simple)

    st.subheader('Variable #5: Población')
    latex_formula = r"H_0: \text{No hay evidencia suficiente para afirmar una diferencia significativa entre los niveles de población entre Colombia y Suramerica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en cuanto a niveles de población entre Colombia y Suramerica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las 17 pruebas se obtuvo un valor p value menor 
    a 0.05, por lo que se rechaza la hipótesis nula. Esto quiere decir que 
    existe una diferencia significativa en cuanto a niveles de población entre Colombia y Suramerica.
    """
    st.text(texto_simple)

    latex_formula = r"H_0: \text{No hay evidencia suficiente para afirmar una diferencia significativa entre los niveles de población entre Colombia y Norteamerica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en cuanto a niveles de población entre Colombia y Norteamerica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las 17 pruebas se obtuvo un valor p value mayor a 0.05,
    por lo que no se puede rechazar la hipótesis nula lo que indica que no hay 
    evidencia suficiente para afirmar una diferencia significativa entre los niveles de población entre Colombia y Norteamerica.
    """
    st.text(texto_simple)
    
with tab4:
    st.title("Mapa General")
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    bienestar2.plot(
    cmap="plasma", 
    ax=ax)
    ax.set_axis_off()
    st.pyplot(fig)

    st.divider()
    fig, axs = plt.subplots(1, 5, figsize=(20, 4))
    columns = ["electricidad", "desempleo", "poblacion", "cultivos", "hambre"]
    titles = ["Acceso a la electricidad", "Desempleo total", "Población total", "Tierras cultivables", "Prevalencia de desnutrición"]

    for i, (column, title) in enumerate(zip(columns, titles)):
        ax = axs[i]
        bienestar2.plot(
            column=column,
            scheme="Quantiles",
            cmap="plasma",
            legend=True,
            legend_kwds={"fmt": "{:.0f}"},
            ax=ax
        )
        ax.set_title(title)
        ax.set_axis_off()
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    st.subheader('Transformación por variables')
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    axs = axs.flatten()
    years = ["2002-2004", "2005-2009", "2010-2014", "2015-2019"]
    bienestar2['año'] = bienestar2['año'].astype(int)
    
    for i, ax in enumerate(axs):
        year_range = years[i]
        start_year, end_year = map(int, year_range.split("-"))
        desarrollo_años = bienestar2[(bienestar2['año'] >= start_year) & (bienestar2['año'] <= end_year)]
    
        desarrollo_años.plot(
            column="poblacion",
            scheme="Quantiles",
            cmap="plasma",
            legend=True,
            legend_kwds={"fmt": "{:.0f}"},
            ax=ax,
        )
    
        ax.set_axis_off()
        ax.set_title(f"Población de {year_range} en Países de América")
    plt.suptitle("Variación de la población en América entre los años 2002 y 2019")
    plt.tight_layout()
    st.pyplot(fig)

    texto_simple = """
    Teniendo en cuenta el gráfico anterior podemos observar que de 2002 a 2019 Ecuador, México 
    y Costa Rica registraban una población superior a la de otros países de la región, mientras
    que para el periodo de 2005 a 2009 Paraguay tuvo un aumento en su población.Para el periodo 
    del 2015 a 2019 la población en Venezuela disminuyó debido al aumento de la inflación, la 
    cual alcanzo el punto más alto en la historia de este país. 
    """
    st.text(texto_simple)

    st.divider()
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    axs = axs.flatten()
    years = ["2002-2004", "2005-2009", "2010-2014", "2015-2019"]
    desarrollo_años = bienestar2[(bienestar2['año'] >= start_year) & (bienestar2['año'] <= end_year)]

    for i, ax in enumerate(axs):
    
        year_range = years[i]
        start_year, end_year = map(int, year_range.split("-"))
        desarrollo_años = bienestar2[(bienestar2['año'] >= start_year) & (bienestar2['año'] <= end_year)]
    
        desarrollo_años.plot(
            column="Desempleo",
            scheme="Quantiles",
            cmap="plasma",
            legend=True,
            legend_kwds={"fmt": "{:.0f}"},
            ax=ax,
        )
    
        ax.set_axis_off()
        ax.set_title(f"Desempleo de {year_range} en países de América")
    plt.suptitle("Comportamiento del desempleo en América entre los años 2002 y 2019")
    plt.tight_layout()
    st.pyplot(fig)

    texto_simple = """
    Con base en el gráfico, es posible observar que en el primer periodo de tiempo Venezuela presentó el 
    indicador más alto en desempleo y Mexico, Peru, y Bolivia presentaron los más bajos, así mismo para el segundo periodo ( 2005-2009) 
    se registra un aumento en desempleo en los paíss de la región a excepción de Argentina y Paraguay y Venezuela disminuyó sus índices.
    Para los dos últimos periodos, en la mayoría de países de América del Sur se registra un aumento en el desempleo.
    """
    st.text(texto_simple)

    st.divider()
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    axs = axs.flatten()
    years = ["2002-2004", "2005-2009", "2010-2014", "2015-2019"]
    bienestar2['año'] = bienestar2['año'].astype(int)

    for i, ax in enumerate(axs):
        year_range = years[i]
        start_year, end_year = map(int, year_range.split("-"))
        desarrollo_años = bienestar2[(bienestar2['año'] >= start_year) & (bienestar2['año'] <= end_year)]
    
        desarrollo_años.plot(
            column="hambre",
            scheme="Quantiles",
            cmap="plasma",
            legend=True,
            legend_kwds={"fmt": "{:.0f}"},
            ax=ax,
        )
    
        ax.set_axis_off()
        ax.set_title(f"Nivel de desnutricón de {year_range} en Países de América")
    plt.suptitle("Comportamiento de la desnutrición en América entre los años 2002 y 2019")
    plt.tight_layout()
    st.pyplot(fig)

    texto_simple = """
    En los 4 periodos, Canadá y Estados Unidos registraron los indices más bajos en cuanto a desnutrición,
    por su parte Bolivia registró los niveles más altos, es importante destacar que Venezuela tuvo un 
    cambio más abrupto entre los países de la región pasando de tener los indices más bajos a los más altos en desnutrición.
    Finalmente, se observó que el único país de suramérica en tener niveles bajos de desnutrición fue Uruguay.  
    """
    
with tab5:

    st.title("Indicador")

    texto_simple = """

    Los mapas proporcionan una representación visual del nivel de bienestar en los países de América según los 
    resultados del indicador elaborado. Además, en el análisis georreferenciado, se utilizaron los mismos 
    intervalos de tiempo, lo que permite observar los cambios a lo largo de los años, desde 2002 hasta 2019.
    Según este indicador, antes de la crisis financiera mundial de 2008, es decir, durante el período de 
    2002-2007, los países de América con un mayor nivel de bienestar eran Estados Unidos y Canadá, mientras 
    que Bolivia tenía el nivel más bajo. Durante y después de la crisis financiera, es decir, entre 2008 y 
    2011, Canadá, Perú y Uruguay se destacaron como los países con un mayor nivel de bienestar, mientras que 
    Colombia y Bolivia se encontraban entre los de menor bienestar. En el período de 2012 a 2015, Estados 
    Unidos, Canadá y Perú seguían liderando en cuanto al bienestar, mientras que Colombia, Venezuela y Bolivia 
    continuaban registrando resultados menos favorables. Finalmente, entre 2016 y 2019, Estados Unidos y Canadá 
    mantenían su posición en la cima en términos de bienestar, pero Colombia, Ecuador, Venezuela y Paraguay 
    experimentaron un deterioro en su bienestar general, lo que indica una tendencia preocupante en la región.
    """
    st.text(texto_simple)


with tab6:
    x="""
    - Daniela Gonzalez
    - Sofia Gomez
    - Estiven Pira
    """
    st.text(x)
    

    
