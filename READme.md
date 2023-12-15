## Pose Estimation

### Exercise Count tracker and Form Validator

*Run the following command.*

`git clone [repo-name].git`

`pip install -r requirements.txt`

*this installs the required libraries (tensorflow for macos)*

To test this project, replace the video footage path in the `path` placeholder in the `pose_enhanced_trainer.py` script. Keep the video such that the side view of the person is visible and accordingly as per view of arm, find the angle for left or right arm.

### How to run the project?

Navigate into the project directory after cloning the project and then run,
`python3 pose_enhanced_trainer.py`

### Methodology and Working Explained: 

This is an implementation of computer vision technique called Pose Estimation and landmark tracking to track certain landmarks of interest and leverage the use of Pose Estimation library Mediapipe to count the proper bicep curls.

To implement this methodlogy, first Pose module is made which contains the basic functionality of drawing the Pose landmark coordinates and finding the position of that particular landmark.

The `findPose()` function draws the landmark coordinates upon the image frame using mediapipe library- draw_landmarks. 

The `findPosition()` function is used to store the list of all the landmarks having `[landmark_id, x_coordinate, y_coordinate]`.

Then we have `findAngle()` function to calculate the angle between 3 landmark points, using the maths formula `to_degrees[atan2(p3_y-p2_y, p3_x-p2_x) - atan2(p1_y-p2_y,p1_x-p2_x)]` where p1, p2 and p3 are the points of interest. The angle being found around p2 point. `_x` and `_y` being the x and the y coordinates respectively.

The angle between these 3 points of interest is found and negative angle is then converted into the rangle of (0,360). Then optionally as per visual preference to separate the landmarks of interest from all landmarks, additional elements, like drawing concentric circles for specific landmarks and then joining them with a line is done.

For now, this implementation was tested on a stock footage of a person doing bicep curls and only the Right arm was taken into consideration, being prominently visible in the frame. Then the respective landmarks of the right arm were passed as the points (p1,p2,p3) which cooresponds to the landmark_id in the list containing all the landmark id and the coordinates. Then the angle is calculated for every frame.

After getting the angle, the minimum and the maximum angle range can be saved for the next part of the implementation. *It is important to know the possible minimum and maximum values of angles reached.*

With our minimum and maximum angle range values, the angle range is then converted into a range of `(0,100)` using the numpy `interp` function. This is done to give a better intuitive understanding of range variation on scale of (0,100) when the angle is changed upon doing bicep curls. 

Then for counting curls, the logic used is to assign a direction for up and down direction while doing a curl. When the percentage (the value interpolated with the angle range) is 100, then it means that the person is going up, therefore half of curl is incremented and the direction is changed to down. Afterwards, when the percentage is 0, then it means that the person is doing a downward curl and again the curl count is incremented by 0.5 and direction changed to up. Finally when the person makes a movement in both upwards and downwards direction, then and then only a full curl is counted.

Finally, for visual depiction to aid with intuition of curl motion, the range of angle is interpolated with a range value of a rectangular bar to be filled as per variations in angle.
*This part is completely optional and just for my intuition of motion and visual appeasement.*

Similarly, this methodology can be implemented for any body part exercise that revolves around doing the exercise with a precision of angle/ acceptable angle range, to count proper valid repititions of that exercise. 

**This was tested on Macbook M1 Air CPU with a decent FPS**
