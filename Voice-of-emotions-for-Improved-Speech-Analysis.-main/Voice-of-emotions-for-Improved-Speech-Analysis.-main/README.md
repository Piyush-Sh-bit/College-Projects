# Voice-of-emotions-for-Improved-Speech-Analysis.
### Introduction
Speech emotion recognition aims to identify the emotional state of a speaker based on their speech signal. Deep learning models, such as Convolutional Neural Networks (CNNs) and Recurrent Neural Networks (RNNs), have demonstrated success in this task. However, the performance of individual models can be limited. 

This study presents a fusion approach that combines the outputs of CNNs and RNNs as features for a Support Vector Machine (SVM) classifier. Our approach is evaluated on a benchmark speech emotion recognition dataset and compared with individual models. The results show that our fusion approach outperforms the individual models and highlights the benefits of combining multiple models for improved speech emotion recognition.

The following sections provide a detailed description of our approach and experimental results. Our findings contribute to the ongoing effort to enhance the performance of speech emotion recognition systems.

### Task Performed
● Implemented by using the CNN and RNN model.

● Compare the accuracy of the CNN and RNN models on the dataset to determine which model performs better.

● The SVM ensemble will use the predictions of the CNN and RNN models as inputs to make a prediction on the emotion of each sample and compare the ensemble result with the individual models.


### Methodology
1.Data Collection: Obtain a diverse dataset of speech and song data from the“https://zenodo.org/record/1188976#.Xk2zcS2ZP_U.”Pre-process the data to extract relevant features such as Mel-Frequency Cepstral Coefficients (MFCCs) and pitch values.

2.Data Labelling: Label each sample in the dataset with an emotion label (e.g., happy, sad, angry, etc.). This will be used as the target variable for the models.

3.CNN Model: Train a Convolutional Neural Network (CNN) on the pre-processed data. This model will be used to recognize emotions in speech and song by learning the relationships between the different features and the corresponding emotions. 

4.RNN Model: Train a Recurrent Neural Network (RNN) on the pre-processed data. This model will be used to recognize emotions in speech and song by considering the sequential nature of speech and song data. 

5.Model Comparison: Compare the accuracy of the CNN and RNN models on the dataset to determine which model performs better.

6.SVM Ensemble: Combine the outputs of the CNN and RNN models using Support Vector Machines (SVM). The SVM will use the predictions of the CNN and RNN models as inputs to make a final prediction on the emotion of each sample.

7.Evaluation: Evaluate the performance of the SVM ensemble by comparing its accuracy with the accuracy of the CNN and RNN models.

8.Conclusion: Summarize the results of the project, highlighting the strengths and limitations of each model, and provide recommendations for future work in the field of speech emotion recognition.
