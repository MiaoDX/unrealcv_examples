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

def plot_image(image, boxes=None, scores=None):
    ax.cla() # Clear axis
    ax.imshow(image, aspect='equal')
    ax.axis('off')

    #print(boxes)
    #print(scores)

    #if boxes != None and scores != None:
    if len(boxes) > 0 and len(scores) > None:
        CONF_THRESH = 0.8
        NMS_THRESH = 0.3
        for cls_ind, cls in enumerate(D.CLASSES[1:]):
            cls_ind += 1 # Skip background
            cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind+1)]
            cls_scores = scores[:, cls_ind]
            dets = np.hstack((cls_boxes, cls_scores[:,np.newaxis])).astype(np.float32)
            keep = D.nms(dets, NMS_THRESH)
            dets = dets[keep, :]
            plot_bb(cls, dets, thresh=CONF_THRESH)

    fig.canvas.draw()

def plot_bb(class_name, dets, thresh=0.5):
    inds = np.where(dets[:, -1] >= thresh)[0] #
    if len(inds) == 0:
        return

    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]

        patch = plt.Rectangle((bbox[0], bbox[1]), bbox[2] - bbox[0]
        , bbox[3] - bbox[1], fill=False, edgecolor='red', linewidth=3.5)
        ax.add_patch(patch)
        text = '{:s} {:.3f}'.format(class_name, score)
        ax.text(bbox[0], bbox[1] - 2, text, bbox=dict(facecolor='blue', alpha=0.5)
        , fontsize=14, color='white')

def process_image(filename):
    if not net:
        init_tf() # Tensorflow needs to be started in this thread, otherwise GIL will make it very slow

    print 'Process image: %s' % filename

    if not os.path.isfile(filename):
        print 'Image file %s not exist' % filename
        return

    image = D.cv2.imread(filename)
    timer = D.Timer()
    timer.tic()
    scores, boxes = D.im_detect(sess, net, image)
    timer.toc()
    print ('Detection took {:.3f}s for '
    '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    show_img = image[:,:, (2,1,0)] # Reorder to RGB
    plot_image(show_img, boxes, scores)
    # plot_image(show_img)


def message_handler(message):
    print 'Got server message %s' % repr(message)
    if message == 'clicked':
        image = client.request('vget /camera/0/lit')
        process_image(image)

"""
if __name__ == '__main__':
    if not net:
        print('Going to init the network')
        init_tf()
        print("init network done")

        imfile = '/home/miao/virtual_world/LinuxNoEditor/RealisticRendering/Binaries/00000001.png'
        imfile = '/home/miao/virtual_world/LinuxNoEditor/RealisticRendering/Binaries/Linux_8000/Loc:00001.02_-0101.75_00209.94_Rot:-0039.95_00029.62_00049.50.png'
        #process_image(imfile)
        D.demo(sess, net, imfile)
        plt.show()


"""




if __name__ == '__main__':
    from unrealcv import client
    
    print("This is faster_rcnn tensorflow version.py")
    _L = logging.getLogger('unrealcv')
    _L.setLevel(logging.ERROR)


    if not net:
        init_tf()

    client.message_handler = message_handler
    client.connect()

    if not client.isconnected():
        print 'UnrealCV server is not running. Run the game downloaded from http://unrealcv.github.io first.'
    else:
        # Initialize the matplotlib
        fig, ax = plt.subplots()

        
        # Show an empty image
        image = np.zeros((300, 300))
        ax.imshow(image)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
    client.disconnect()
