# Easy-Cut
 
**DeepLabCut: markerless pose estimation of user-defined body parts with deep learning**

_Alexander Mathis, Pranav Mamidanna, Kevin M. Cury, Taiga Abe, Venkatesh N. Murthy, Mackenzie Weygandt Mathis & Matthias Bethge_

[[`DeepLabCut`](http://www.mousemotorlab.org/deeplabcut)] [[`nature neuroscience`](https://www.nature.com/articles/s41593-018-0209-y)] [[`arXiv`](https://arxiv.org/abs/1804.03142)] [[`BibTeX`](#CitingDeepLabCut)]


DeepLabCut is a toolbox for markerless tracking of body parts of animals. We can train the neural network to learn the movements of rats, humans, robots, basically any thing! This repository is DeepLabCut. But, we do intergrate it with Google Colab and add a few more features to make it very easy for everyone to use! Also, we can make full use of the Tesla K80 GPU that Colab offers. 

Below are a few examples of what DeepLabCut has to offer:

---

1. Tracking a fly.

<div align="center">
  <img src="/Examples/MATHIS_2018_fly.gif" />
</div>

<br />

---

2. Tracking a Mouse.

<div align="center">
  <img src="/Examples/MouseLocomotion_warren.gif" />
</div>

<br />

---

3. Tracking a horse.

<div align="center">
  <img src="/Examples/brownhorse.gif" />
</div>

<br />

---

## Understanding DeepLabCut

This project is suitable for anyone who wants to extract the position of different body part of animals performing some kind of a behaviour. The positions can be extracted from images/videos. DeepLabCut trains feature detectors and then trains a deep network to analyze the other videos. 

Following is a small flowchart for how DeepLabCut works: 

**Install --> Extract frames -->  Label training data -->  Train DeeperCut feature detectors -->  Apply your trained network to unlabeled data -->  Extract trajectories for analysis.**


## <a name="CitingDeepLabCut"></a>Citing DeepLabCut

If you use DeepLabCut, please use the following BibTeX entry.

```
  @techreport{mathis2018deeplabcut,
  title={DeepLabCut: markerless pose estimation of user-defined body parts with deep learning},
  author={Mathis, Alexander and Mamidanna, Pranav and Cury, Kevin M and Abe, Taiga and Murthy, Venkatesh N and Mathis, Mackenzie Weygandt and Bethge, Matthias},
  year={2018},
  institution={Nature Publishing Group}
  }
```


## Code contributors:

The entire credit of this repo should go to the following: 

[Alexander Mathis](https://github.com/AlexEMG), [Mackenzie Mathis](https://github.com/MMathisLab), and the DeeperCut authors for the feature detector code. Edits and suggestions by [Jonas Rauber](https://github.com/jonasrauber), [Taiga Abe](https://github.com/cellistigs), [Hao Wu](https://github.com/fullerene12), [Jonny Saunders](https://github.com/sneakers-the-rat), [Richard Warren](https://github.com/rwarren2163) and [Brandon Forys](https://github.com/bf777). The feature detector code is based on Eldar Insafutdinov's TensorFlow implementation of [DeeperCut](https://github.com/eldar/pose-tensorflow).

## References:

    @inproceedings{insafutdinov2017cvpr,
        title = {ArtTrack: Articulated Multi-person Tracking in the Wild},
        author = {Eldar Insafutdinov and Mykhaylo Andriluka and Leonid Pishchulin and Siyu Tang and Evgeny Levinkov and Bjoern Andres and Bernt Schiele},
        booktitle = {CVPR'17},
        url = {http://arxiv.org/abs/1612.01465}
    }
    
    @article{insafutdinov2016eccv,
        title = {DeeperCut: A Deeper, Stronger, and Faster Multi-Person Pose Estimation Model},
        author = {Eldar Insafutdinov and Leonid Pishchulin and Bjoern Andres and Mykhaylo Andriluka and Bernt Schiele},
        booktitle = {ECCV'16},
        url = {http://arxiv.org/abs/1605.03170}
    }
    
    @article{Mathisetal2018,
      title={DeepLabCut: markerless pose estimation of user-defined body parts with deep learning},
      author = {Alexander Mathis and Pranav Mamidanna and Kevin M. Cury and Taiga Abe  and Venkatesh N. Murthy and Mackenzie W. Mathis and Matthias Bethge},
       journal={Nature Neuroscience},
        year={2018},
        url={https://www.nature.com/articles/s41593-018-0209-y}
}


