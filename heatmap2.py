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

def PointsHeat_simulation(path):
    """
    Calcule le milieu de chaque polygone d'un fichier Geojson
    
    
    """
    
    with open(path) as f:
        fileImport = geojson.load(f)
    res=[]
    i=0
    k=0
    for i in range(len(fileImport['features'])):
        
        g2=shape(fileImport['features'][i]['geometry'])
        area_var=round(area(fileImport['features'][i]['geometry']))

       
        cord_center=g2.centroid.wkt
        geojson_string = geojson.dumps(mapping(loads(cord_center)))
        geojson_dict = ast.literal_eval(geojson_string)
        center_point=geojson_dict["coordinates"]
        k=0
        for k in range(area_var):
            res.append(center_point)
            k+=1
        i+=1
            
    return res

def PointsHeat_reels(path):
    """
    Calcule le milieu de chaque polygone d'un fichier Geojson
    
    
    """
    
    with open(path) as f:
        fileImport = geojson.load(f)
    res=[]
    i=0
    k=0
    for i in range(len(fileImport['features'])):
        g2=shape(fileImport['features'][i]['geometry'])
        area_var=round(g2.area)
        
        cord_center=g2.centroid.wkt
        geojson_string = geojson.dumps(mapping(loads(cord_center)))
        geojson_dict = ast.literal_eval(geojson_string)
        center_point=geojson_dict["coordinates"]
        k=0
        if area_var == 0 :
            area_var == 1
        for k in range(area_var):
            res.append(center_point)
            k+=1
        i+=1
            
    return res


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





def HeatMap_Gen(path1,path2 ):

    directory = os.listdir(path1)
    dir_save=(path2)
    os.chdir(path1)
    for file in directory:
        path_abs=(file)



        surface=getSurface(path_abs)
        X=CenterPoly(path_abs)




        #X.append([178.4033025,-18.098674])
        #X.append([178.41152,-18.098654])
        #X.append([178.40349,-18.107383]) 
        #X.append([178.41154,-18.107301])

        X.append([178.4033025,-18.098674])
        X.append([178.41152,-18.098654])
        X.append([178.40349,-18.107383]) 
        X.append([178.41154,-18.107301])
        
        
        surface.append(1)
        surface.append(1)
        surface.append(1)
        surface.append(1)


        area_bat=np.array(surface)



        X = np.array(X)




        # get the mesh
        m1, m2 = X[:, 0], X[:, 1]


        xmin = (m1.min()) 
        xmax = (m1.max()) 
        ymin = (m2.min()) 
        ymax = (m2.max()) 

        

        mapConvert(xmin,xmax,ymin,ymax)
        print(xmin,xmax,ymin,ymax)
        # get the density estimation 
        X, Y = np.mgrid[xmin:xmax:150j, ymin:ymax:150j]
        positions = np.vstack([X.ravel(), Y.ravel()])
        values = np.vstack([m1, m2])


        kernel =stats.gaussian_kde(values,bw_method=None, weights=area_bat)#bw_method=None, weights=area_bat
        Z = np.reshape(kernel(positions).T, X.shape)
        

        # plot the result
        fig, ax = plt.subplots(figsize = (10,10))

        plt.imshow(np.rot90(Z), cmap=plt.cm.jet,
                extent=[xmin, xmax, ymin, ymax])



        cbar=plt.colorbar()
        cbar.ax.set_yticks(0)
        cbar.ax.set_yticklabels([0])
        cbar.set_label('DENSITY', rotation=270)
        
        ax.plot(m1, m2, 'k.', markersize=5)





   
        
        ax.set_xlim([xmin, xmax])
        ax.set_ylim([ymin, ymax])
        plt.xlabel('Latitude')
        plt.ylabel('Longitude')
        plt.savefig(os.path.join(dir_save, (file + ".png"))) 







def  mapConvert(xmin,xmax,ymin,ymax):
    img = plt.imread(path_final + r"\Stage-main\python_class\FichierComparaisonImg\map\finalmap2.png")
    fig, ax = plt.subplots(figsize = (10,10))
    plt.imshow(img, cmap=plt.cm.jet,
        extent=[xmin, xmax, ymin, ymax])
    cbar=plt.colorbar()
    cbar.ax.set_yticks(0)
    cbar.ax.set_yticklabels([0])
    cbar.set_label('DENSITY', rotation=270)

    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.savefig(os.path.join(path_map, ("map.png"))) 





    
## PATH_FINAL A CHANGER EN FONCTION DE USER

path_final=(r"C:\Users\stefa\OneDrive\Desktop\SimulationOutil")

#Variable vers les fichiers Geojson
path_file_json=(path_final + r"\Stage-main\python_class\FichierComparaison")  

#variable du Path vers le fichier dont on retrouver les Heatmaps
path_photo=(path_final +r"\Stage-main\python_class\FichierComparaisonImg\heats")


#variable du Path vers le fichier dont on retrouve la map
path_map=(path_final + r"\Stage-main\python_class\FichierComparaisonImg\map_converted")


#variable du Path vers le fichier avec map+heatmap superposées
path_heatmaps=(path_final + r"\Stage-main\python_class\FichierComparaisonImg\heatmaps")






def heatmap_background(path1 , path2):
        directory = os.listdir(path1)
        map=path2
        img1 = cv2.imread(map)
        os.chdir(path1)
        
        for file in directory:
                img2 = cv2.imread(file)
                res = cv2.addWeighted(img1, 1, img2, 0.3, 0)
                cv2.imwrite(path_final +  '\\Stage-main\\python_class\\FichierComparaisonImg\\heatmaps\\' + file  , res) 
                cv2.waitKey(0)
                cv2.destroyAllWindows()






def main_heatMap():
    HeatMap_Gen(path_file_json,path_photo)
    path_map=(path_final + r"\Stage-main\python_class\FichierComparaisonImg\map_converted\map.png")
    heatmap_background(path_photo , path_map)
    

main_heatMap()
