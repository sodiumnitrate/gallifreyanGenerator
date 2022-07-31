import drawSvg as draw
import numpy as np
import pdb


def two_circles(pos1,pos2,r1,r2,drawing=None):
    pos1 = np.array(pos1)
    pos2 = np.array(pos2)

    dist = pos2 - pos1

    d = np.linalg.norm(pos1 - pos2)

    assert(d < r1 + r2)

    dist = dist / d

    if r2 > r1:
        dummy = r2
        r2 = r1
        r1 = dummy
        dist *= -1

    cos_beta = (r2**2+d**2-r1**2)/(2*r2*d)
    cos_alpha = (r1**2+d**2-r2**2)/(2*r1*d)

    angle1 = (2*np.pi - 2*np.arccos(cos_alpha))*180/np.pi
    angle2 = (2*np.arccos(cos_beta))*180/np.pi

    if drawing is None:
        drawing = draw.Drawing(200,100, origin='center')

    theta = np.arccos(dist[0]) * 180/np.pi


    start_angle1 = np.arccos(cos_alpha)*180/np.pi + theta
    start_angle2 = 180 - np.arccos(cos_beta)*180/np.pi + theta

    drawing.append(draw.Arc(pos1[0],pos1[1],r1,start_angle1,start_angle1+angle1,stroke='black',stroke_width=2,fill='none'))
    drawing.append(draw.Arc(pos2[0],pos2[1],r2,start_angle2,start_angle2+angle2,stroke='black',stroke_width=2,fill='none'))

    return drawing

d = two_circles([10,0],[0,20],30,15)

d.saveSvg('example.svg')