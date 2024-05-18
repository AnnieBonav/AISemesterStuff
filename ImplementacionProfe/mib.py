#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#title          :Bayesiano_Discreto.ipynb
#description    :Motor de inferencia bayesiano para variables discretas.
#author         :Dr. Jorge Hermosillo Valadez
#date           :20201104
#version        :1.0
#usage          :investigación
#notes          :permiso acordado para ser utilizado para fines académicos
#                conservando este encabezado
#python_version :3.5
#==============================================================================

#Librerías estándar
import numpy as np
from itertools import product,chain
from operator import itemgetter
from collections import defaultdict
import pandas as pd
from math import floor

# ## Funciones de entrada/salida de datos
def genera_espacio(entrada: list)->list:
    #=============================================================================
    # Función para generar el espacio de valores posibles mediante el producto
    # cartesiano de los valores de las variables (entrada)
    # entrada: - lista de valores posibles por cada variable de entrada.
    # salida: - L: lista de n-tuplas con todas las combinaciones
    #           posibles de los valores de las variables.
    # ejemplo:
    # entrada = [0,1]
    # L = [(0,0),(0,1),(1,0),(1,1)]
    #==============================================================================
    L=[]
    #print("Entrada: ", entrada)
    for element in product(*entrada):
        L.append(element)
    return L

def genera_llaves(variables: list)-> list:
    #===============================================================================
    # Función para generar las llaves de entrada a un diccionario de probabilidades
    # entrada: - lista de variables (objetos tipo Var).
    # salida: - llaves: lista de n-tuplas con todas las combinaciones
    #           posibles de los valores de las variables de entrada.
    # ejemplo:
    # variables = [A,B] ; con A=[0,1], B=[0,1]
    # llaves = [(['A'], ['B'], 0, 0)
    #           (['A'], ['B'], 0, 1),
    #           (['A'], ['B'], 1, 0),
    #           (['A'], ['B'], 1, 1)]
    #=================================================================================
    llaves=[]
    # print(variables)
    entrada=[i.values for i in variables]
    #entries=genera_espacio(entrada)
    entries=[]
    for element in product(*entrada):
        entries.append(element)
    l=[]
    for v in variables:
        l.append(v.name)
    l=tuple(list(chain(*product(l))))
    for i in range(len(entries)):
        x=list(chain(*(l,entries[i])))
        llaves.append(tuple(x))
    return llaves

def genera_llaves_cond(var,entrada,indep):  
    #==================================================================================
    # Genera las llaves de entrada al diccionario de una distribución condicional.
    # Si son varias variables de entrada, genera las combinaciones posibles.
    # entradas: - var: variable o lista de variables (variables dependiente de salida)
    #           - entrada: combinación de valores de la entrada a la tabla
    #           - indep: lista de variables independientes (entradas de la tabla)
    # salida: - salida: lista de n-tuplas con las combinaciones de salida
    #         - llaves: lista de n-tuplas con las combinaciones de entrada
    #==================================================================================
    salida=[]
    llaves=[]
    #listVar=False
    try:
        if isinstance(var,list):
            listVar=True
        else:
            listVar=False
    except:
        listVar=False
    if not listVar:
        nombre = var.name
        for i in range(len(var.values)):
            salida.append((nombre,var.values[i]))
    else:
        salida=genera_llaves(var)
    l=[]
    for v in indep:
        l.append(v.name)
    l=tuple(list(chain(*product(l))))
    for i in range(len(entrada)):
        x=list(chain(*(l,entrada[i])))
        llaves.append(tuple(x))
    # print('salida: ',salida, ' llaves: ',llaves)
    return salida, llaves

def carga_tabla(var,tabla):
    #================================================================
    # Función para cargar valores de probabilidad en un diccionario
    # entrada: - apuntador a la variable (objeto tipo Var)
    #          - lista o diccionario de valores de probabilidad
    # salida: - diccionario de valores de probabilidad para Var
    #================================================================
    dico={}
    keys=genera_llaves(var)
    #print(keys)
    if isinstance(tabla,list):
        for k,v in zip(keys,tabla):
            dico[k]=v
    elif isinstance(tabla,dict):
        for k,v in zip(keys,list(tabla.values())):
            dico[k]=v
    else:
        print('Tabla debe ser dict o list')
    return dico


def carga_tabla_cond(var,entrada,indep,tabla):
    #==================================================================================
    # Función para cargar valores de probabilidad condicional en un diccionario
    # entrada: - var: apuntador a la variable de salida (objeto tipo Var)
    #          - entrada: lista de n-tuplas con combinaciones de los valores de entrada
    #          - indep: lista de variables (tipo Var) independientes (entrada)
    #          - tabla: lista o diccionario de valores de probabilidad de la salida
    # salida: - diccionario de valores de probabilidad para var
    # ejemplo: ver función "genera_llaves"
    #===================================================================================
    dico={}
    salidas,keys=genera_llaves_cond(var,entrada,indep)
    #print(salidas,keys)
    if isinstance(tabla,list):
        for k,v in zip(keys,tabla):
            tab={}
            for i,s in enumerate(salidas):
                tab[s]=v[i]
            dico[k]=tab
    elif isinstance(tabla,dict):
        for k,v in zip(keys,list(tabla.values())):
            tab={}
            for i,s in enumerate(salidas):
                tab[s]=v[i]
            dico[k]=tab
    else:
        print('Tabla debe ser dict o list')
    return dico
    

def genera_vars_llaves(variables):
    #=============================================================================
    # Función para generar el espacio de valores posibles mediante el producto
    # cartesiano de los valores de las variables (entrada)
    # entrada: - entrada: variables de entrada.
    # salida: - llaves: lista de n-tuplas con todas las combinaciones
    #           posibles de los valores de las variables.
    #         - var_list: lista de combinaciones por cada variable
    # ejemplo:
    # A=[0,1], B=[0,1]
    # llaves= [('A', 'B', 0, 0), ('A', 'B', 0, 1), ('A', 'B', 1, 0), ('A', 'B', 1, 1)]
    # var_list=[('A', 0), ('A', 1), ('B', 0), ('B', 1)]
    #==============================================================================
    var_list=[]
    llaves=genera_llaves(variables)
    for v in variables:
        var_list.append(genera_llaves([v]))    
    var_list=list(chain.from_iterable(var_list)) #flat list of lists
    return llaves, var_list

    
def look_up_table(variables,espacio):
    #=============================================================================
    # Función para recuperar la intersección entre las variables y el espacio 
    # cartesiano de entrada
    # entrada: - variables: variables de búsqueda.
    #          - espacio: lista de n-tuplas con todas las combinaciones
    #           posibles del espacio de búsqueda.
    # salida: - lista de las variables con sus valores que tienen intersección con
    #           el espacio de búsqueda.
    # ejemplo:
    # A=[0,1], C=[0,1,2]
    # variables = [A,C]
    # espacio = ([A,C,0,0],[A,C,0,1],[A,C,0,2],[A,C,1,0],[A,C,1,1],[A,C,1,2])
    # lkt = [('A', 1), ('C', 1), ('A', 0), ('C', 0), ('C', 2)]
    #==============================================================================
    def genera_mascaras(va):
        L=[]
        n=len(va)
        cadena='1'*2*n
        for i in range(n):
            mascara=[]
            a=cadena[:i]+'0'+'1'*(n-(i+1))
            a=a*2
            mascara.extend(a)
            mascara=np.array(mascara,dtype=int)
            L.append(mascara)
        return L

    def get_masked_array(key,mask):
        y=list(key)
        z=[]
        for i in range(len(mask)):
            if mask[i]==0:
                z.append(y[i])
        return z
    lkt=[]
    v=[]
    for va in variables:
        v.append(va.name)
    mascaras=genera_mascaras(variables)
    for k in espacio:
        for m in mascaras:
            if set(v).issubset(list(k)):
                z=get_masked_array(k,m)
                if all(z) not in lkt:
                    lkt.append(tuple(z))
    lkt=list(set(lkt))
    return lkt

def filter(keys,v,thevars):
    ###################################################################
    # Function to look for a matching between the input keys (dico_Y) 
    # and the variable-value pair in turn (llave from dico_X)
    #  - Look first for variable name matching
    #  - Look next for variable value matching
    #  - If pattern matches return keys matching
    ###########################################################
    m=[]
    # print('keys: ',keys)
    # print('filter criterion: ',v)
    # print('the variable names: ', thevars)
    n=len(keys[0])
    in_v=[]
    foundMatch=False
    for x in v:  #x contains the (variable,value) pair
        # print('x = ',x)
        for i in range(n):
            # print(f'keys[0][i={i}]=',keys[0][i])
            if keys[0][i] == x[0]:
                foundMatch=True
                # print(f'FOUND VARIABLE MATCH IN KEYS!!!! --> keys[0][i={i}]==x[0]={x[0]}')
                i_v=i
            if foundMatch:
                # if isinstance(keys[0][i],int):
                #     print(f'______FOUND INT AT_____: i+i_v={i}+{i_v}')
                #     in_v.append(i+i_v)
                #     # in_v.append(i_v)
                #     break
                if keys[0][i] not in thevars:
                    # print(f'______FOUND VALUE AT_____: i+i_v={i}+{i_v}')
                    in_v.append(i+i_v)
                    # in_v.append(i_v)
                    break
    if foundMatch:
        # print(f'looking for value matching, in_v={in_v}')
        foundMatch=False
        for j,x in enumerate(v):
            # print(f'in cycle on v--> j={j},x={x}')
            for k in keys:
                # print(f'looking into {k}[{in_v}[{j}]]=={x}[1]')
                if k[in_v[j]]==x[1]:
                    foundMatch=True
                    # print('FOUND MATCH IN PATTERN!!!!')
                    if k not in m:
                        m.append(k)
        if foundMatch:
            return m
    return None


def filter_rec(candidates,variables,v):
    ###################################################
    #Canidates are the search space
    #variables are filtering terms.
    # the filter criterion is the key searched for
    ####################################################
    # print('candidates: ',candidates)
    # print('key searched for: ',v)
    # print('variables: ',variables)
    n=len(v)
    i_v=0
    i_n=0
    terms=[]
    foundVar=False
    match=False
    Idx=True
    try:
        x=variables.pop()
    except IndexError:
        x=[]
    if x!=[]:
        # print('$$$$$$$$ variables not void $$$$$$$$$')
        for i in range(n):
            if v[i] == x[0]:
                foundVar=True
                i_v=i
                # print(f'FOUND VARIABLE MATCH IN KEYS!!!! --> v[i={i}]==x[0]={x[0]}')
            if isinstance(v[i],int) and Idx==True:
                i_n=i
                Idx=False
            if foundVar and i==i_v+i_n:
                if v[i]==x[1]:
                    # print(f'FOUND VALUE MATCH IN KEYS!!!! --> v[i={i}]==x[1]={x[1]}')
                    match=True
                    #print('match: ',v,x)
                    break
        if match:
            match=False
            foundVar=False
            foundIdx=False
            for k in candidates:
                for i in range(len(k)):
                    if k[i] == x[0]:
                        i_v=i
                        foundVar=True
#                         print('foundVar: ',k,i,x)
                    if foundVar:
                        if isinstance(k[i],int) and not foundIdx:
                            i_n=i+i_v
                            foundIdx=True
#                             print('Index of value match at: ',i,i_v,i_n)
                        if foundIdx and k[i_n]==x[1]:
#                             print('found A TERM MATCH: ',k,x)
                            match=True
                            if k not in terms:
                                terms.append(k)
                                break
            candidates=filter_rec(terms,variables,v)
        else:
            candidates=filter_rec(candidates,variables,v)
        return candidates
    else:
        #print('No more vars, returning: ',candidates)
        return candidates


def find_match(keys,k,thevars):
    #print('matching... ',keys,k)
    return filter(keys,[k],thevars)

def find_reverse_match(keys,k):
#     print('matching... ',keys,k)
    m=[]
    n=len(k)
    in_v=[]    
    foundMatch=False
    for x in keys:
        for i in range(n):
            if k[i] == x[0]:
                foundMatch=True
                i_v=i
            if foundMatch:
                if isinstance(k[i],int):
                    in_v.append(i+i_v)
                    break
    if foundMatch:
        foundMatch=False
        for j,x in enumerate(keys):
#             print('x is ====> {0}, and k is ====> {1}'.format(x,k))
            if k[in_v[j]]==x[1]:
#                 print('MATCH OK!!!')
                foundMatch=True
                if x not in m:
                    m.append(x)
#         print('The ouput of the matching process is: ',m)
        if foundMatch:
            return m
    return None

    
def compute_conditional_probs(dico_Y,dico_X,searched,known,r=0):
    #######################################################################
    # The problem is to compute the division dico_Y/dico_X
    # dico_X has less variables than dico_Y
    # So, keys in dico_X (llaves) are used as patterns to be found in
    # dico_Y (keys_Y).
    # However, if dico_X's keys has more than one variable
    # the patterns of combination pairs (variables,values)
    # have to be detected, so they can be found in dico_Y
    # The names of the variables are passed, so as to differentiate
    # the values from the names of the variables, as values 
    # may be other thing than integers (e.g. real numbers or categorical).
    #######################################################################
    Sn=[a.name for a in searched]
    Kn=[a.name for a in known]
    thevars=Sn+Kn
    # print(f'Searched vars: {Sn}, Known vars: {Kn}')
    entrada=[i.values for i in known]
    entrada=genera_espacio(entrada)
    # print('Entries: ',entrada)
    salida,llaves=genera_llaves_cond(searched,entrada,known)
    # print('salida={0}, llaves={1}'.format(salida,llaves))
    dico={}
    keys_Y=list(dico_Y.keys())
    # print('dico_Y keys: ',keys_Y)
    for k in llaves:
        # print('looking for match of {0} with {1}'.format(k,keys_Y))
        # km=find_match(keys_Y,k,Sn+Kn)
        Srd_vars = look_up_table(searched+known,dico_Y.keys())
        # print(f'Srd_vars ====>>> {Srd_vars}')
        km=filter_rec(dico_Y.keys(),Srd_vars,k)
        # print('match found is ',km)
        dO={}
        for i,o in enumerate(salida):
            # print(f'Computing output dO[{o}]=dico_Y[{km[i]}]/dico_X[{k}]={dico_Y[km[i]]}/{dico_X[k]}')
            # print(f'dO[{o}]={dico_Y[km[i]]/dico_X[k]}')
            if r!=0:
                dO[o]=round(dico_Y[km[i]]/dico_X[k],r)
            else:
                dO[o]=dico_Y[km[i]]/dico_X[k]
        dico[k]=dO
    return dico

def find_values(refKey,matchKey,dico):
    ma=None
    m=find_reverse_match([matchKey],refKey)
    if m is not None:
        ma=dico[matchKey]
#     print('FIND VALUES RETURNS::::::: ',ma)
    return ma

def checkMatch(kand,sand,v,variables):
#     print('Receiving K={0}, S={1}, v={2}, vars={3}'.format(kand,sand,v,variables))
    n=len(v)
    i_v=0
    i_n=0
#    terms_k=[]
#    terms_s=[]
    foundVar=False
    match=False
    Idx=True
    for x in variables:
        for i in range(n):
            if v[i] == x[0]:
                foundVar=True
                i_v=i
            if isinstance(v[i],int) and Idx==True:
                i_n=i
                Idx=False
            if foundVar and i==i_v+i_n:
                if v[i]==x[1]:
                    match=True
                    #print('match: ',v,x)
                    break
        if match:
            match=False
            foundVar=False
            foundIdx=False
            for k in kand:
                for i in range(len(k)):
                    if k[i] == x[0]:
                        i_v=i
                        foundVar=True
#                         print('foundVar: ',k,i,x)
                    if foundVar:
                        if isinstance(k[i],int) and not foundIdx:
                            i_n=i+i_v
                            foundIdx=True
#                             print('Index of value match at: ',i,i_v,i_n)
                        if foundIdx and k[i_n]==x[1]:
#                             print('found A TERM MATCH: ',k,x)
                            match=True
                            return match,'K'
            match=False
            foundVar=False
            foundIdx=False
            for s in sand:
                for i in range(len(s)):
                    if s[i] == x[0]:
                        i_v=i
                        foundVar=True
#                         print('foundVar: ',k,i,x)
                    if foundVar:
                        if isinstance(s[i],int) and not foundIdx:
                            i_n=i+i_v
                            foundIdx=True
#                             print('Index of value match at: ',i,i_v,i_n)
                        if foundIdx and s[i_n]==x[1]:
#                             print('found A TERM MATCH: ',k,x)
                            match=True
#                            clase='S'
                            return match,'S'
    return match,'U'
    
    
def checkLines(S_llaves,K_llaves,KS,KSvars,lineas):
#     print('Checking {} for alignment'.format(KS))
    L=[]
    for e in KS:
#         print('Checking... ',e)
        for K,S in zip(K_llaves,S_llaves):
            for l in lineas:
                k=K[l]
                s=S[l]
                found=False
#                 print('checking for match in: K={0}, S={1}'.format(k,s))
                found,C=checkMatch([k],s,e,KSvars)
                if found:
#                     print('Match found sending: [{}]'.format([e,l,C]))
                    L.append([e,l,C])
    return L


# ## Estructuras de datos del motor de inferencia
class Var():
    #==========================================================================
    # Variables aleatorias unidimensionales
    # atributos: - name: Nombre de la variable (string); p.e. "A"
    #            - values: Lista de valores discretos posibles de la variable
    # métodos: - set_values
    #==========================================================================
    def __init__(self,name:str='A',values=None): 
        self.name = name
        self.card = 0
        if values is not None:
            self.values = list(values)
            self.card = len(values)
            
    def set_values(self,values):
        self.values = list(values)
        self.card = len(values)
        
    def print_var(self):
        return (self.name, self.card, self.values)

class Distrib():
    #==========================================================================
    # Distribución Marginal - Tabla de probabilidad de una variable
    # atributos: - name: Nombre de la distribución (string); p.e. "P(A)"
    #            - indep: variables independientes
    #            - var: apuntador a objeto de tipo Var
    #            - tabla: Diccionario de valores de probabilidad
    # métodos: - asignación de atributos
    #          - recuperación de valores de probabilidad
    #==========================================================================
    def __init__(self,name,variable:Var=None,tabla=None):
        self.name = name
        self.indep=[]
        if variable is not None:
            self.var = variable
        if tabla is not None:
            self.tabla=carga_tabla(self.var,tabla)
    
    def set_name(self,name):
        self.name = name

    def set_variable(self,variable):
        self.var = variable
        
    def load_tabla(self,var,tabla):
        self.tabla=carga_tabla(var,tabla)

    def _print(self):
        print('Printing: ',self.name)
        for k in self.tabla.keys():
            print('{0}:{1} '.format(k,self.tabla[k]),end=' ')
        print('\n')
    
    def to_Frame(self):
        print('Creating DataFrame for: ',self.name)
        dico=self.get_P()
        nombre=self.name
        columnas=[nombre]
        indice=list(dico.keys())
        registros=list(dico.values())
        df=pd.DataFrame(registros,columns=columnas,index=indice)
        return df
        
    
    def get_P(self,key='all'):
        if key != 'all':
            return self.tabla[key]
        else:
            return self.tabla

    def get_all_P(self):
        L=[]
        for k in self.tabla.keys():
            L.append(self.get_P(k))
        return L

class DistribCond(Distrib):
    #=============================================================================
    # Distribución Condicional* - Tabla de valores de probabilidad condicional
    # atributos: - name: Nombre de la distribución (string); p.e. "P(A|B)"
    #            - indep: lista de variables independientes (tipo Var) (entrada)
    #            - var: apuntador a objeto de tipo Var (salida)
    #            - tabla: Diccionario de valores de probabilidad de la salida
    # métodos: - asignación de atributos
    #          - recuperación de valores de probabilidad
    # llamado a funciones:
    #          - genera_espacio(entrada): genera las combinaciones posibles de
    #            los valores de entrada.
    #          - carga_tabla_cond(**keys): genera la tabla condicional
    # *En principio la tabla puede contener varias variables de salida.
    #===============================================================================
    def __init__(self,name,var,indep,tabla=None):
        self.name = name
        self.indep=indep
        self.var=var
        entrada=[i.values for i in indep]
        self.entry=genera_espacio(entrada)
        if tabla is not None:
            self.tabla=carga_tabla_cond(self.var,self.entry,self.indep,tabla)
            
    def set_name(self,name):
        self.name = name
        
    def load_tabla(self,tabla):
        self.tabla=carga_tabla_cond(self.var,self.entry,self.indep,tabla) 
        
    def get_P(self,conditions='all',values='all'):
        L=[]
        if not isinstance(conditions,str) and not isinstance(conditions,list):
            print("Las condiciones deben ser una lista de tuplas")
            return L
        else:
            if conditions=='all' and values == 'all':
                return self.tabla
            else:
                if conditions=='all':
                    entries = itemgetter(*self.tabla.keys())(self.tabla)
                else:
                    entries = itemgetter(*conditions)(self.tabla)
                if values == 'all':
                    L.append(entries)
                else:
                    if len(values) == len(conditions):
                        for v,d in zip(values,entries):
                            data = itemgetter(*v)(d)
                            L.append(data)
                    elif len(values) <= len(conditions):
                        val = values[:]
                        for i in range(len(conditions)-len(values)-1):
                            val.extend(val)
                        val.extend(val)
                        for v,d in zip(val,entries):
                            data = itemgetter(*v)(d)
                            L.append(data)
                    else:
                        print("Combinación de condiciones y valores incompatible!")    
        return L

    def to_Frame(self,formateo=False):
        def format_numbers(data):
            base10 = np.log10(abs(data))
            base10 = abs(floor(base10))
            if base10 >= 4:
                return data
            else:
                return f'{data:.6f}'

        dico=self.get_P()
        indice=list(dico.keys())
        vals=list(dico.values())
        columnas=[]
        registros=[]
        if type(vals[0])==dict:
            for d in vals:
                if list(d.keys()) not in columnas:
                    columnas.append(list(d.keys()))
                registros.append(list(d.values()))
        else:
            columnas=list(dico[list(dico.keys())[0]].keys())
            registros=[]
            for i,d in enumerate(vals): 
                reg=[]
                for c in columnas:
                    reg.append(d[c])
                registros.append(reg)
        if type(self.var) == list:
            searched=[v.name for v in self.var]
        else:
            searched=[self.var.name]
        if type(self.indep) == list:
            known=[v.name for v in self.indep]
        else:
            known=[self.indep.name]
        thevars=searched+known
        df=pd.DataFrame(registros,columns=columnas,index=indice)
        if formateo:
            for col in df.columns:
                df[col]=df[col].map(lambda x:f'{format_numbers(x)}')
        return df

class JointDistrib(DistribCond):
    #================================================================================
    # Distribución Conjunta* - Tabla de probabilidad de una descomposición
    #                          condicional siguiendo la regla del producto.
    # atributos: - name: Nombre de la distribución (string); p.e. "P(AB)"
    #            - variables: lista de variables (tipo Var) (entrada)
    #            - descomp: lista de distribuciones marginales y condicionales;
    #                       La lista se ordena por orden ascendente de la 
    #                       longitud del nombre de cada distribución.
    #            - entries: 
    # métodos: - lectura de valores de probabilidad
    # *No se calculan las posibilidades de valores de entrada, solo sirve para
    #  estructurar el cálculo a partir de distribuciones marginales y condicionales.
    #=================================================================================
    def __init__(self,name,variables,descomp):
        self.name = name
        self.vars = variables
        self.label_to_var = {}
        self.ID=self
        for v in self.vars:
            self.label_to_var[v.name]=v
        descomp.sort(key=lambda x: len(x.name), reverse=True)
        self.descomp = descomp
        #entrada=[i.values for i in variables]
        #self.entries=genera_espacio(entrada)
        
    def get_P(self,n=1000):
        Q_=Question(self)
        distrib=Q_.query(self.vars)
        tabla=distrib.get_P()
        if self.ID is self:
            if len(tabla)>n:
                opc=input(f'El tamaño de la tabla es mayor a {n}... ¿prefiere crear un archivo csv?[S]/n') or 'S'
                if opc=='S':
                    df=self._toFrame()
                    df.to_csv('outputTable.csv')
                    print('se guardo el archivo outputTable.csv')
                    return None
        return tabla

    def _print(self):
        for distrib in self.descomp:
            print('{0} : {1}'.format(distrib.name,distrib.tabla))

    def to_Frame(self):
        self.ID=None
        dico=self.get_P()
        self.ID=self
        nombre=self.name
        columnas=[nombre]
        indice=list(dico.keys())
        registros=list(dico.values())
        df=pd.DataFrame(registros,columns=columnas,index=indice)
        return df

class Question():
    #================================================================================
    # Pregunta - Inferencia probabilista mediante una pregunta a la Conjunta.
    # atributos: - joint: Distribución conjunta (objeto); p.e. P_AB
    # métodos: - compute_marginal: calcula una distribución marginal sobre N variables
    #          - compute_conditional: calcula una distrb. cond. de NxM variables
    # NOTA: las variables se dividen en los siguientes sub-conjuntos:
    # - KNOWN: variables cuyos valores de probabilidad son conocidos.
    # - UNKNOWN: variables cuyos valores son deconocidos.
    # - SEARCHED: variables cuyos valores nos interesa conocer (query)
    #=================================================================================
    def __init__(self,joint):
        self.joint = joint
        
    def known_distrib(self,name):
        return None
        
    def compute_marginal(self,searched,unknown,vals=None,valu=None,r=0):
        #================================================================================
        # Método de inferencia probabilista de una distribución marginal.
        # entradas: - searched
        #           - unknown
        # salidas: - diccionario de P(searched)
        #=================================================================================
        # print('<<<<<<<<<<<<<<<<<<<<<<<<<>>>>DEBUG>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # print('-----------------------COMPUTING MARGINAL-------------------')
        # print('<<<<<<<<<<<<<<<<<<<<<<<<<>>>>DEBUG>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        if len(searched)>1:
            skeys,var_list = genera_vars_llaves(searched)
        else:
            skeys = genera_llaves(searched)
        ukeys = genera_llaves(unknown)
        # print('DEBUG Searched space:= ',skeys)
        # print('DEBUG UNKNOWN SPACE====>>> ',ukeys)
        Unk_vars = look_up_table(unknown,ukeys)
        Unk_vars.sort()
        # print('DEBUG Looking up for Unknown Unk_vars:= ',Unk_vars)
        dico={}
        for v in skeys:
            # print('========DEBUG ============')
            # print('Filling up v:= ',v)
            # print('========DEBUG ============')
            ###################################################
            # Working data structures to compute marginal dist.
            ###################################################
            K_llaves=[]
            S_llaves=[]
            lineas=[]
            a_Lps=[]
            #############################################################
            # COMPUTING P(v=searched) from JOINT distribution.
            # JOINT is assumed to be a product of Distributions .
            # Distributions are assumed to be of the form P(Y|X) or P(Y)
            # where X or Y may be a list of variables.
            ############################################################
            for n,distrib in enumerate(self.joint.descomp):
                ################################################################
                # Creating new array alignments K=X; S=Y.
                # Array alignmnents Li are assumed to correspond
                # to Known (K) searched keys in the first distribution.
                # P points to the current distribution.
                # We adopt the convention: K(known)=X; S(searched)=Y.
                # Knd stands for KNOWN_dist vars and Srd for SEARCHED_dist vars.
                # Combinatorial spaces are created from this variables and then
                # filtered out in function of the searched variable 'v'.
                ################################################################
                LK={}
                LS={}
                L_ps=defaultdict(dict)
                if n!= 0:
                    LK=defaultdict(list)
                    LS=defaultdict(list)
                P=distrib
                Knd=distrib.indep
                Srd=distrib.var
                if Knd == []:
                    Skeys=genera_llaves(Srd)
                    # print('DEBUG {0} No hay indep: {1}'.format(distrib.name,Skeys))
                    Srd_vars = look_up_table(Srd,Skeys)
                    S_U=list(set(Srd_vars) & set(Unk_vars))
                    thevars=[a.name for a in Srd]
                    Srd_space=Skeys
                    # print('DEBUG original Srd_space is: ',Srd_space)
                    if S_U != []:
                        Srd_space=filter(Srd_space,S_U,thevars)
                    Srd_space=filter_rec(Srd_space,Srd_vars,v)
                    # print('------------DEBUG --------------------------')
                    # print('NO-CONDICIONAL---> Have to retrieve Srd_space: ',Srd_space)
                    # print('------------DEBUG --------------------------')
                    #################################################
                    # Align probability computations on S.
                    #################################################
                    for i,k in enumerate(lineas):
                        LK[k]=[]
                    n_Svars=look_up_table(Srd,Srd_space)
                    L_s=checkLines(S_llaves,K_llaves,Srd_space,n_Svars,lineas)
                    if L_s == []:
                        for i,k in enumerate(lineas):
                            LS[k]=Srd_space
                    else:
                        for e in L_s:  #e,l,K_S
                            LS[e[1]].append(e[0])
                    # print("/////////////////////DEBUG /////////////////////////////////")
                    # print('   NO-CONDICIONAL---> HAVE TO COMPUTE PROBS ON')
                    # print('/////////////////////DEBUG /////////////////////////////////')
                    # print('LK={}'.format(LK))
                    # print('LS={}'.format(LS))
                    # print('//////////////////////DEBUG ////////////////////////////////////////')
                    # print('   NO-CONDICIONAL---> Getting prob values from {}'.format(P.name))
                    # print('//////////////////////DEBUG ////////////////////////////////////////')
                    for s in LS.keys():
#                         print(s)
                        y=LS[s]
#                         print(y)
                        L_ps[s]=defaultdict(list)
                        # print('DEBUG CREATED FIRST L_ps >>> {0} using {1}'.format(L_ps,s))
                        for j in y:
                            # print('DEBUG Retrieving prob value --->> P({0})= '.format(j),end=' ')
                            # print('DEBUG {}'.format(P.tabla[j]))
                            p=P.tabla[j]
                            # print('DEBUG Current p value ===>>>> ',p)
                            L_ps[s][j].append(p)
                    # print('>>>>>>>>>>>>>>>> DEBUG Overall probabilities: <<<<<<<<<<<<<<<<<<<<<<',L_ps)
                    a_Lps.append(L_ps)
                    K_llaves.append(LK)
                    S_llaves.append(LS)
                else:
                    #################################################
                    # Filtering the KNOWN SPACE: X to compute P(Y|X)
                    #################################################

                    Kkeys=genera_llaves(Knd)
                    Skeys=genera_llaves([Srd])
#                     print('DEBUG {0}: {1} | {2}'.format(distrib.name,Skeys,Kkeys))
                    Knd_vars = look_up_table(Knd,Kkeys)
                    Srd_vars = look_up_table([Srd],Skeys)
                    K_U=list(set(Knd_vars) & set(Unk_vars))
                    S_U=list(set(Srd_vars) & set(Unk_vars))
                    thevars=list(set([a.name for a in [Srd]]+[a.name for a in Knd]))
#                    S_v=list(set(Srd_vars) & set([v]))
                    Knd_space=Kkeys
#                     print('DEBUG original Knd_space is: ',Knd_space)
                    if K_U != []:
                        # print('-_-_-_-_-PROBLEM IS HERE-_-_-_-')
                        Knd_space=filter(Knd_space,K_U,thevars)
                    Knd_space=filter_rec(Knd_space,Knd_vars,v) 
                    Knd_space.sort()
#                     print('-----------------DEBUG ------------------------------------')
#                     print('CONDICIONAL--->Have to look in Knd space: ',Knd_space)
#                     print('------------------DEBUG ------------------------------------')
                    #######################################################
                    # Initialize the array alignment labels: 'LINES'
                    # and create new array alignments K<->X; S<->Y.
                    # Array alignmnents Li are assumed to correspond
                    # to Known (K) searched keys in the first distribution.
                    #######################################################
                    if n==0:
                        linea='L'
                        for i in range(len(Knd_space)):
                            lineas.append(linea+str(i))
#                         print('DEBUG Full NEW lines created: ',lineas)
                        LK=defaultdict(list)
                        LS=defaultdict(list)
                    #################################################
                    # Filtering the RETRIEVED SPACE: Y.
                    #################################################
                    Srd_space=Skeys
                    if S_U != []:
                        Srd_space=filter(Srd_space,S_U,thevars)
#                         print('filtering Srd_space from S_U yields: ',Srd_space)
#                     print("Have to FILTER Srd space: {0} from Srd_vars: {1} to get v: {2}".format(Srd_space,Srd_vars,v))
                    Srd_space=filter_rec(Srd_space,Srd_vars,v)
                    Srd_space.sort()
#                     print('------------------DEBUG -------------------------------------')
#                     print('CONDICIONAL--->Have to retrieve Srd_space: ',Srd_space)
#                     print('------------------DEBUG -------------------------------------')
                    
                    #################################################
                    # Align probability computations on K and S.
                    #################################################

#                     print('DEBUG Looking for INTERSECTIONS WITH PAST')
                    n_Kvars=look_up_table(Knd,Knd_space)
                    n_Svars=look_up_table([Srd],Srd_space)
                    L_k=checkLines(S_llaves,K_llaves,Knd_space,n_Kvars,lineas)
#                     print('DEBUG >>>>>>>>>>>>>>>GETTING L_k= ',L_k)
                    L_s=checkLines(S_llaves,K_llaves,Srd_space,n_Svars,lineas)
#                     print('DEBUG >>>>>>>>>>>>>>>GETTING L_s= ',L_s)
                    if L_k == []:
                        for i,k in enumerate(lineas):
                            LK[k]=Knd_space[i]
                    else:
                        for e in L_k:  #e,l,K_S
                            LK[e[1]].append(e[0])
#                             if e[2]=='K':
#                                 print('FROM L_k: Found match in Knd_space')
#                             else:
#                                 print('FROM L_k: Found match in Srd_space')
#                             print('e[0]={0} appended to LK[{1}]={2}'.format(e[0],e[1],LK[e[1]]))
                    if L_s == []:
                        for i,k in enumerate(lineas):
                            LS[k]=Srd_space
                    else:
                        for e in L_s:  #e,l,K_S
                            LS[e[1]].append(e[0])
#                             if e[2]=='K':
#                                 print('FROM L_s: Found match in Knd_space')
#                             else:
#                                 print('FROM L_s: Found match in Srd_space')
#                             print('e[0]={0} appended to LS[{1}={2}]'.format(e[0],e[1],LS[e[1]]))
                                
                    ######################################################
                    # Retrieve probabilities based on K and S alignments.
                    ######################################################
#                     print("//////////////////DEBUG ////////////////////////////////////")
#                     print('     CONDICIONAL---> HAVE TO COMPUTE PROBS ON')
#                     print('//////////////////DEBUG ////////////////////////////////////')
#                     print('LK={}'.format(LK))
#                     print('LS={}'.format(LS))
#                     print('///////////////////////DEBUG ///////////////////////////////////////')
#                     print('     CONDICIONAL--->Getting prob values from {}'.format(P.name))
#                     print('//////////////////////DEBUG ////////////////////////////////////////')
                    LK_llaves=list(LK.keys())
                    LK_llaves.sort()
                    LS_llaves=list(LS.keys())
                    LS_llaves.sort()
                    for k,s in zip(LK_llaves,LS_llaves):
#                         print(k,s)
                        x=LK[k]
#                         print(x)
                        L_ps[k]=defaultdict(dict)
#                         print('DEBUG CREATED FIRST L_ps >>> {0} using {1}'.format(L_ps,k))
                        y=LS[s]
#                         print(y)
                        if isinstance(x,list):
#                             print('x is a list')
                            for i in x:
#                                 print(i)
                                L_ps[k][i]=defaultdict(list)
#                                 print('CREATED SECOND L_ps >>> {0} using {1}'.format(L_ps,i))
                                for j in y:
#                                     print('Retrieving prob value --->> ',P.tabla[i][j])
                                    p=P.tabla[i][j]
#                                     print('Current p value ===>>>> ',p)
                                    L_ps[k][i][j].append(p)
                        else:
                            L_ps[k][x]=defaultdict(list)
#                             print('CREATED SECOND L_ps >>> {0} using {1}'.format(L_ps,x))
                            for j in y:
#                                 print('Retrieving prob value --->> P({0}|{1})= '.format(x,j),end=' ')
#                                 print('{}'.format(P.tabla[x][j]))
                                p=P.tabla[x][j]
#                                 print('Current p value ===>>>> ',p)
                                L_ps[k][x][j].append(p)
#                     print('>>>>>>>>>>>>>>>> DEBUG Overall probabilities: <<<<<<<<<<<<<<<<<<<<<<')
#                     print(L_ps)
                    a_Lps.append(L_ps)
#                     print('>>>>>>>>>>>>>>>> DEBUG Overall probabilities: <<<<<<<<<<<<<<<<<<<<<<')
                    K_llaves.append(LK)
                    S_llaves.append(LS)
            ####################################################
            # Compute probabilities based on K and S alignments
            ####################################################
            
            # print('\n')
            # print('<=><=><=><=><=><=><=>DEBUG <=><=><=><=><=><=><=><=><=>')
            # print('ALMOST DONE FOR ',v)
            # print('<=><=><=><=><=><=><=>DEBUG <=><=><=><=><=><=><=><=><=>')
            # print('\n')
            # print(a_Lps)
            llaves=a_Lps[0].keys()
            s=[]
            for linea in llaves:
                dd=[]
                for d in a_Lps:
                    dd.append(d[linea])
                dd.reverse()
                d=dd.pop()
                dd.reverse()
                # print('checking ',d)
                summation=0.0
                keys=list(d.keys())
                for k in keys:
                    # print('DEBUG k= ',k)
                    # print('DEBUG cheking {0} S space'.format(d))
                    for dk in d[k].keys():
                        # print('DEBUG checking key: ',dk)
                        pr=np.array(d[k][dk])
                        # print('DEBUG Current pr = ',pr)
                        for j in range(len(dd)):
                            # print('DEBUG against dd[{0}]={1}'.format(j,dd[j]))
                            todas_las_llaves=[]
                            for kllave in dd[j].keys():
                                todas_las_llaves.append(kllave)
                            if dk in todas_las_llaves:
                                # print('DEBUG dk in kllave')
                                kllave=dk
                                # print('DEBUG {0} next key is kllave = {1}'.format(dd[j],kllave))
                                if isinstance(dd[j][kllave],dict):
                                    el=0
                                    for kkllave in dd[j][kllave].keys():
                                        el+=np.array(dd[j][kllave][kkllave])
                                    # print('multiplying pr={0} x SUM_dd[{1}][{2}][{3}] -->> {0}x{4}'\
                                    #       .format(pr,j,kllave,kkllave,el))
                                    pr*=np.array(el)
                                    # print('pr= ',pr)
                                else:
                                    # print('multiplying pr={0} x SUM_dd[{1}][{2}] -->> {0}x{3}'\
                                    #       .format(pr,j,kllave,dd[j][kllave]))
                                    pr*=np.array(dd[j][kllave])
                                    # print('pr= ',pr)
                            else:
                                for kllave in dd[j].keys():
                                    if isinstance(dd[j][kllave],dict):
                                        # print(':::::dict:::::detected:::::')
                                        el=0
                                        for kkllave in dd[j][kllave].keys():
                                            el+=np.array(dd[j][kllave][kkllave])
                                        # print('multiplying pr={0} x dd[{1}][{2}][{3}] -->> {0}x{4}'\
                                        #         .format(pr,j,kllave,kkllave,dd[j][kllave][kkllave]))
                                            # pr*=np.array(dd[j][kllave][kkllave])
                                            # print('pr= ',pr)
                                        pr*=np.array(el)
                                        # print('pr= ',pr)
                                    else:
                                        # print('multiplying pr={0} x dd[{1}]:[{2}] -->> {0}x{3}'\
                                        #       .format(pr,j,kllave,dd[j][kllave]))
                                        pr*=np.array(dd[j][kllave])
                                        # print('pr= ',pr)
                        summation+=pr
                        # print('DEBUG CURRENT SUMMATION GIVES: ==>> ',summation)
                s.append(summation)
            # print('<=><=><=><=><=><=><=>DEBUG <=><=><=><=><=><=><=><=><=>')
            # print('FINAL COMPUTATIONS FOR ',v)
            # print('<=><=><=><=><=><=>DEBUG <=><=><=><=><=><=><=><=><=><=>')
            # print('MULTIPLYING AND SUMMING OVER:')
            # print(s)
            fp=np.sum(np.array(s))
            # print('DEBUG Final p value ========>>>>> ',fp)
            if r!=0:
                dico[v]=np.round(fp,r)
            else:
                dico[v]=fp
        return dico

    def compute_conditional(self,searched,known,unknown):
        ###################################################################
        # The aim is to compute the marginals involved at the numerator
        # and at denominator.
        # Then the function performing the division aligning the variables
        # and corresponding values is called
        ####################################################################
        nS=[s.name for s in searched]
        nK=[s.name for s in known]
        nU=[s.name for s in unknown]
        name='P('+','.join(nS) +'|'+','.join(nK) +')'
        # print('computing: {}, WITH UNKNOWN VARIABLES: {}'.format(name,nU))
        searchedJoint=searched+known
        unknownJoint=searched+unknown
        dico_Y=self.compute_marginal(searchedJoint,unknown)
        dico_X=self.compute_marginal(known,unknownJoint)
        # print(':::::::dicoY::::::::', dico_Y)
        # print(':::::::dicoX::::::::', dico_X)
        dico=compute_conditional_probs(dico_Y,dico_X,searched,known)

        return dico

    def query(self,searched, known=[]):
        # try:
        if len(searched)>1:
            if known !=[]:   #CONDITIONAL DISTRIBUTION OF SEVERAL SEARCHED VARIABLES
                nS=[s.name for s in searched]
                nK=[s.name for s in known]
                name='P('+','.join(nS) +'|'+','.join(nK) +')'
                print('computing conditional of joint: {}'.format(name))
                All=[a.name for a in self.joint.vars]
                Uk=list(set(All)-set(nS).union(set(nK)))
                unknown=[]
                for nombre in Uk:
                    unknown.append(self.joint.label_to_var[nombre])

                dico=self.compute_conditional(searched,known,unknown)                                            
                distribution = DistribCond(name,searched,known)            
                distribution.tabla=dico
                return distribution
            else:  #MARGINAL DISTRIBUTION OF SEVERAL SEARCHED VARIABLES
                names=[s.name for s in searched]
                name='P('+','.join(names)+')'
                print('Computing marginal joint: {}'.format(name))
                All=[a.name for a in self.joint.vars]
                Uk=list(set(All)-set(names))
                #print('Unknow vars: ',Uk)
                unknown=[]
                for n in Uk:
                    unknown.append(self.joint.label_to_var[n])
                distribution = Distrib(name,searched)
                dico=self.compute_marginal(searched,unknown)
                distribution.load_tabla(searched,dico)
                return distribution
        else:  #MARGINAL DISTRIBUTION OF A SINGLE VARIABLE
            searched=searched[0]
            if known is None or known==[]:
                name='P('+searched.name+')'
                print('computing marginal {}'.format(name))
                All=[a.name for a in self.joint.vars]
                Uk=list(set(All)-set([searched.name]))
                #print('Unknow vars: ',Uk)
                unknown=[]
                for n in Uk:
                    unknown.append(self.joint.label_to_var[n])

                dico=self.compute_marginal([searched],unknown)
                distribution = Distrib(name,[searched])            
                distribution.load_tabla([searched],dico)
                return distribution
            else: #CONDITIONAL DISTRIBUTION OF A SINGLE SEARCHED VARIABLE
                nK=[s.name for s in known]
                name='P('+ searched.name +'|'+','.join(nK) +')'
                print('computing conditional: {}'.format(name))
                All=[a.name for a in self.joint.vars]
                Uk=list(set(All)-set(searched.name).union(set(nK)))
                #print('Unknow vars: ',Uk)
                unknown=[]
                for n in Uk:
                    unknown.append(self.joint.label_to_var[n])

                dico=self.compute_conditional([searched],known,unknown)                    

                distribution = DistribCond(name,searched,known)            
                distribution.tabla=dico
                return distribution
#     except TypeError:  #NO LIST SENT: SINGLE VARIABLE SEARCHED
#         if known is None or known==[]:  #MARGINAL DISTRIBUTION
#             name='P('+searched.name+')'
#             print('computing marginal {}'.format(name))
#             All=[a.name for a in self.joint.vars]
#             Uk=list(set(All)-set([searched.name]))
#             #print('Unknow vars: ',Uk)
#             unknown=[]
#             for n in Uk:
#                 unknown.append(self.joint.label_to_var[n])

#             dico=self.compute_marginal([searched],unknown)
#             distribution = Distrib(name,[searched])            
#             distribution.load_tabla([searched],dico)
#             return distribution
#         else:   #CONDITIONAL DISTRIBUTION
#             nK=[s.name for s in known]
#             name='P('+','.join(searched.name) +'|'+','.join(nK) +')'
#             print('computing conditional: {}'.format(name))
#             All=[a.name for a in self.joint.vars]
#             Uk=list(set(All)-set(searched.name).union(set(nK)))
#             unknown=[]
#             for n in Uk:
#                 print('=========IN FOR=========')
#                 unknown.append(self.joint.label_to_var[n])
#             dico=self.compute_conditional([searched],known,unknown)                    
#             distribution=DistribCond(name,searched,known)
#             distribution.tabla=dico
#             return distribution


def ejemplo_prueba():
    dE={0:0.6,1:0.4}
    dC={0:0.7,1:0.3}
    dN_EC={(0,0):{0:0.8,1:.18,2:.02},(0,1):{0:.3,1:.6,2:.1},(1,0):{0:.3,1:.4,2:.3},(1,1):{0:.1,1:.2,2:.7}}
    dO_N={0:{0:.9,1:.1},1:{0:.4,1:.6},2:{0:.01,1:.99}} 
    
    E=Var('E',[0,1])
    C=Var('C',[0,1])
    O=Var('O',[0,1])
    N=Var('N',[0,1,2])
    
    P_E=Distrib('P(E)',[E],dE)
    
    P_C=Distrib('P(C)',[C],dC)
    P_N_EC=DistribCond('P(N|EC)',N,[E,C],dN_EC)
    P_O_N=DistribCond('P(O|N)',O,[N],dO_N)
    
    #joint distribution
    P_ECNO=JointDistrib('P(ECNO)',[E,C,N,O],[P_E,P_C,P_N_EC,P_O_N])
    P_ECNO._print()

##Descomentar la línea siguiente para probar el codigo
#ejemplo_prueba()