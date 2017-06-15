'''
==============
3D scatterplot
==============

Demonstration of a basic scatterplot in 3D.
'''


def plt_location(ax, point_list, reference_point, c='g', marker='o',s=50):
    xs = []
    ys = []
    zs = []
    for item in point_list:
        loc = item['location']
        xs.append(loc[0])
        ys.append(loc[1])
        zs.append(loc[2])
    ax.scatter(xs, ys, zs, c=c , marker=marker, s=s)
    ax.scatter(reference_point[0], reference_point[1], reference_point[2], c='m', marker='X', s=100)  # the couch


def plt_rotation(ax, point_list, c='g', marker='o',s=50):
    xs = []
    ys = []
    zs = []
    for item in point_list:
        rot = item['location']
        xs.append(rot[0])
        ys.append(rot[1])
        zs.append(rot[2])
    ax.scatter(xs, ys, zs, c=c , marker=marker, s=s)



def get_less_and_bigger_than_thresh_list(camera_trajectory, thresh = 0.95):
    less_than_thresh_list = []
    bigger_than_thresh_list = []
    for item in camera_trajectory:
        score = item['score']
        if score < thresh:
            less_than_thresh_list.append(item)
        else:
            bigger_than_thresh_list.append(item)

    print ("less_than_thresh number:{}".format(len(less_than_thresh_list)))

    for item in less_than_thresh_list:
        print (item['filename'], item['score'])

    return less_than_thresh_list, bigger_than_thresh_list


def draw_curve(point_list):
    import matplotlib.pyplot as plt
    import numpy as np


    x_list = []
    y_list = []
    z_list = []
    pitch_list = []
    yaw_list = []
    roll_list = []
    score_list = []
    for item in point_list:
        score = item['score']
        loc = item['location']
        rot = item['rotation']

        score_list.append(score)
        x_list.append(loc[0])
        y_list.append(loc[1])
        z_list.append(loc[2])
        pitch_list.append(rot[0])
        yaw_list.append(rot[1])
        roll_list.append(rot[2])



    fig = plt.figure(1)
    #plt.axis([-0.05, 6.33, -1.05, 1.05])

    p1 = fig.add_subplot(231)
    p1.scatter(x_list, score_list, c='red',marker='o', s=2)
    p1.set_xlabel("x")
    p1.set_ylabel("score")



    p2 = fig.add_subplot(232)
    p2.scatter(y_list, score_list, c='green', marker='o', s=2)
    p2.set_xlabel("y")
    p2.set_ylabel("score")


    p3 = fig.add_subplot(233)
    p3.scatter(z_list, score_list, c='black',marker='o', s=2)
    p3.set_xlabel("z")
    p3.set_ylabel("score")

    p4 = fig.add_subplot(234)
    p4.scatter(pitch_list, score_list, c='pink', marker='o', s=2)
    p4.set_xlabel("pitch")
    p4.set_ylabel("score")

    p5 = fig.add_subplot(235)
    p5.scatter(yaw_list, score_list, c='m',marker='o', s=2)
    p5.set_xlabel("yaw")
    p5.set_ylabel("score")

    p6 = fig.add_subplot(236)
    p6.scatter(roll_list, score_list, c='blue', marker='o', s=2)
    p6.set_xlabel("roll")
    p6.set_ylabel("score")

    plt.show()


def check_location():
    import json
    filename = 'camera_traj_with_score_1.json'
    camera_trajectory = json.load(open(filename))
    print ("Total number: {}".format(len(camera_trajectory)))

    less_than_thresh_list, bigger_than_thresh_list =  get_less_and_bigger_than_thresh_list(camera_trajectory, 0.97)

    couch_pos = [180.0, 0.0, 60.0]

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    plt_location(ax, bigger_than_thresh_list, couch_pos)
    plt_location(ax, less_than_thresh_list, couch_pos, c='r', marker='^',s=60)

    plt.show()

def check_rotation():
    import json
    filename = 'camera_traj_with_score_1.json'
    camera_trajectory = json.load(open(filename))
    print ("Total number: {}".format(len(camera_trajectory)))

    less_than_thresh_list, bigger_than_thresh_list =  get_less_and_bigger_than_thresh_list(camera_trajectory, 0.97)

    couch_pos = [180.0, 0.0, 60.0]

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    plt_rotation(ax, bigger_than_thresh_list)
    plt_rotation(ax, less_than_thresh_list, c='r', marker='^',s=60)

    plt.show()


def check_one_var():
    import json
    filename = 'camera_traj_with_score.json'
    camera_trajectory = json.load(open(filename))
    print ("Total number: {}".format(len(camera_trajectory)))
    draw_curve(camera_trajectory)

if __name__ == '__main__':
    # check_location()
    # check_rotation()
    check_one_var()

