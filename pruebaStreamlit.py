import re
import graphviz
import streamlit as st

@st.cache_resource
def cargar_datos():
    grafo = graphviz.Digraph("Carrera", filename="Digraph.gv")
    with open("estado.txt") as file:
        estado=int(file.readlines()[0])
    if not estado:
        # Creación de nodos
        grafo.node("0","Administracion de sistemas informaticos", category="Programa Curricular", style="filled", fillcolor="lightblue")
        grafo.node("1","Introduccion a ASI", category="Fundamentales Obligatorias", style="filled", fillcolor="red")
        grafo.node("2", "Fundamentos de economia", style="filled", fillcolor="red")
        grafo.node("3", "Sistemas de Informacion", style="filled", fillcolor="red")
        grafo.node("4", "Planeacion de sistemas de Informacion", style="filled", fillcolor="red")
        grafo.node("6","Fundamentos de programacion", style="filled", fillcolor="red")
        grafo.node("7", "Programacion Orientada a Objetos", style="filled", fillcolor="red")
        grafo.node("8", "Estructuras de datos", style="filled", fillcolor="red")
        grafo.node("9", "Analisis y diseno de algoritmos", style="filled", fillcolor="red")
        grafo.node("10", "Ingenieria de Software I", style="filled", fillcolor="red")
        grafo.node("11", "Calculo diferencial", style="filled", fillcolor="red")
        grafo.node("12", "Calculo integral", style="filled", fillcolor="red")
        grafo.node("13", "Estadistica I", style="filled", fillcolor="red")
        grafo.node("14", "Introduccion a la epistemologia", style="filled", fillcolor="red")

        # Creación de aristas
        grafo.edge("0", "1")
        grafo.edge("1", "3")
        grafo.edge("3", "4")
        grafo.edge("4", "10")
        grafo.edge("0", "6")
        grafo.edge("6", "7")
        grafo.edge("7", "8")
        grafo.edge("8", "9")
        grafo.edge("9", "10")
        grafo.edge("0", "11")
        grafo.edge("11", "12")
        grafo.edge("12", "13")
        grafo.edge("0", "14")
        grafo.edge("1", "2")
    else:
        with open("Digraph.gv") as file:
            datos=file.read()
        st.write(grafo.source)
    grafo.save()
    return grafo

grafo=cargar_datos()

asignGrafo={"----":0}
for nodo in grafo:
    ind=nodo.find("[")
    if ind!=-1:
        infoAsig={}
        id=nodo[0:ind]
        parte2=nodo[ind:][1:-2]
        cargaUtil=re.split('" ', parte2)
        for valor in cargaUtil:
            if valor.count(" ")!=0 and valor.count('"')==0:
                subValores=valor.split()
                for subV in subValores:
                    lista=subV.split("=")
                    tipo=lista[0]
                    dato=lista[1]
                    infoAsig[tipo]=dato
            else:
                lista=valor.split("=")
                tipo=lista[0]
                dato=lista[1].replace('"','')
                infoAsig[tipo]=dato
        if infoAsig.get("category",None)=='Programa Curricular':
            continue
        nombreAsig=cargaUtil[0].replace("label=","").replace('"','')
        asignGrafo[nombreAsig]=[id, infoAsig]

# Crea el grafo unidireccional
st.title("Ruta de carrera")
st.write("En esta sección podrás ver todas las materias que componen tu programa curricular" 
        " e ir seleccionando aquellas que has visto para trazar tu recorrido.")

opcion=st.selectbox("Asignatura", asignGrafo)
if opcion and asignGrafo[opcion]:
    st.write("Este el el grafo", grafo)
    st.write("antes de")
    datos=asignGrafo[opcion]
    nombre=int(datos[0])
    st.header(nombre)
    diccInfo=datos[1]
    nuevoGrafo=graphviz.Digraph()
    nuevoGrafo.node(str(nombre), opcion, style="filled", fillcolor="green")
    for nodo in grafo.body:
        texto=nodo.strip().split()
        if not (texto[0]==str(nombre) and texto[1][0]=="["):
            nuevoGrafo.body.append(nodo)
            st.write(nodo)
    grafo=nuevoGrafo
    grafo.save()
    grafo.format="png"
    grafo.render()
st.header("Esquema:")
with open("Digraph.gv") as archivo:
    imagen=archivo.read()
st.graphviz_chart(imagen)

st.write(asignGrafo)
st.write(grafo.body)
