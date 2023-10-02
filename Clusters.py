import matplotlib.pyplot as Plt
import math
import random
import matplotlib.colors as mc

def ReadFile(string):
   points = []
   with open(string, 'r') as file:
        for row in file:
            point = [float(item) for item in row.strip().split()]
            points.append(point)
   return points

def generate_colors(numberOfColors):
   colors = mc.ListedColormap(list(mc.TABLEAU_COLORS.values())[:numberOfColors])
   Take_Solid_Colors = [colors(i) for i in range(numberOfColors)] 
   return Take_Solid_Colors

def Distance(points,centers):
   distance =sum((x-y)**2 for x, y in zip(points,centers))
   distance = math.sqrt(distance)
   return distance

def Add_clusters(points,centers):
   clusters = [[] for _ in range(len(centers))]
   for point in points:
      min_dist = float('inf')
      nearest_center = None
      for i, center in enumerate(centers):
         distance = Distance(point,center)
         if distance < min_dist:
            min_dist = distance
            nearest_center = i
      clusters[nearest_center].append(point)
   return clusters

def cal_centers(points):
   num_points = len(points)
   lenth = len(points[0])
   center = [sum(point[i] for point in points)/num_points for i in range(lenth)]
   return center

def Regenerate_New_Centers(clusters):
   centers = [cal_centers(cluster) for cluster in clusters]
   return centers

def converged_or_not(old_centers,new_centers, threshold = 50):
   distances = [sum((x - y) ** 2 for x, y in zip(old, new)) ** 0.5
                 for old, new in zip(old_centers, new_centers)]
   return all(distance < threshold for distance in distances)

def draw_plot(clusters,centers,k):
   colors = generate_colors(k)
   for i, cluster in enumerate(clusters):
      points_x = [point[0] for point in cluster]
      points_y = [point[1] for point in cluster]
      Plt.scatter(points_x, points_y, c = colors[i],label = f'cluster {i+1}')
   centers_x = [center[0] for center in centers]
   centers_y = [center[1] for center in centers]
   Plt.scatter(centers_x, centers_y, c='black',marker='*',label='Centers')
   Plt.legend()
   Plt.xlabel('X-axis')
   Plt.ylabel('Y-axis')
   Plt.title('K-Means Clustering')
   Plt.show()

def clustraing (points,k,max_iteration=500):
   centers = random.sample(points,k)
   clusters = None
   for i in range(1,max_iteration+1):
      clusters = Add_clusters(points,centers)

      new_centers = Regenerate_New_Centers(clusters)

      if i > 1 and converged_or_not(centers,new_centers):
         break
      centers = new_centers
   return clusters,centers
   
points = ReadFile("jain_feats.txt")

k = int(input("How many Centers do you need?: "))

clusters, centers = clustraing(points,k)

print("Centers: \n", centers)
for i, cluster in enumerate(clusters):
    print(f"Cluster {i+1}: \n", cluster)


draw_plot(clusters,centers,k)