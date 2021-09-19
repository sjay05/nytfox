# NytFox 

> A Real Time Car Theft Monitoring System.
 
![Image](https://i.ibb.co/y0PzzPh/Screen-Shot-2021-09-19-at-12-27-10-AM.png)

## Problem | Inspiraton

Vehicle theft is a serious threat to public safety and could cost up to billions of dollars on a yearly basis. In Canada, a car is stolen every 6 minutes according to the Insurance Bureau. Ontario, as it stands, was ranked first in Canada in 2020 with about 24000 car thefts.

As a vehicle owner, to become aware of your property being stolen is a matter of when you check your driveway. This could take usually hours/days on average. When owners do realize, recorded footage could only prove that their car was stolen, and the realization of their car being unable to be retrieved starts to set in.

## Solution

Our solution, using any surveillance camera (in this case, Raspberry Pi) builds upon the current circumstances. Using computer vision libraries, the camera can now detect theft occuring in real-time and send notifications to the owner of the vehicle. 

To build upon this solution, notifications can be *forwarded* to police as soon as you receive them, significantly increasing the chances of your vehicle being retrieved. In the future, this could be integrated with CCTV cameras on the road to detect the location of your car.

To make sure that the camera doesn't send notifications when you're accessing your car, using face_recognition the Raspberry Pi now knows that this situation is under safe conditions. If at all the owner believes an alert received is a false-alarm he is able to dismiss the alert.

## Built With

* Raspberry Pi and PiCamera
* OpenCV and MobileNet Object Detection
* Face-Recognition Libraries
* Flask and Flask-SocketIO
* ImageZMQ
* HTML/CSS/JS

## Notes 

This project is a submission to Hack the North 2021 on Septermber 19th, 2021.

Team: Sanjay Seenivasan

## Pictures

![Design](https://i.ibb.co/HxnvXLV/Screen-Shot-2021-09-19-at-12-32-13-AM.png)

![Alert](https://i.ibb.co/S62FmRF/Screen-Shot-2021-09-19-at-12-48-28-AM.png)