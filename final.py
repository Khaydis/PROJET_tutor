
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
import scipy.stats as stats
import geojson 
from shapely.wkt import loads
from shapely.geometry import mapping
import geojson
import ast
from shapely.geometry import shape
from area import area
from sympy import Polygon
from scipy.stats import gaussian_kde
import os
from pathlib import Path

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





directory = os.listdir('C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\batiments_data')


dir_save='C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\resultats'










os.chdir('C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\batiments_data')
for file in directory:
    path_abs=(file)



    surface=getSurface(path_abs)
    X=CenterPoly(path_abs)
    X.append([178.4033025,-18.098674])
    X.append([178.41152,-18.098654])
    X.append([178.40349,-18.107383]) #
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



    # get the density estimation 
    X, Y = np.mgrid[xmin:xmax:150j, ymin:ymax:150j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([m1, m2])


    kernel =stats.gaussian_kde(values,bw_method=None, weights=area_bat)#bw_method=None, weights=area_bat
    Z = np.reshape(kernel(positions).T, X.shape)


    # plot the result
    

    fig, ax = plt.subplots(figsize = (10,10))
    
    
    

    print(xmin,xmax,ymin,ymax)
    plt.imshow(np.rot90(Z), cmap=plt.cm.jet,
            extent=[xmin, xmax, ymin, ymax])


    plt.colorbar()
    #ax.plot(m1, m2, 'k.', markersize=5)



    #ax.plot(m1, m2, 'k.', linewidth=5, markersize=7)


    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.savefig(os.path.join(dir_save, (file + ".png"))) 








img = plt.imread("C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\resultats\\finalmap2.png")
fig, ax = plt.subplots(figsize = (10,10))
plt.imshow(img, cmap=plt.cm.jet,
        extent=[xmin, xmax, ymin, ymax])


plt.colorbar()
ax.plot(m1, m2, 'k.', markersize=0)



#ax.plot(m1, m2, 'k.', linewidth=5, markersize=7)


ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig(os.path.join(dir_save, ("map.png"))) 