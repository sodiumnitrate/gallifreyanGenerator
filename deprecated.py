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