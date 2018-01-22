Team 21

About:-
This project is aimed at Smart City solution to detect and  prevent various diseases/health hazards. We aim for various city sewers for this data. The collected data is then used by ML algorithms to predict the results. The final results are then sent to the VR for easy tracking of the results in real-time.

Idle Working:-
Here we get images from the microscope which are sent to the central server (for the prediction of results by ML algorithms) via a Raspberry Pi 3. These output images (by ML algorithm) are then sent to V.R for real time user-experience.

Folders:-
Remote Node :- This folder has been deployed with emulated microscope.  
AnalysisMachine :- This folder is connected to the cloud(Microsoft Azure) . AnalysisMachine does image recognition using ‘Bag of Words’ and ‘SVM’. Dataset was for Marburg virus was taken from www.image-net.org
VR :- This folder is related to VR. This app is made in Unity 3D using MapBox APIs and VR SDK.

Libraries used:-
Azure SDK, Android SDK, Unity 3D.
Python:- paramiko, opencv, sklearn
Windows:- Zeiss Labscope , Bitvise SSH server (These 2 in total is emulated microscope.)
