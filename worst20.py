
def plot_worst(im_name_with_score):
    import matplotlib.pyplot as plt
    import cv2

    imread = lambda x: cv2.imread(x)[:,:,(2,1,0)]

    base_dir = '/home/miao/virtual_world/LinuxNoEditor/RealisticRendering/Binaries/Linux_8000/'

    #ims = ['0_100.png', '400_500.png', '800_900.png', '1200_1300.png', '1600_1700.png', '1900_2000.png']


    fig, axes = plt.subplots(nrows=5, ncols=6)
    for i, ax in enumerate(axes.flat):
        #im = ax.imshow(np.random.random((10,10)), vmin=0, vmax=1)
        im_name, im_score = im_name_with_score[i]



        im = imread(base_dir + im_name)
        ax.imshow(im)
        ax.set_title('{:.4f}'.format(im_score))
        ax.axis('off')

    plt.subplots_adjust(left=0.02, right=0.98, top=0.96, bottom=0.02, hspace=0.15, wspace=0.20)
    #fig.subplots_adjust(right=0.8)
    #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    #fig.colorbar(im, cax=cbar_ax)

    plt.show()

if __name__ == '__main__':

    from operator import itemgetter
    from pprint import pprint
    from generate_images_traj import save_to_file
    import json

    camera_trajectory = json.load(open('camera_traj_with_score.json'))

    #camera_trajectory = camera_trajectory[:10]

    print ("Total number: {}".format(len(camera_trajectory)))

    #camera_trajectory.sort(key=itemgetter("score"))

    camera_trajectory_sorted = sorted(camera_trajectory, key=lambda item: item['score'])

    pprint (camera_trajectory_sorted[:10])




    im_score = []
    for item in camera_trajectory_sorted:
        im_score.append(item['score'])

    import matplotlib.pyplot as plt
    plt.figure("hist")
    arr=im_score
    n, bins, patches = plt.hist(arr, bins=1000, normed=0, facecolor='green', alpha=0.75, log=True)
    plt.xlabel('score')
    plt.ylabel('number')
    plt.title('The number of experiments with score')
    plt.show()



    save_to_file(camera_trajectory_sorted, 'camera_traj_sorted.json')

    im_name_with_score = []
    for item in camera_trajectory_sorted[150:180]:
        im_name_with_score.append( (item['filename'], item['score']) )

    plot_worst(im_name_with_score)
