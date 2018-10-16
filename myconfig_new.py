# coding: utf-8

############################
# This configuration file sets various parameters for generation of training
# set file & evalutation of results
############################

# myconfig.py:

########################################
# Step 1:
Task = 'experiment'
########################################

# Filename and path to behavioral video:
vidpath = '.'
filename = 'experimentvideo1.avi'

cropping = False

# ROI dimensions / bounding box (only used if cropping == True)
# x1,y1 indicates the top left corner and
# x2,y2 is the lower right corner of the croped region.

x1 = 0
x2 = 640
y1 = 277
y2 = 624

# Portion of the video to sample from in step 1. Set to 1 by default.
portion = 1

########################################
# Step 2:
########################################

bodyparts = ['l_akle', 'l_ear', 'l_elbow', 'l_eye', 'l_hip', 'l_kee', 'l_shoulder', 'l_wrist', 'ose', 'r_akle', 'r_ear', 'r_elbow', 'r_eye', 'r_hip', 'r_kee', 'r_shoulder', 'r_wrist']  # Exact sequence of labels as were put by
# annotator in *.csv file
Scorers = ['labeller_1']  # who is labeling?

# Set this true if the data was sequentially labeled and if there is one file per folder (you can set the name of this file below, i.e. multibodypartsfilename)
# Otherwise there should be individual files per bodypart, i.e. in our demo case hand.csv, Finger1.csv etc.

multibodypartsfile=False
multibodypartsfilename="results.csv"

# When importing the images and the labels in the csv/xls files should be in the same order!
# During labeling in Fiji one can thus (for occluded body parts) click in the origin of the image
#(i.e. top left corner (close to 0,0)), these "false" labels will then be removed. To do so set the following variable:
#set this to 0 if no labels should be removed!

invisibleboundary=10 # If labels are closer to origin than this number they are set to NaN (not a number). Please adjust to your situation. Units in pixel.

########################################
# Step 3:
########################################

date = 'Sep'
scorer = 'labeller_1'

# Userparameters for training set. Other parameters can be set in pose_cfg.yaml
Shuffles = [1]  # Ids for shuffles, i.e. range(5) for 5 shuffles
TrainingFraction = [0.95]  # Fraction of labeled images used for training

# Which resnet to use
# (these are parameters reflected in the pose_cfg.yaml file)
resnet = 50

trainingsiterations='5000'

# For Evaluation/ Analyzing videos
# To evaluate the last model that was trained most set this to: -1
# To evaluate all models (training stages) set this to: "all"  (as string!)

snapshotindex = -1 #"all"
shuffleindex = 0
pcutoff=.1 # likelihood. RMSE will be reported for all pairs and pairs with larger likelihood than pcutoff (see paper). This cutoff will also be used in plots.
plotting=True #If true will plot train & test images including DeepLabCut labels next to human labels. Note that this will be plotted for all snapshots as indicated by snapshotindex
