import math

def Supershape(a, b ,m ,n1 ,n2 ,n3 ,num_points):
    path = []

    for n in range(num_points):
        u = m* math.pi * n /num_points

        r = (math.fabs(math.cos(u)/a)**n2 + math.fabs(math.sin(u)/b)**n3)**(-1/n1)
        path.append(r)

    max_r = max(path)

    normalised_path = [r/max_r for r in path]
    return normalised_path

def drawShape(radii,midX ,midY, size=500 ,angle = 0):

    x=[]
    y=[]
    for n in range(len(radii)):
        u = 2*math.pi*n/len(radii)

        x.append(radii[n] * math.cos(u-angle))
        y.append(radii[n] * math.sin(u-angle))

    if max(x) - min(x) > max(y) - min(y):
        scale = size/(max(x)-min(x))
    else:
        scale = size/(max(y)-min(y))

    points= [(x1*scale + midX, y1*scale + midY) for (x1,y1) in zip(x,y)]

    return points


def drawShapes(radii, midX, midY, num_shapes, size,max_width):

    shapes = []

    for i in range(num_shapes):
        shapes.append(drawShape(radii,midX=midX,midY=midY,size = ( i * (max_width/num_shapes) + size) % (max_width + 200)))

    return shapes

