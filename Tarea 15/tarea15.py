# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 10:45:09 2022

@author: dcmol
"""
import matplotlib.pyplot as plt
def sumlists(da_list):
    """
    Sums lists.

    Parameters
    ----------
    da_list : A list
    Must consist of lists

    Returns
    -------
    list:
        A list with the concatenated elements of da_list

    """
    if len(da_list)==2:
        return da_list[0]+da_list[1]
    return sumlists([da_list[0],sumlists(da_list[1:])])
def peanostep():
    """

    Returns
    -------
    sequence : list
        List of tuples for the Peano Curve.

    """
    sequence=[(0,0),(0,1),(.5,1),(.5,0),(1,0),(1,1)]
    return sequence
def peanocurve(steps,start=(0,0),scale=1,reflected=False,revers=False):
    """
    Parameters
    ----------
    steps : int
        The number of steps of the curve.
    start : tuple, optional
        For recursion purposes. The position of the curve. The default is (0,0).
    scale : float, optional
        For recursion purposes. The size of the curve. The default is 1.
    reflected : Boolean, optional
        Reflects the curve with respect to axis x. The default is False.
    revers : Boolean, optional
        Reverses the orientation of the curve. The default is False.

    Returns
    -------
    sequence : list
        Returns the sequence of corners in Peano curve.

    """
    if steps==1:
        sequence=peanostep()
        if reflected:
            sequence=[(1-a[0],a[1]) for a in sequence]
        sequence=[(scale*a[0],scale*a[1]) for a in sequence]
        sequence=[(start[0]+a[0],start[1]+a[1]) for a in sequence]
        if revers:
            sequence.reverse()
        return sequence
    keystart=[2*((1-2/steps**3)/3+1/steps**3),(1-2/steps**3)/3+1/steps**3,0]
    recursion=[]
    counter=0
    rev=True
    ref=True
    for i in range(3):
        for j in range(3):
            if counter%3==0:
                rev=not rev
                keystart.reverse()
            counter+=1
            ref=not ref
            recursion.append(peanocurve(steps-1,scale=(1-2/steps**3)/3,
                                        reflected=ref,revers=rev,
                                        start=(keystart[i],keystart[j])))
    sequence=sumlists(recursion)
    if reflected:
        sequence=[(1-a[0],a[1]) for a in sequence]
    sequence=[(scale*a[0],scale*a[1]) for a in sequence]
    sequence=[(start[0]+a[0],start[1]+a[1]) for a in sequence]
    if revers:
        sequence.reverse()
    return sequence
def peanostep3d():
    """

    Returns
    -------
    sequence : list
        List of tuples for the 3d Peano Curve.

    """
    sequence=[(0,0,0),(0,1,0),(0,1,0.5),(0,0,0.5),(0,0,1),(0,1,1),
              (0.5,1,1),(0.5,0,1),(0.5,0,0.5),(0.5,1,0.5),(0.5,1,0),
              (0.5,0,0),(1,0,0),(1,1,0),(1,1,0.5),(1,0,0.5),(1,0,1),(1,1,1)]
    return sequence

def peanocurve3d(steps,start=(0,0,0),scale=1,rotx=0,rotz=0,reflect=False,revers=False):
    """
    Parameters
    ----------
    steps : int
        The number of steps of the curve.
    start : tuple, optional
        For recursion purposes. The position of the curve. The default is (0,0).
    scale : float, optional
        For recursion purposes. The size of the curve. The default is 1.
    rotx : TYPE, optional
        DESCRIPTION. The default is 0.
    rotz : TYPE, optional
        DESCRIPTION. The default is 0.
    reflect : Boolean, optional
        Reflects the curve with respect to a parallel to plane yz. The default is False.
    revers : Boolean, optional
        Reverses the orientation of the curve. The default is False.
    Returns
    -------
    sequence : list
        returns the corners of the 3d Peano curve.

    """
    #pylint: disable=too-many-locals
    #pylint: disable=too-many-arguments
    #pylint: disable=too-many-branches
    #pylint: disable=too-many-statements
    if steps==1:
        sequence=peanostep3d()
        if rotx==180:
            sequence=[(1-a[2],a[1],a[0]) for a in sequence]
            sequence=[(1-a[2],a[1],a[0]) for a in sequence]
        if rotz==180:
            sequence=[(1-a[1],a[0],a[2]) for a in sequence]
            sequence=[(1-a[1],a[0],a[2]) for a in sequence]
        if reflect:
            sequence=[(1-a[0],a[1],a[2]) for a in sequence]
        sequence=[(scale*a[0],scale*a[1],scale*a[2]) for a in sequence]
        sequence=[(start[0]+a[0],start[1]+a[1],start[2]+a[2]) for a in sequence]
        if revers:
            sequence.reverse()
        return sequence
    recursion=[]
    ref=False
    rev=False
    keystart=[2*((1-2/steps**3)/3+1/steps**3),(1-2/steps**3)/3+1/steps**3,0]
    keystart.reverse()
    keyx=keystart.copy()
    counter=0
    for k in range(3):
        if k>0:
            ref=not ref
            rev=not rev
        for i in range(3):
            for j in range(3):
                counter+=1
                if counter%3==1 and counter>1:
                    keystart.reverse()
                recursion.append(peanocurve3d(steps-1,scale=(1-2/steps**3)/3,
                                              rotx=180*j,rotz=180*i,revers=rev,
                                              reflect=ref,
                                              start=(keyx[k],keystart[j],keystart[i])))
            sequence=sumlists(recursion)
    if rotx==90:
        sequence=[(1-a[2],a[1],a[0]) for a in sequence]
    if rotx==180:
        sequence=[(1-a[2],a[1],a[0]) for a in sequence]
        sequence=[(1-a[2],a[1],a[0]) for a in sequence]
    if rotx==270:
        sequence=[(1-a[2],a[1],a[0]) for a in sequence]
        sequence=[(1-a[2],a[1],a[0]) for a in sequence]
        sequence=[(1-a[2],a[1],a[0]) for a in sequence]
    if rotz==90:
        sequence=[(1-a[1],a[0],a[2]) for a in sequence]
    if rotz==180:
        sequence=[(1-a[1],a[0],a[2]) for a in sequence]
        sequence=[(1-a[1],a[0],a[2]) for a in sequence]
    if rotz==270:
        sequence=[(1-a[1],a[0],a[2]) for a in sequence]
        sequence=[(1-a[1],a[0],a[2]) for a in sequence]
        sequence=[(1-a[1],a[0],a[2]) for a in sequence]
    if reflect:
        sequence=[(1-a[0],a[1],a[2]) for a in sequence]
    sequence=[(scale*a[0],scale*a[1],scale*a[2]) for a in sequence]
    sequence=[(start[0]+a[0],start[1]+a[1],start[2]+a[2]) for a in sequence]
    if revers:
        sequence.reverse()
    return sequence
def draw2dcurve(curv):
    """
    Draws a given 2d discrete curve
    Parameters
    ----------
    curv : list
        list of points of curve.

    Returns
    -------
    None.
    """
    x_points=[a[0] for a in curv]
    y_points=[a[1] for a in curv]
    plt.figure(figsize=(5,5))
    plt.axis('equal')
    print(curv)
    plt.plot(x_points,y_points,linewidth=0.5)
    plt.xticks([0,1])
    plt.yticks([0,1])
    plt.show()
def draw3dcurve(curv):
    """
    Draws a given 3d discrete curve
    Parameters
    ----------
    curv : list
        list of points of curve.

    Returns
    -------
    None.
    """
    x_points=[a[0] for a in curv]
    y_points=[a[1] for a in curv]
    z_points=[a[2] for a in curv]
    plt.ion()
    fig=plt.figure(figsize=(5,5))
    da_axis= fig.add_subplot(111, projection='3d')
    plt.plot(x_points,y_points,z_points,linewidth=0.5)
    plt.xticks([0,1])
    plt.yticks([0,1])
    da_axis.set_zticks([0,1])
    plt.show()
draw3dcurve(peanocurve3d(3))
