
image_distance = 0
focal_length = 9 # adjusted for dji mavic mini
altitude = 15

def distance_formula(x1, x2, y1, y2):
  distance = ((x2-x1)**2 + (y2-y1)**2)**1/2
  return distance

def object_distance(obj1_x, obj1_y, obj2_x, obj2_y):
  #image_distance = distance_formula(obj1_x, obj2_x, obj1_y, obj2_y)
  image_distance = 224
  object_distance = (image_distance * altitude) / (focal_length * 10**5)
  return object_distance


image_distance = 866
object_distance = ((image_distance * altitude) / (focal_length * 10**3)) * 18 / 5
print(object_distance)
