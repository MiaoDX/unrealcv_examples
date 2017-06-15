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

if __name__ == '__main__':
    # check_location()
    check_rotation()


