# A toy example to use python to control the game.
import sys
sys.path.append('..')
from unrealcv import client
import matplotlib.pyplot as plt
import numpy as np

help_message = '''
A demo showing how to control a game using python
a, d: rotate camera to left and right.
q, e: move camera up and down.
'''
plt.rcParams['keymap.save'] = ''

def get_cur_position():
    now_loc_str = client.request('vget /camera/0/location')
    now_rot_str = client.request('vget /camera/0/rotation')
    print ("Current location")
    print (now_loc_str)
    print (now_rot_str)
    print ("")


def onpress(event):
    rot_step = 1
    loc_step = 5

    print event.key



    if event.key == '1':
        rot[0] += rot_step
    if event.key == '2':
        rot[0] -= rot_step
    if event.key == '3':
        rot[1] += rot_step
    if event.key == '4':
        rot[1] -= rot_step
    if event.key == '5':
        rot[2] += rot_step
    if event.key == '6':
        rot[2] -= rot_step

    if event.key == 'z':
        rot[0] = 0
    if event.key == 'x':
        rot[1] = 0
    if event.key == 'c':
        rot[2] = 0

    if event.key == 'q':
        loc[0] += loc_step
    if event.key == 'w':
        loc[0] -= loc_step
    if event.key == 'e':
        loc[1] += loc_step
    if event.key == 'r':
        loc[1] -= loc_step
    if event.key == 't':
        loc[2] += loc_step
    if event.key == 'y':
        loc[2] -= loc_step





    cmd = 'vset /camera/0/rotation %s' % ' '.join([str(v) for v in rot])
    client.request(cmd)
    cmd = 'vset /camera/0/location %s' % ' '.join([str(v) for v in loc])
    client.request(cmd)

    if event.key == 'p':
        get_cur_position()

    if event.key == 's': # seems we should shoot the object_mask first, possible a bug
        #client.request('vget /camera/0/object_mask')
        client.request('vset /viewmode object_mask')

    if event.key == 'd': # shoot back
        client.request('vset /viewmode lit')

    if event.key == 'o':
        # Get a list of all objects in the scene
        scene_objects = client.request('vget /objects').split(' ')
        print('There are %d objects in this scene' % len(scene_objects))
        print(scene_objects)

    """
    # failed to run as a program, but okay in command line
    if event.key == 'n': # shoot back
        print ("set new init location")
        #get_cur_position()
        new_loc = [float(v) for v in client.request('vget /camera/0/location').split(' ')]
        new_rot = [float(v) for v in client.request('vget /camera/0/rotation').split(' ')]
        loc[0] = new_loc[0]
        loc[1] = new_loc[2]
        loc[2] = new_loc[2]
        rot[0] = new_rot[0]
        rot[1] = new_rot[1]
        rot[2] = new_rot[2]
    """

loc = None
rot = None
def main():
    client.connect()
    if not client.isconnected():
        print 'UnrealCV server is not running. Run the game from http://unrealcv.github.io first.'
        return
    else:
        print help_message

    #init_loc = [float(v) for v in client.request('vget /camera/0/location').split(' ')]
    #init_rot = [float(v) for v in client.request('vget /camera/0/rotation').split(' ')]

    init_loc = [  80.32575164,   53.36482714,  112.20281103]
    init_rot = [-27.6425879453, -28.1642545592, 0]



    global rot, loc
    loc = init_loc; rot = init_rot
    image = np.zeros((300, 300))

    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('key_press_event', onpress)
    ax.imshow(image)
    plt.title('Keep this window in focus, used to receive key press event')
    plt.axis('off')
    plt.show() # Add event handler


if __name__ == '__main__':
    main()
