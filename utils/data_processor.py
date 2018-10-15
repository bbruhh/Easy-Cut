import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import glob
import os
from collections import defaultdict
import itertools
import cv2
import matplotlib.pyplot as plt
import json

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def merge_dicts(a,b):
    de = defaultdict(list, a)
    for i, j in b.items():
        de[i].extend(j)
    return de

def polygon_xml(ob):
    tlist = []
    ylist = []
    xlist = []
    for itrial in ob.iter('polygon'):# go thru polygons
        for ifield in itrial: 
            if ifield.tag == 't':
                t = int(ifield.text)
            if ifield.tag == 'pt':
                for ipt in ifield:
                    if ipt.tag == 'x':
                        xlist.append(int(ipt.text)) 
                    elif ipt.tag == 'y':
                        ylist.append(int(ipt.text))
                        tlist.append(t)
    return tlist, xlist, ylist

def video_xml(fpath,user):
    tree = ET.parse(fpath)
    root = tree.getroot()
    zpartlist = []; ztlist = []; zxlist = []; zylist = [];
    for ob in root.iter('object'): # goes through body parts
        for iname in ob.iter('name'):
            dum=1
        tlist,xlist,ylist = polygon_xml(ob)
        partlist = [iname.text]*len(tlist)
        zpartlist.extend(partlist)
        ztlist.extend(tlist)
        zxlist.extend(xlist)
        zylist.extend(ylist)
    flist = [int(os.path.basename(fpath)[1:-4])]*len(zylist)
    userlist = [user]*len(zylist)
    return {'user':userlist,'video':flist,'part': zpartlist, 'x': zxlist, 'y': zylist, 't': ztlist}

def box_coco(df):
    df = df.reset_index()
    boxlist = np.asarray([np.min(df.x), np.min(df.y), np.max(df.x)-np.min(df.x), np.max(df.y)-np.min(df.y)]) # l,b,w,h
    xy = np.asarray([val for pair in zip(df.x, df.y) for val in pair])
    df_out = df.loc[0,:]
    df_out['box'] = boxlist
    df_out['box_seg'] = xy
    df_out = df_out[['part','x', 'y', 'box','box_seg']]
    return df_out



def build_list(row_idx,xs):
    nparts = 17
    x_list =[0]*nparts
    for i, irow in enumerate(row_idx):
        x_list[int(irow)] = xs[i]
    return x_list

def rescale_values(df):
    df['max'] = df[["ncols", "nrows"]].max(axis=1)
    new_max = 640
    cols = ['x','y', 'ncols', 'nrows','box', 'box_seg'] 
    df[cols] = df[cols].div(df['max'],axis=0)*new_max
    for icol in cols:
        if (icol == 'ncols')|(icol == 'nrows'):
            df[icol] = df[icol].astype(int)
        else:
            df[icol] = df[icol].apply(np.around)
    return df

def get_image(df):
    df = df.reset_index().loc[0,:]
    return {'file_name':str(df.imageid)+'.jpg', 'id': df.imageid, 'height':int(df.nrows), 'width':int(df.ncols)}

def frame_reduce(df,step):
    return df.reset_index().loc[df.reset_index().t % step == 0,:].drop(['video','partlabel','index', 'person'],axis=1)

def df_DLC_format(df,user):
    df_x = df
    df_x['ax'] = 'x'
    df_x['coord'] = df_x['x']

    df_y = df_x.copy()
    df_y['ax'] = 'y'
    df_y['coord'] = df_y['y']

    df_1 = df_x.append(df_y).sort_values('partlabel')

    arrays = [np.asarray([user]*len(df_1.partlabel)),np.array(df_1.partlabel),np.array(df_1.ax)]
    index = pd.MultiIndex.from_arrays(arrays, names=('scorer', 'bodyparts', 'coords'))
    coord = df_1.coord
    rowname = ['infantvideos1/'+str(df.reset_index().imageid[0])+'.jpg']
    return pd.DataFrame(data=np.asarray(coord), index = index,columns = rowname).transpose()

zuser = 'labeller_1'

step = 4 # how many frames? 1 in 'step' frames

new_max = 640 # images are resized relative to some max npixels. Images in COCO are max 640 pixels

npartitions = 2 # how many partitions for train/test division? typical would be 10

imagepath = './data/image/*'
xmlpath = './data/xml/*'
csvpath = './data/labels_NN_input'
outputimagepath = './data/image_NN_input'

parts = ['ose', 'l_eye', 'r_eye', 'l_ear', 'r_ear', 'l_shoulder', 'r_shoulder', 'l_elbow', \
 'r_elbow', 'l_wrist', 'r_wrist', 'l_hip', 'r_hip', 'l_kee', 'r_kee', 'l_akle', 'r_akle']

if 1-os.path.isdir(csvpath):
    os.mkdir(csvpath)

df = pd.DataFrame()

# find image size for each folder
vidlist = []; rowlist = []; collist = []
img_folder = sorted(glob.glob(imagepath))
for fpath in img_folder:
    imgfile = sorted(glob.glob(os.path.join(fpath,'*')))[0]
    vidlabel = int(os.path.basename(fpath)[1:])
    img = cv2.imread(imgfile,0)
    nrows = len(img)
    ncols = len(img[0])
    vidlist.append(vidlabel); rowlist.append(nrows); collist.append(ncols);    
df_vid = pd.DataFrame(dict(video = vidlist, nrows = rowlist, ncols = collist))

# loop over user folders, get annotations
xml_folder = sorted(glob.glob(xmlpath))
zdict = {'user':[],'video':[],'part': [], 'x': [], 'y': [], 't': []}
for fpaths in xml_folder:
    user = os.path.basename(fpaths)
    fpaths = sorted(glob.glob(os.path.join(fpaths,'*.xml')))
    for fpath in fpaths:
        dict_file = video_xml(fpath, user)
        zdict = merge_dicts(zdict,dict_file)

df = pd.DataFrame(zdict, columns=['user','video', 'part', 'x', 'y', 't'])
df['box'] = np.nan; df['box_seg'] = np.nan; df['partnumber'] = np.nan
df['person'] = df['part'].str[-1:].astype(int)

df['partlabel'] = df['part'].str[:-4]
# dfbox = df[df.partlabel=='bbox']
dfparts = df[df.partlabel!='bbox']
dfparts = dfparts.groupby(['user', 'video','person','partlabel','t']).mean().reset_index()
# dfbox = dfbox.groupby(['user', 'video','person','partlabel','t']).apply(box_coco).reset_index()

df1 = dfparts[['user','video','person','partlabel','partnumber','t','x','y','box', 'box_seg']]
for ii,ipart in enumerate(parts):
    df1.loc[df1.partlabel==ipart, 'partnumber'] =int(ii)
df2 = pd.merge(df1,df_vid, on='video', how='inner')

# rescale all values
df2 = rescale_values(df2)

# add imageid and id
imageid_list = []; id_list = [];
for i in range(len(df2)):
    imageid_list.append(int('1%06d%06d' % (df2.loc[i,'video'], df2.loc[i,'t'])))
    id_list.append(int('1%06d%06d%02d' % (df2.loc[i,'video'], df2.loc[i,'t'], df2.loc[i,'person'])))
df2['imageid'] = imageid_list
df2['id'] = id_list

image_folders = sorted(glob.glob(imagepath))

# remove videos with 2 people
personOver1 = df2.groupby('video').sum()['person'].reset_index()
videosWithPeople = np.asarray(personOver1[personOver1.person>0].video)
df3 = df2[~np.in1d(df2.video,videosWithPeople)]

# take every nth frame
n = 4
df3.tmod = df3.t%n
df3 = df3[(df3.tmod==0)]

# remove head label
df_dlc = df3.loc[df3.partlabel!='head']

dlc_out = df_dlc.groupby('imageid',group_keys=False).apply(lambda x: df_DLC_format(x, zuser)) 

dlc_out.to_csv(os.path.join(csvpath,'CollectedData_'+zuser+'.csv'))
dlc_out.to_hdf(os.path.join(csvpath,'CollectedData_'+zuser+'.h5'), 'df_with_missing',format = 'table', mode='w')

# resize images in dlc df and save to dlc folder
new_max = 640

image_folders = [imagepath[:-1]+'_'+str(i).zfill(6) for i in np.unique(df3['video'])]

out_folder = ['image_DLC']

if 1-os.path.isdir(outputimagepath):
    os.mkdir(outputimagepath)
for ifolder in out_folder:
    new_image_path = os.path.join(outputimagepath,ifolder)
    if 1-os.path.isdir(new_image_path):
        os.mkdir(new_image_path)

for i, ifolder in enumerate(image_folders):
    vidnumber = int(os.path.basename(ifolder)[1:])
    ts = df3[df3.video==vidnumber].t.unique()
    print(ifolder)
    print(vidnumber)
    print(ts)
    x = [ifolder+'/'+str(it)+'.jpg' for it in ts]
    df_image = pd.DataFrame()
    df_image['images'] = pd.Series(x)
    df_image['image_number'] = pd.Series(ts)
    image_files = df_image.sort_values('image_number').images.tolist()
    
    for j, iimage in enumerate(image_files):
        I = cv2.imread(iimage)
        rows = len(I[0]); cols = len(I); 
        max_image = np.max([rows,cols])
        new_image_name = '1%06d%06d.jpg' % (int(os.path.basename(ifolder)[1:]), int(os.path.basename(iimage)[:-4]))
        resized_I = cv2.resize(I, (int(rows/max_image*new_max), int(cols/max_image*new_max)))
        cv2.imwrite(os.path.join(new_image_path, new_image_name),resized_I)
