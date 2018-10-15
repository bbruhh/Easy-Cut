# Running Easy-Cut on Google Colab

While using Google Colab, you will not need to pre-install anything. The whole method can easily run on the Colab Notebook. The first step is to have the data. Our lab used the [Vatic Annotation tool](https://github.com/cvondrick/vatic), to create a dataset. The Vatic Annotaion Tool breaks the video frame by frame and you can easily annotate the body parts you require and can download the frames and keypoints as XML files.

## Data Processing

This part is done on our local systems, it is used to create the files required to use DeepLabCut with ease. This is how your file system should be- 

```
data_processor.py
data
|_ image
|  |_ <im-1-folder>
|  |_ ...
|  |_ <im-N-folder>
|      |_ <im-N-name>.jpg
|      |_ ...
|      |_ <im-N-name>.jpg
|
|_ xml
   |_ labeller_1
       |_<im-1-folder_xml>
       |_ ...
       |_<im-N-folder_xml>

```

Basically `<im-N-folder>` and it's corresponding XML file should have the same name. 

We then run the Data Processor script. 

`python3 data_processor.py`

This creates new 2 new folders and the file system looks like the following. 

```
data_processor.py
data
|_ image
|  |_ <im-1-folder>
|  |_ ...
|  |_ <im-N-folder>
|      |_ <im-N-name>.jpg
|      |_ ...
|      |_ <im-N-name>.jpg
|
|_ xml
|  |_ labeller_1
|      |_<im-1-folder_xml>
|      |_ ...
|      |_<im-N-folder_xml>
|_image_NN_input
|  |_image_DLC
|     |_<img1>.jpg (in DLC format)
|     |_.... (in DLC format)
|     |_<imgN>.jpg (in DLC format)
|_labels_NN_input
|  |_CollectedData_labeller_1.csv
|  |_CollectedData_labeller_1.h5
|
```

Now, you can upload the `image_NN_input` folder and the `labels_NN_input` folder to your personal drive. This is the data you will be using to train your model. 

## Google Colab Framework




