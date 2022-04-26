
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats as stats
import geojson 
from shapely.wkt import loads
from shapely.geometry import mapping
import geojson
import ast
from shapely.geometry import shape










def Extractcoordinates(path):
    """
    Prend chaque point du polygone 
    
    """
    
    with open(path) as f:
        fileImport = geojson.load(f)
    k=0
    i=0
    res=[]
    coord_x_y=[]

    for i in range(len(fileImport['features'])):
            k=0
            if fileImport['features'][i]['geometry']['type']=='MultiPolygon':
                for k in range(len(fileImport['features'][i]['geometry']['coordinates'][0][0])):
                        coord_x_y=[fileImport['features'][i]['geometry']['coordinates'][0][0][k-1][0],fileImport['features'][i]['geometry']['coordinates'][0][0][k-1][1]]
                        res.append(coord_x_y)
                i+=1
            else:
                    
                for k in range(len(fileImport['features'][i]['geometry']['coordinates'][0])):
                
                        coord_x_y=[fileImport['features'][i]['geometry']['coordinates'][0][k-1][0],fileImport['features'][i]['geometry']['coordinates'][0][k-1][1]]
                        res.append(coord_x_y)
                        k+=1
                i+=1
            
                      
    return res
    


def Extractcoordinates2():
    """
    Prend chaque point du polygone 
    
    """
    
    with open("C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\test\\batiments_simulation_2019.01.25.geojson") as f:
        fileImport = geojson.load(f)
    k=0
    i=0
    res=[]
    coord_x_y=[]

    for i in range(len(fileImport['features'])):
            k=0
            if fileImport['features'][i]['geometry']['type']=='MultiPolygon':
                for k in range(len(fileImport['features'][i]['geometry']['coordinates'][0][0])):
                        coord_x_y=[fileImport['features'][i]['geometry']['coordinates'][0][0][k-1][0],fileImport['features'][i]['geometry']['coordinates'][0][0][k-1][1]]
                        res.append(coord_x_y)
                i+=1
            else:
                    
                for k in range(len(fileImport['features'][i]['geometry']['coordinates'][0])):
                
                        coord_x_y=[fileImport['features'][i]['geometry']['coordinates'][0][k-1][0],fileImport['features'][i]['geometry']['coordinates'][0][k-1][1]]
                        res.append(coord_x_y)
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
        













np.random.seed(12)
#X = np.concatenate((np.random.normal(loc = -5, scale= 2, size = (100,3)), np.random.normal(loc = 10, scale= 3, size = (100,3))))



path="C:\\Users\\stefa\\OneDrive\\Desktop\\PROJECT\\test\\batiments_reels_2019.01.25.geojson"

L=Extractcoordinates(path)

L2=CenterPoly(path)


L2 = np.array(L2)
L = np.array(L)




X=L
X2=L2










# get the mesh
m1, m2 = X[:, 0], X[:, 1]
ml1, ml2 = X2[:, 0], X2[:, 1]

xmin = m1.min()
xmax = m1.max()
ymin = m2.min()
ymax = m2.max()

# get the density estimation 
X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([X.ravel(), Y.ravel()])
values = np.vstack([m1, m2])
kernel = stats.gaussian_kde(values)
Z = np.reshape(kernel(positions).T, X.shape)


# plot the result
fig, ax = plt.subplots(figsize = (10,8))

plt.imshow(np.rot90(Z), cmap=plt.cm.jet,
           extent=[xmin, xmax, ymin, ymax])

plt.colorbar()
# ax.plot(m1, m2, 'k.', markersize=5)



ax.plot(m1, m2, 'k.', linewidth=0, markersize=0)
ax.plot(ml1, ml2, 'k.', linewidth=0, markersize=5)

ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.savefig("reels(2019.01.25).png")
plt.show()
