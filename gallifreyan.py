import drawSvg as draw
import numpy as np
import pdb
from word_splitter import *
import sys

word = sys.argv[1]

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

def rough_word_layout(word, scale=1):
    # get number of groups and divide word circle
    groups = get_split_word(word)
    num_groups = len(groups)
    theta = 2*np.pi/num_groups

    # separation between groups
    separation = 2 * scale
    rad_consonant_circle = 15 * scale
    rad_word_circle = (separation + rad_consonant_circle) / np.sin(theta/2)
    
    rad_vowel_circle = rad_word_circle / 8

    drawing = draw.Drawing(rad_word_circle*4,rad_word_circle*4, origin='center')
    drawing.append(draw.Circle(0,0,rad_word_circle,fill='none',stroke='black'))

    angle = 0
    print(groups)
    for group in groups:
        vowel, consonant = get_consonant_vowel_groups(group)
        x,y = rad_word_circle * np.cos(angle), rad_word_circle * np.sin(angle)
        
        # draw the vowel
        # TODO: figure out vowel placement and decorations later
        if vowel != "":
            if vowel in "EIU":
                x_v,y_v = x,y
                if vowel == "I":
                    # draw line from edge of vowel circle to the center of the word circle
                    rad = rad_word_circle - rad_vowel_circle 
                    lx,ly = rad * np.cos(angle), rad * np.sin(angle)
                    drawing.append(draw.Line(0,0,lx,ly,fill='none',stroke='black'))
                elif vowel == "U":
                    # draw line from edge of vowel circle, outward, radially
                    length = rad_word_circle * 2
                    rad = rad_word_circle + rad_vowel_circle
                    x1,y1 = rad * np.cos(angle), rad * np.sin(angle)
                    x2,y2 = (rad + length) * np.cos(angle), (rad + length) * np.sin(angle)
                    drawing.append(draw.Line(x1,y1,x2,y2,fill='none',stroke='black'))

            elif vowel == "A":
                rad = rad_word_circle + rad_vowel_circle * 4
                x_v,y_v = rad * np.cos(angle), rad * np.sin(angle)
            else:
                # vowel = O
                rad = rad_word_circle - rad_vowel_circle * 4
                x_v,y_v = rad * np.cos(angle), rad * np.sin(angle)
            drawing.append(draw.Circle(x_v,y_v,rad_vowel_circle,fill='none',stroke='black'))

        # draw the consonant
        # TODO: figure out placement and decorations later
        if consonant != "":
            drawing.append(draw.Circle(x,y,rad_consonant_circle,fill='none',stroke='black'))

        angle += theta

    return drawing


# draw two intersecting arcs
#d = two_circles([10,0],16,370,15,30)
d = rough_word_layout(word,scale=2)
d.saveSvg('example.svg')