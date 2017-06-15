# This is a 10 lines python example to show how to generate an image dataset with image, depth and object_mask.
# Read https://unrealcv.github.io/tutorial/getting_started.html before trying this script
# Note: if you need high-accuracy depth, please use `vget /camera/0/depth depth.exr`
import json
import time
from unrealcv import client

camera_trajectory = json.load(open('camera_traj_simple.json'))
print ("Total number: {}".format(len(camera_trajectory)))

client.connect()
# Get object information
obj_info = client.request('vget /objects')



import datetime,time

now = time.strftime("%Y-%m-%d %H:%M:%S")
print(now)
starttime = time.time()
print (starttime)


for i, item in enumerate(camera_trajectory):

    if i%100 == 0:
        print ("{}/{} ... {}".format(i, len(camera_trajectory), time.strftime("%Y-%m-%d %H:%M:%S")))

    loc = item['location']
    rot = item['rotation']
    # Set position of the first camera
    client.request('vset /camera/0/location {} {} {}'.format(loc[0], loc[1], loc[2]))
    client.request('vset /camera/0/rotation {} {} {}'.format(rot[0], rot[1], rot[2]))
    # Get image and ground truth
    # modes = ['lit', 'depth', 'object_mask']
    # [im, dep, obj] = [client.request('vget /camera/0/{}'.format(m)) for m in modes]
    # print ['{} is saved to {}'.format(k, v) for (k,v) in zip(modes, [im, dep, obj])]

    """
    modes = ['lit','object_mask']
    time.sleep(0.01)  # make sure the image is ready, no blur or similar effects
    im = client.request('vget /camera/0/lit')
    time.sleep(0.01)
    dep = client.request('vget /camera/0/object_mask')
    print ['{} is saved to {}'.format(k, v) for (k,v) in zip(modes, [im, dep])]
    """

    time.sleep(0.01)  # make sure the image is ready, no blur or similar effects
    im = client.request('vget /camera/0/lit {}'.format(item['filename']))

now = time.strftime("%Y-%m-%d %H:%M:%S")
print(now)
endtime = time.time()
print (endtime)
print ("Duration:{}s".format(endtime-starttime))
