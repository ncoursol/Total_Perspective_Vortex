# Total_Perspective_Vortex
## Introduction
This subject aims to create a brain computer interface based on electroencephalographic
data (EEG data) with the help of machine learning algorithms. Using a subject’s EEG
reading, you’ll have to infer what he or she is thinking about or doing - (motion) A or B
in a t0 to tn timeframe.

42 subject: https://cdn.intra.42.fr/pdf/pdf/84885/en.subject.pdf

The subject focuses on implementing the algorithm of dimensionality reduction, to
further transform filtered data before classification. This algorithm will have to be integrated within sklearn so it be able to use sklearn tools for classification and score
validation.
## Datas
The recordings are provides from [PhysioNet - EEG Motor Movement/Imagery Dataset](https://physionet.org/content/eegmmidb/1.0.0/).

The PhysioNet Resource’s original and ongoing missions were to conduct and catalyze for biomedical research and education, in part by offering free access to large collections of physiological and clinical data and related open-source software.
- ### Abstract
  This data set consists of over 1500 one- and two-minute EEG recordings, obtained from 109 volunteers, as described below.
- ### Experimental Protocol
  Subjects performed different motor/imagery tasks while 64-channel EEG were recorded using the BCI2000 system. Each subject performed 14 experimental runs: two one-minute baseline runs (one with eyes open, one with eyes closed), and three two-minute runs of each of the four following tasks:
  
  1. A target appears on either the left or the right side of the screen. The subject opens and closes the corresponding fist until the target disappears. Then the subject relaxes.
  1. A target appears on either the left or the right side of the screen. The subject imagines opening and closing the corresponding fist until the target disappears. Then the subject relaxes.
  1. A target appears on either the top or the bottom of the screen. The subject opens and closes either both fists (if the target is on top) or both feet (if the target is on the bottom) until the target disappears. Then the subject relaxes.
  1. A target appears on either the top or the bottom of the screen. The subject imagines opening and closing either both fists (if the target is on top) or both feet (if the target is on the bottom) until the target disappears. Then the subject relaxes.
