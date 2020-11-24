# Geodynamics and Data Mining for Earthquake Hazards

### Introduction
A key piece of data in assessing seismic hazard for a region is the knowledge of
prior activity – the magnitude, frequency, as well as damage patterns of likely
earthquakes. Prior to the digital error of modern seismology and the
pervasiveness of social media, knowledge of patterns of damage came from
historical accounts, or more recently in the 1900’s, after event surveys. These
accounts are important in calibrating current strong ground motion numerical
models for large earthquakes that could cause widespread destruction. See the
project proposal [here](https://docs.google.com/document/d/1Jy4wVc0VI-S1xsQBLGDiCbZen5ulVX0YXdsRfj8YVVM/edit).

### Problem Statement
The data collected through felt reports provides insight into the effects of earthquakes overtime but is hard to use in research due to how it is currently formatted in various scanned forms. The felt reports date back for many more years than digital or instrumental records allowing the timescale of data used in research to be lengthened. Various people surveyed with felt reports will also have different mannerisms and qualitative measurements used in their language. Some respondents provide extraneous information that will need to be removed to make their response useful. 

### Proposed Solution
The goal of this project is to capture all information for researchers studying
the damage extent of historical earthquake studies. We will scrape data from the postcard images
and convert to text. Then we will process the text felt reports with NLP to try and
extract research usable data from them.

### Data Processing
Due to the complex nature of the postcards, a lot of preprocessing must be done to the image in order to get them into a state from which the machine learning algorithm can parse the text into digital text strings instead. This is due to the fact that the algorithms are extremely sensitive and it's hard enough to create strings from handwritten and printed input without the worry of additional imperfections.

The dataset varies greatly in terms of the content provided. Though most documents follow the same general format, that being the general layout of a C&G5-680 document, some are more random, including some newspaper clippings and other reports. Because of the focus on the postcards, the other content must be detected and removed from the incoming dataset. Once the correct images have been attained, the picture must be straightened. Through the use of Hough lines, it is rather simple to determine whether or not a document is straight. We used Hough lines to evaluate the angle at which the document is tilted in order to straighten the overall document. Scanning the whole document for lines leads to issues as handwriting and vertical lines interfere with the algorithm. Thus, a single line present on all documents must be designated and found every time in order to straighten the image. After straightening the image, various areas of the image containing information were cropped out and sent to their respective cropped image formats. This was done using template matching. C&5-680 forms are all the same, so taking various landmarks from the document, such as section titles, assists in finding the areas in which handwriting is likely to appear. This works for most cases, although there are some in which form outlines are completely ignored and the subject instead decides to write their notes on the right side of the document.

Once template matching was completed, we used our predetermined “cookie cutters” to separate the useful written information into different images for further analysis and text extraction. However, because of the existence of extra inconsistencies, such as marks and lines, further action may be required in order to get individual images into a usable format for OCR. This includes line removal and removal of random spots and scuffs. It is also worth noting that images with circled words, or checkboxes will need to be handled separately and entirely differently than the OCR images, seeming as they are more specific and also allow some degree of leniency when it comes to the actual shape.

### Methodology
To address the handwritten text on the postcards, we have made use of the SimpleHTR Github repository: a handwritten text recognition system trained on the IAM dataset.

Implemented with TensorFlow, we were able to use the pretrained neural network model, with a few modifications to better fit our use cases, to process a subset of the data. The neural network consists of 5 convolutional neural network layers, 2 recurrent neural network layers, and a final Connectionist Temporal Classification layer.

The accuracy of said processing is provided in the results section. Preprocessing in the form of cleaning the handwritten text of lines and other marks, and cropping of images to an acceptable format was required, before making use of said model. Nonetheless, being that the IAM dataset contained handwriting patterns very similar to the handwriting we encountered in the provided postcards dataset, the model proved sufficiently successful in processing the handwritten text. We also intend to make use of word beam search decoding to further improve the results by constraining words to those contained in a dictionary. The processed text will then be stored in a csv file with each recognized word related to its location and relevant category on the postcard. The stored text will then be further processed using NLP models designed for each category, to begin building our final dataset mapping the processed text to numerical and categorical values to describe each earthquake event.

### Image Processing
Our processing starts with pre-sorting in order to remove content that isn’t valuable for our project, as well as to group the images that are in the form of a C&G5-680. We do this processing by using OpenCV’s template recognition, and the possibility of reviewing any form that is not of this layout of information. The images vary slightly in the ppi of the scanner, and in the artifacts in them which means that one pass with a template from a different source only found 174 out of 871 images as being the correct type. Another pass taken with a new template taken from the image dataset in question resulted in 688 additional images being recognized. Of the 29 images still rejected only 2 of them partially contained a C&G580, however both of those images covered the forms header with a newspaper clipping, a problem that also exists in the images that were accepted by one of the two passes of template matching filtering. The template matching approach accepted no image that did not contain the intended header.

Once the C&G5-680 forms are grouped together, we specify approximate bounds for the expected areas of responses to each question and template match for the question prompts and split the images into each question. Before we try to interpret the images, we try to remove any bounds of the boxes and noise from the portion of the image we expect to find a response. Optical character recognition (OCR) is the use of technology to translate handwritten text in digital images of physical documents into code that can be used for data processing. We then parse each question using OCR designed for text using Tesseract and designed for handwriting using SimpleHTR in order to grab necessary information. We compared the results and confidence that we get from the two methods of recognizing character responses. From there on, we can take the different fields of data and export them to CSV.

