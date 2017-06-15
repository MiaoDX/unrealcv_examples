# Config of faster rcnn
import sys, os, logging
sys.path.append('..')


# RCNN config
rcnn_path = '/home/miao/virtual_world/codes/faster_rcnns/Faster-RCNN_TF'
sys.path.append(os.path.join(rcnn_path, 'tools'))
import demo as D # Use demo.py provided in faster-rcnn
import numpy as np
import matplotlib.pyplot as plt

sess = None
net = None

SOFACLASSES = ('__background__',
           'sofa')



def init_tf():
    print("Thies is init_tf")
    global sess, net

    D.cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    args = D.parse_args()

    if args.model == ' ':
        args.model = '/home/miao/virtual_world/codes/faster_rcnns/Pretrained/VGGnet_fast_rcnn_iter_70000.ckpt'
        #raise IOError(('Error: Model not found.\n'))
        
    # init session
    sess = D.tf.Session(config=D.tf.ConfigProto(allow_soft_placement=True))
    # load network
    net = D.get_network(args.demo_net)
    # load model
    saver = D.tf.train.Saver(write_version=D.tf.train.SaverDef.V1)
    saver.restore(sess, args.model)
   
    #sess.run(tf.initialize_all_variables())

    print '\n\nLoaded network {:s}'.format(args.model)

    # Warmup on a dummy image
    im = 128 * np.ones((300, 300, 3), dtype=np.uint8)
    for i in xrange(2):
        _, _= D.im_detect(sess, net, im)
    print("Init_tf done")


def get_sofa_score(sess, net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    #im_file = os.path.join(D.cfg.DATA_DIR, 'demo', image_name)
    #im_file = os.path.join('/home/corgi/Lab/label/pos_frame/ACCV/training/000001/',image_name)
    im_file = image_name
    im = D.cv2.imread(im_file)

    # Detect all object classes and regress object bounds
    timer = D.Timer()
    timer.tic()
    scores, boxes = D.im_detect(sess, net, im)
    timer.toc()
    #print ('Detection took {:.3f}s for {:d} object proposals').format(timer.total_time, boxes.shape[0])

    '''
    # Visualize detections for each class
    im = im[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(im, aspect='equal')
    '''

    CONF_THRESH = 0.8
    NMS_THRESH = 0.3



    #for cls_ind, cls in enumerate(SOFACLASSES[1:]):
    for cls_ind, cls in enumerate(D.CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes,
                          cls_scores[:, np.newaxis])).astype(np.float32)
        keep = D.nms(dets, NMS_THRESH)
        dets = dets[keep, :]


        if cls == 'sofa':
            # copy from vis_detections function
            score = dets[0, -1]
            if score >= CONF_THRESH:
                #print ("succeed")
                pass
            else:
                #print ("failed")
                pass


            return np.float32(score).item()


            # inds = np.where(dets[:, -1] >= CONF_THRESH)[0]
            # if len(inds) == 1: # we only have on sofa
            #     print ("succeed")
            #     #print ("seems we got to find it")
            #     #os.system("pause")
            #     #raw_input('Just a pause')
            #     #D.vis_detections(im, cls, dets, ax, thresh=CONF_THRESH)
            #     #return True
            #     return dets[:, -1] # the score
            # else:
            #     print ("failed")
            #     #return False
            #     return 0.0
            #

"""
if __name__ == '__main__':
    if not net:
        print('Going to init the network')
        init_tf()
        print("init network done")

        imfile = '/home/miao/virtual_world/LinuxNoEditor/RealisticRendering/Binaries/Linux/Loc:00000.29_00104.12_00105.02_Rot:-0014.07_-0030.09_00000.00.png'
        #process_image(imfile)
        D.demo(sess, net, imfile)
        plt.show()
"""


if __name__ == '__main__':
    import time
    if not net:
        print('Going to init the network')
        init_tf()
        print("init network done")

        import json
        camera_trajectory = json.load(open('camera_traj_simple.json'))

        # we only test 5
        camera_trajectory = camera_trajectory

        print ("Total number: {}".format(len(camera_trajectory)))

        starttime = time.time()

        failednum = 0
        failedlist = []
        allnum = len(camera_trajectory)
        for i, item in enumerate(camera_trajectory):

            if i % 50 == 0:
                print ("{}/{} ... {}".format(i, len(camera_trajectory), time.strftime("%Y-%m-%d %H:%M:%S")))


            imfile = '/home/miao/virtual_world/LinuxNoEditor/RealisticRendering/Binaries/Linux/'+item['filename']
            #D.demo(sess, net, imfile)
            #print ("{}/{}, {}".format(i+1, allnum, imfile))

            score = get_sofa_score(sess, net, imfile)

            #print ("score:{}".format(score))

            camera_trajectory[i]['score'] = score

            MY_CONF_THRESH = 0.8 # this can be changed
            if score < MY_CONF_THRESH: # the socre must be large than 0.1
                failednum += 1
                failedlist.append(imfile)

        failedration = float(failednum)/allnum
        print ("After calc, success ratio:{}, fail ration:{}".format(1.0-failedration, failedration))
        print ("Failed images:")
        for im in failedlist:
            print (im)





        # for item in camera_trajectory:
        #     print (item)

        from generate_images_traj import save_to_file
        save_to_file(trajectory=camera_trajectory, filename='camera_traj_with_score.json')

        print ("Saved camera_traj_with_score done")
        print ("ALL DONE")

        endtime = time.time()
        print (endtime)
        print ("Duration:{}s".format(endtime - starttime))
        #plt.show()
