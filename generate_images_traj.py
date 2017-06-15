import numpy as np



def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.1415926535897931
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def angle_degree_between(v1, v2):
    return angle_between(v1, v2)/np.pi*180


def save_to_file(trajectory, filename='camera_traj_simple.json'):
    import json
    if len(trajectory) != 0:
        with open(filename, 'w') as f:
            json.dump(trajectory, f, indent = 2)


"""
Copy and change from [mplot3d/scatter3d_demo.py](https://matplotlib.org/mpl_examples/mplot3d/scatter3d_demo.py)
"""
def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin

def generate_and_plot_points(n, x_min, x_max, y_min, y_max, z_min, z_max, reference_point):
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(reference_point[0], reference_point[1], reference_point[2], c='m', marker='X', s=100) # the couch

    all_xs = []
    all_ys = []
    all_zs = []

    for c, m, xlow, xhigh, ylow, yhigh in [('r', 'o', x_min, 0, y_min, 0), ('b', '^', x_min, 0, 0, y_max), ('g', '*', 0, x_max, y_min, 0), ('y', '+', 0, x_max, 0, y_max)]:
        xs = randrange(n, xlow, xhigh)
        ys = randrange(n, ylow, yhigh)
        zs = randrange(n, z_min, z_max)
        ax.scatter(xs, ys, zs, c=c, marker=m)

        # the add for python list is just append back one by one
        all_xs = all_xs + xs.tolist()
        all_ys = all_ys + ys.tolist()
        all_zs = all_zs + zs.tolist()


    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()
    return all_xs,all_ys,all_zs


def generate_camera_traj(xs, ys, zs, roll_range):
    couch_pos = np.array([180.0, 0.0, 60.0])

    xyzs = zip(xs, ys, zs)

    # https://www.learnopencv.com/rotation-matrix-to-euler-angles/
    # The industry standard is Z - Y - X because that corresponds to yaw, pitch and roll.
    pitch_z_axis = np.array([0.0, 0.0, 1.0]) # the angle between the projection of vector on x-z plane and z-axis is is rotate around y, the pitch
    yaw_x_axis = np.array([1.0, 0.0, 0.0]) # projection on x-y & x-axis is rotating around z, thus yaw

    trajectory= []

    for xyz in xyzs:
        xyz = np.array(xyz)
        relative_vector = couch_pos - xyz

        pitch_projection = [relative_vector[0], 0.0, relative_vector[2]] # y is zero
        yaw_projection = [relative_vector[0], relative_vector[1], 0.0]


        pitch = angle_degree_between(pitch_projection, pitch_z_axis)
        yaw = angle_degree_between(yaw_projection, yaw_x_axis)

        pitch = -(pitch-90) # down view

        if (xyz[1] > 0): # y>0
            yaw = -yaw



        # print ("xyz:{}".format(xyz))
        # print ("pitch:{}".format(pitch))
        # print ("yaw:{}".format(yaw))



        # let's sample some yaw, random 19 plus one 0.0 => 20 rolls
        rols = randrange(19, -roll_range, roll_range).tolist()
        rols.append(0.0)
        for rol in rols:
            rot = [pitch, yaw, rol]

            print ("roatation:{}".format(rot))
            print ("location:{}".format(xyz))

            filename = 'Loc:{:08.2f}_{:08.2f}_{:08.2f}_Rot:{:08.2f}_{:08.2f}_{:08.2f}.png'.format(xyz[0],xyz[1],xyz[2],rot[0],rot[1],rot[2])
            trajectory.append(dict(rotation=rot, location=xyz.tolist(), filename=filename))

    return trajectory



def generate_r_t():
    """
    x:[-180,90]
    y:[-200,150]
    z:[75,230]
    """
    x_min = -180
    x_max = 90
    y_min = -200
    y_max = 150
    z_min = 75
    z_max = 230

    couch_pos = [180.0, 0.0, 60.0]
    n = 100

    xs, ys, zs = generate_and_plot_points(n, x_min, x_max, y_min, y_max, z_min, z_max, couch_pos)
    print (len(xs), len(ys), len(zs))
    return xs, ys, zs

if __name__ == '__main__':

    xs, ys, zs = generate_r_t()

    roll_range = 50 # we can roll from -50 to 50

    trajectory = generate_camera_traj(xs, ys, zs, roll_range)

    save_to_file(trajectory)