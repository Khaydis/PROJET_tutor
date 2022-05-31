import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import geojson 
from shapely.wkt import loads
from shapely.geometry import mapping
import geojson
import ast
from shapely.geometry import shape
from area import area
import os
from skimage.metrics import structural_similarity



path_final=(r"C:\Users\stefa\OneDrive\Desktop\SimulationOutil")

#Variable vers les fichiers Geojson
path_file_json=(path_final + r"\Stage-main\python_class\FichierComparaison")  

#variable du Path vers le fichier dont on retrouver les Heatmaps
path_photo=(path_final +r"\Stage-main\python_class\FichierComparaisonImg\heat_maps")


#variable du Path vers le fichier dont on retrouve la map
path_map=(path_final + r"\Stage-main\python_class\FichierComparaisonImg\map_converted")



#variable du Path vers le fichier avec map+heatmap superposées
path_heatmaps=(path_final + r"\Stage-main\python_class\FichierComparaisonImg\heatmaps_background")

#path vers fichier avec les differences
path_saveDiff=(path_final + r"\Stage-main\python_class\FichierComparaisonImg\difference")

#path vers le fichier avec les similitarités

path_saveSimil=(path_final + r"\Stage-main\python_class\FichierComparaisonImg\similar")




def CenterPoly(path):
    """
    Calcule le milieu de chaque polygone d'un fichier Geojson
    
    
    """
    
    with open(path) as f:
        fileImport = geojson.load(f)
    res=[]
    i=0
    for i in range(len(fileImport['features'])):
        g2=shape(fileImport['features'][i]['geometry'])
        cord_center=g2.centroid.wkt
        geojson_string = geojson.dumps(mapping(loads(cord_center)))
        geojson_dict = ast.literal_eval(geojson_string)
        center_point=geojson_dict["coordinates"]
        res.append(center_point)
        i+=1
    return res





def getSurface(path):
    with open(path) as f:
        fileImport = geojson.load(f)
    res=[]
    for i in range(len(fileImport['features'])):

            obj=(fileImport['features'][i]['geometry'])
            res.append(round(area(obj)))
            i+=1

    
    return res 








def Get_cadre(path1):
    final_cadre=[]
    directory = os.listdir(path1)
    os.chdir(path1)
    for file in directory:
        path_abs=(file)
        X=CenterPoly(path_abs)
        X = np.array(X)

        # get the mesh
        m1, m2 = X[:, 0], X[:, 1]
        xmin = (m1.min()) 
        xmax = (m1.max()) 
        ymin = (m2.min()) 
        ymax = (m2.max()) 
        heat_cdr=[xmin,xmax,ymin,ymax]

        final_cadre.append(heat_cdr)
        
        

    return final_cadre



def Get_Biggest_Cadre(liste):
    xmin=liste[0][0]
    xmax=liste[0][1]
    ymin=liste[0][2]
    ymax=liste[0][3]
    
    for elem in liste:
        if (elem[0]<xmin ):
            xmin=elem[0]

        if (xmax<elem[1] ):
            xmax=elem[1]

        if (elem[2]<ymin ):
            ymin=elem[2]
        
        if (ymax<elem[3] ):
            ymax=elem[3]

    return ([xmin,xmax,ymin,ymax])



        



def find_date(str):
    emp_str = ""
    for m in str:
        if m.isdigit():
            emp_str = emp_str + m
    return emp_str 


def find_similar_files(path1):
    dicto={}
    directory = os.listdir(path1)
    os.chdir(path1)
    for elem in directory:
        x=find_date(elem)            
        if x in dicto:
            dicto[x].append(elem)
        
        else:
            dicto[x]=[elem]
    
    return dicto


def find_simil(dataset1,dataset2):

    (score, diff) = structural_similarity(dataset1, dataset2, full=True)
    res=("HeatMaps Similarity: {:.4f}%".format(score * 100))
            
    return res

            
def find_diff(path1,path2):
    dicto=find_similar_files(path1)
    os.chdir(path1)

    test_list=(Get_cadre(path1))
    final_cadre=Get_Biggest_Cadre(test_list)
    
    xmin=final_cadre[0]
    xmax=final_cadre[1]
    ymin=final_cadre[2]
    ymax=final_cadre[3]
    for key in dicto:
        value=dicto[key]
        if len(value)>1:
            fichier1=Get_Z(path1,value[0])
            fichier2=Get_Z(path1,value[1])
            similarity=(find_simil(fichier1,fichier2))
            if "reels" in value[0]:
                
                fichierRES=np.subtract(fichier2,fichier1)
            else:
                
                fichierRES=np.subtract(fichier1,fichier2)
            
            ax = plt.subplots(figsize = (10,10))
            plt.imshow(np.rot90(fichierRES), cmap=plt.cm.RdBu,
                       extent=[xmin, xmax, ymin, ymax])
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            cb=plt.colorbar()
            plt.title( similarity)
            plt.savefig(os.path.join(path2, (key + ".png"))) 
            cb.remove()




def Get_Z(path1,file):
    os.chdir(path1)        
    path_abs=(file)
    surface=getSurface(path_abs)
    X=CenterPoly(path_abs)

    area_bat=np.array(surface)
    X = np.array(X)

            # get the mesh
    m1, m2 = X[:, 0], X[:, 1]        
    test_list=(Get_cadre(path1))
    final_cadre=Get_Biggest_Cadre(test_list)
        
    xmin=final_cadre[0]
    xmax=final_cadre[1]
    ymin=final_cadre[2]
    ymax=final_cadre[3]
            
    X, Y = np.mgrid[xmin:xmax:150j, ymin:ymax:150j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([m1, m2])

            
    kernel =stats.gaussian_kde(values,bw_method=None,weights=area_bat)#bw_method=None, weights=area_bat
    Z = np.reshape(kernel(positions).T, X.shape)

    return Z




