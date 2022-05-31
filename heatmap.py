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
import cv2
from difference import find_diff






###\\\\
""" 
Choses modifiables : 
-si jamais changement des noms des dossiers du projet ex: FichierComparaisonImg :
Remaplcer le nom dans les variables qui contienent les PATHS.

-Si on veut changer ou ajouter une nouvelle carte changer le nom dans MapConvert()
avec "newCarte.png"  

-Dans le dossier "heat_maps" on retrouve toutes les Heatmaps de chaque fichier

-Dans le dossier "heatmaps_background" On retrouve la carte + Heatmap

-Dans le dossier "map" On place la carte 

-Dans le dossier "map_converted" On retrouve la carte convertie pour fusioner avec HeatMap

EN TANT QUE Autre UTILISATEUR !! Changer la variable "Path_Final" avec votre Path



"""
####\\\\


## PATH_FINAL A CHANGER EN FONCTION DE USER

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
    """ 
    Prend la surface de chaque Batiment
    
    """
    
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


test_list=(Get_cadre(path_file_json))               #on stock les plus grandes cadres de chaque fichier
final_cadre=Get_Biggest_Cadre(test_list)   #on prend le plus grand cadre pour toutes les fichiers
    
global xmin
xmin = final_cadre[0]
global xmax
xmax=final_cadre[1]
global ymin
ymin=final_cadre[2]
global ymax
ymax=final_cadre[3]











def  mapConvert(xmin,xmax,ymin,ymax ,path1):
    """
    Convertie une l'image d'une carte sous le meme format que les HeatMaps 
    pour les superposer
    
     
    """
    #X,Y,Z pour ne pas affecter les couleurs de l'image
    X=[[0,0,0],[0,0,0]] 
    Y=[[0,0,0],[0,0,0]]
    Z=[[0,0,0],[0,0,0]]
    img = plt.imread(path_final + r"\Stage-main\python_class\FichierComparaisonImg\map\finalazi.png")
    fig, ax = plt.subplots(figsize = (10,10))
    plt.imshow(img, cmap=plt.cm.jet,
        extent=[xmin, xmax, ymin, ymax])
    plt.pcolor(X, Y, Z, cmap=plt.cm.jet, vmin=0, vmax=Get_max_val(path1),shading='auto')
    cbar=plt.colorbar()
    cbar.set_label('DENSITY', rotation=270)
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.savefig(os.path.join(path_map, ("map.png"))) 






def Get_max_val(path1 ):
    """
    Cherche la plus grande valeur de densité pour imposer le Vmax de l'echelle
    returns : int max
    """
    max=0
    directory = os.listdir(path1)
    os.chdir(path1)

    for file in directory:
        path_abs=(file)
        
        surface=getSurface(path_abs)
        X=CenterPoly(path_abs)

        area_bat=np.array(surface)
        X = np.array(X)

        # get the mesh
        m1, m2 = X[:, 0], X[:, 1]
        #print(xmin,xmax,ymin,ymax)
        X, Y = np.mgrid[xmin:xmax:150j, ymin:ymax:150j]
        positions = np.vstack([X.ravel(), Y.ravel()])
        values = np.vstack([m1, m2])

        
        kernel =stats.gaussian_kde(values,bw_method=None, weights=area_bat)#bw_method=None, weights=area_bat
        Z = np.reshape(kernel(positions).T, X.shape)
        if np.amax(Z)>= max:
            max=np.amax(Z)
        
    return max
        
    

def HeatMap_Gen(path1,path2 ):

    directory = os.listdir(path1)
    dir_save=(path2)
    os.chdir(path1)
    for file in directory:
        path_abs=(file)



        surface=getSurface(path_abs)            #prend la surface de chaque polygone
        X=CenterPoly(path_abs)                  #prend le centre de chaque polygone


        area_bat=np.array(surface)



        X = np.array(X)

        # get the mesh
        m1, m2 = X[:, 0], X[:, 1]

        
        #xmin = (m1.min()) 
        #xmax = (m1.max()) 
        #ymin = (m2.min()) 
        #ymax = (m2.max()) 

        # get the density estimation 
        
        X, Y = np.mgrid[xmin:xmax:150j, ymin:ymax:150j]
        positions = np.vstack([X.ravel(), Y.ravel()])
        values = np.vstack([m1, m2])

        
        kernel =stats.gaussian_kde(values,bw_method=None, weights=area_bat)#bw_method=None, weights=area_bat
        Z = np.reshape(kernel(positions).T, X.shape)
        
        

        # plot the result
        fig, ax = plt.subplots(figsize = (10,10))

        rom=plt.imshow(np.rot90(Z), cmap=plt.cm.jet,
                extent=[xmin, xmax, ymin, ymax])
        
        plt.pcolor(X, Y, Z, cmap=plt.cm.jet, vmin=0, vmax=Get_max_val(path1),shading='auto')
        cbar=plt.colorbar()



        cbar.set_label('DENSITY', rotation=270)
        
        ax.plot(m1, m2, 'k.', markersize=5)

        
        ax.set_xlim([xmin, xmax])
        ax.set_ylim([ymin, ymax])
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.savefig(os.path.join(dir_save, (file + ".png"))) 










    



def heatmap_background(path1 , path2):
        """ 
        Superpose la carte et la Heatmap pour la mettre dans le background
        """
        
        directory = os.listdir(path1)
        map=path2
        img1 = cv2.imread(map)
        os.chdir(path1)
        
        for file in directory:
                img2 = cv2.imread(file)
                res = cv2.addWeighted(img1, 1, img2, 0.6, 0) #Modifier les parametres pour +/- de clarité
                cv2.imwrite(path_final +  '\\Stage-main\\python_class\\FichierComparaisonImg\\heatmaps_background\\' + file  , res) 
                cv2.waitKey(0)
                cv2.destroyAllWindows()






def main_heatMap():
    HeatMap_Gen(path_file_json,path_photo)
    path_map=(path_final + r"\Stage-main\python_class\FichierComparaisonImg\map_converted\map.png")
    mapConvert(xmin,xmax,ymin,ymax,path_file_json )
    heatmap_background(path_photo , path_map)
    find_diff(path_file_json, path_saveDiff)


main_heatMap()