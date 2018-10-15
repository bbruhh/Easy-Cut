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

