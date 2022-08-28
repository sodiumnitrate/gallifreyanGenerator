import drawSvg as draw
import numpy as np
import pdb
from word_splitter import *
import sys

word = sys.argv[1]

consonant_class = {"B":"tangent", "J":"inside", "T":"bubble", "TH":"on",
                   "PH":"inside", "WH":"bubble", "GH":"on",
                   "CH":"tangent", "K":"inside", "SH":"bubble", "Y":"on",
                   "D":"tangent", "L":"inside", "R":"bubble", "Z":"on",
                   "C":"inside", "Q":"on",
                   "G":"tangent", "N":"inside", "V":"bubble", "QU":"on",
                   "H":"tangent", "P":"inside", "W":"bubble", "X":"on",
                   "F":"tangent", "M":"inside", "S":"bubble", "NG":"on"}

consonant_dots = {"B":0, "J":0, "T":0, "TH":0,
                   "PH":1, "WH":1, "GH":1,
                   "CH":2, "K":2, "SH":2, "Y":2,
                   "D":3, "L":3, "R":3, "Z":3,
                   "C":4, "Q":4,
                   "G":0, "N":0, "V":0, "QU":0,
                   "H":0, "P":0, "W":0, "X":0,
                   "F":0, "M":0, "S":0, "NG":0}

consonant_lines = {"B":0, "J":0, "T":0, "TH":0,
                   "PH":0, "WH":0, "GH":0,
                   "CH":0, "K":0, "SH":0, "Y":0,
                   "D":0, "L":0, "R":0, "Z":0,
                   "C":0, "Q":0,
                   "G":1, "N":1, "V":1, "QU":1,
                   "H":2, "P":2, "W":2, "X":2,
                   "F":3, "M":3, "S":3, "NG":3}

def two_circles(pos1,d,omega,r1,r2,drawing=None):
    '''
    Creates two intersecting circular arcs based on the position of the larger circle,
    the distance between two circles, and the relative orientation of circles.
    '''

    # relative orientation in radians
    omega = omega * np.pi/180

    # make sure that the first circle is the bigger one
    if r2 > r1:
        dummy = r2
        r2 = r1
        r1 = dummy

    # position of the first circle
    pos1 = np.array(pos1)
    # position of the second circle
    pos2 = pos1 + np.array([d*np.cos(omega),d*np.sin(omega)])

    # distance vector between two circle centers
    dist = pos2 - pos1

    # normalized distance vector
    dist = dist / d

    # make sure the distance between two circles is such that they intersect
    assert(d < r1 + r2)
    assert(d > r1-r2)

    # calculate arc angles using cosine rule
    cos_beta = (r2**2+d**2-r1**2)/(2*r2*d)
    cos_alpha = (r1**2+d**2-r2**2)/(2*r1*d)
    angle1 = (2*np.pi - 2*np.arccos(cos_alpha))*180/np.pi
    angle2 = (2*np.arccos(cos_beta))*180/np.pi

    # if there's no drawing object, create one
    if drawing is None:
        drawing = draw.Drawing(200,100, origin='center')

    # calculate starting angles of arcs 
    theta = np.arctan2(dist[1],dist[0]) * 180/np.pi
    start_angle1 = np.arccos(cos_alpha)*180/np.pi + theta
    start_angle2 = 180 - np.arccos(cos_beta)*180/np.pi + theta

    # draw the two arcs
    drawing.append(draw.Arc(pos1[0],pos1[1],r1,start_angle1,start_angle1+angle1,stroke='black',stroke_width=2,fill='none'))
    drawing.append(draw.Arc(pos2[0],pos2[1],r2,start_angle2,start_angle2+angle2,stroke='black',stroke_width=2,fill='none'))

    return drawing

def consonant_arc(d,omega,r1,r2):
    # position of the circle
    pos = np.array([d*np.cos(omega),d*np.sin(omega)])

    # normalized distance vector
    dist = np.array([np.cos(omega), np.sin(omega)])

    # calculate arc angles
    cos_beta = (r2**2+d**2-r1**2)/(2*r2*d)
    cos_alpha = (r1**2+d**2-r2**2)/(2*r1*d)
    angle = (2*np.arccos(cos_beta))*180/np.pi

    theta = np.arctan2(dist[1],dist[0]) * 180/np.pi
    start_angle = 180 - np.arccos(cos_beta)*180/np.pi + theta

    return draw.Arc(pos[0],pos[1],r2,start_angle,start_angle+angle,stroke='black',fill='none')



def word_layout(word, scale=1):
    # get number of groups and divide word circle
    groups = get_split_word(word)
    num_groups = len(groups)
    theta = 2*np.pi/num_groups
    decoration_angle = theta/5

    # separation between groups
    separation = 2 * scale
    rad_consonant_circle = 15 * scale
    rad_word_circle = (separation + rad_consonant_circle) / np.sin(theta/2) * 2
    
    rad_vowel_circle = rad_consonant_circle / 6
    rad_decoration_circle = rad_vowel_circle / 2

    drawing = draw.Drawing(rad_word_circle*4,rad_word_circle*4, origin='center')
    drawing.append(draw.Circle(0,0,rad_word_circle,fill='none',stroke='black'))

    angle = 0
    print(groups)
    for group in groups:
        vowel, consonant = get_consonant_vowel_groups(group)

        # draw the consonant
        if consonant != "":
            if consonant_class[consonant] == "on":
                x,y = rad_word_circle * np.cos(angle), rad_word_circle * np.sin(angle)
                drawing.append(draw.Circle(x,y,rad_consonant_circle,fill='none',stroke='black'))
            elif consonant_class[consonant] == "inside":
                rad = rad_word_circle - rad_consonant_circle - separation * 2
                x,y = rad * np.cos(angle), rad * np.sin(angle)
                drawing.append(draw.Circle(x,y,rad_consonant_circle,fill='none',stroke='black'))
            elif consonant_class[consonant] == "tangent":
                rad = rad_word_circle - rad_consonant_circle + separation / 2
                x,y = rad * np.cos(angle), rad * np.sin(angle)
                d = np.sqrt(x**2+y**2)
                drawing.append(consonant_arc(d,angle,rad_word_circle,rad_consonant_circle))
            elif consonant_class[consonant] == "bubble":
                x,y = rad_word_circle * np.cos(angle), rad_word_circle * np.sin(angle)
                d = np.sqrt(x**2+y**2)
                drawing.append(consonant_arc(d,angle,rad_word_circle,rad_consonant_circle))

        # add consonant decoration
        # TODO: try to do this by taking in to consideration where all the other stuff are
        if consonant != "":
            dots = consonant_dots[consonant]
            lines = consonant_lines[consonant]

            for l in range(1,lines+1):
                delta = angle + decoration_angle * l
                length = rad_consonant_circle * 2
                x2,y2 = x - length * np.cos(delta), y - length * np.sin(delta)
                x1,y1 = length/2 * np.cos(delta) + x2, length/2 * np.sin(delta) + y2
                drawing.append(draw.Line(x1,y1,x2,y2,fill='none',stroke='black'))

            for d in range(1,dots+1):
                delta = angle + decoration_angle * d * 2
                length = rad_consonant_circle * 2
                x2,y2 = x - length * np.cos(delta), y - length * np.sin(delta)
                x1,y1 = length/2 * np.cos(delta) + x2, length/2 * np.sin(delta) + y2
                drawing.append(draw.Circle(x1,y1,rad_decoration_circle,fill='black',stroke='none'))

        # draw the vowel
        # TODO: figure out vowel placement later
        if vowel != "":
            if vowel in "EIU":
                if consonant == "":
                    x_v,y_v = rad_word_circle * np.cos(angle), rad_word_circle * np.sin(angle)
                else:
                    x_v,y_v = x,y
                if vowel == "I":
                    # draw line from edge of vowel circle to the center of the word circle
                    rad = x_v/np.cos(angle) - rad_vowel_circle
                    #rad = rad_word_circle - rad_consonant_circle - rad_vowel_circle 
                    lx,ly = rad * np.cos(angle), rad * np.sin(angle)
                    drawing.append(draw.Line(0,0,lx,ly,fill='none',stroke='black'))
                elif vowel == "U":
                    # draw line from edge of vowel circle, outward, radially
                    length = rad_word_circle 
                    rad = rad_word_circle + rad_vowel_circle
                    x1,y1 = rad_vowel_circle*np.cos(angle) + x_v, rad_vowel_circle*np.sin(angle)+y_v
                    x2,y2 = (rad + length) * np.cos(angle), (rad + length) * np.sin(angle)
                    drawing.append(draw.Line(x1,y1,x2,y2,fill='none',stroke='black'))

            elif vowel == "A":
                rad = rad_word_circle + rad_vowel_circle * 2
                x_v,y_v = rad * np.cos(angle), rad * np.sin(angle)
            else:
                # vowel = O
                if consonant == "":
                    rad = rad_word_circle - rad_vowel_circle * 4
                    x_v,y_v = rad * np.cos(angle), rad * np.sin(angle)
                else:
                    x_v = x - rad_consonant_circle * np.cos(angle)
                    y_v = y - rad_consonant_circle * np.sin(angle)
            drawing.append(draw.Circle(x_v,y_v,rad_vowel_circle,fill='none',stroke='black'))

        angle += theta

    return drawing

# draw two intersecting arcs
d = word_layout(word,scale=2)
d.saveSvg('example.svg')