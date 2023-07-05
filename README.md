# 2023-06-02-Robot-Reach-Calculator
Give joint and link configuration of a robot, and estimate reach. Meant to help design DIY robots.

This is a tool meant to help design DIY robots

# Definitions
World = origin of the system of reference
Joint = a motor that rotates the next link around an axis
Link = structure that connects two joints

Example: Inverse Double Pendulum
World
Link World - Joint 1 has zero length
Joint 1 rotates around RZ
Link Joint 1 - Joint 2 has fixed length L12
Joint 2 rotates around RZ, the system is two dimensional. Note that when this joint is fixed at 0°, the next link isfixed in respect to Joint 2, meaning it will rotate with Joint 1
Link Joint 2 - End Effector has fixed length L2E
End Effector

# Parameters
Number of joints
Configuration of the joints
Length of the link

# Inputs
Joint angles

# Output
Position and rotation of the end effector relative to World

# Forward Kinematic
Given the geometry, I have a forward solution that links the angles of the joints to the position of the end effector

# Forward Sensitivity
In a given configuration, each end effector axis has a given sensitivity to changes in joint angle [°/mm]
This informs about gear ratio as well

# Inverse Kinematic
Given a desired end position of the end effector, a number of joint angles may exist that achieve that position

# Inverse Sensitivity
In any given configuration, each joint will have a given sensitivity to changes in end effector position
The inverse sensitivity allows to estimate the load at each joint knowing the load at the end effector

# Reach Map
Draw each point that can be reached.
To give colors to the reach:
A point is easy to reach if the angles are close to the default angles
A point is hard to reach if the angles are far from the default angles
Another idea to give color to the reach is to use a bin system.
Scan joints at a given angular resolution, and show up where they end up.
Regions with lots of dots are easy, regions with few dots are hard

# Sensitivity Map
Map each point depending on the overall sensitivity across joints
Singular points are going to have very high sensitivity and be hard to reach

# Example: Inverse Pendulum
I have just one joint, that is in the World (0,0). There is an hidden zero length link between World and J1
J1 leads to link L1E, that rotates around one axis (RZ)
The end of link L1E is the special joint E, the end effector
Because J1 rotates around RZ in the origin, and the link has fixed length, the End Effector will move in a circle in the XY plane

Dimensions: 2 (X,Y)
Joints: 1
Links: 2

W = (0,0)
LW1 = (0,0)
J1 = (0,0,1) (RZ)
L1E = L1E
E = End Effector

Null Parameters:
- W_X: origin
- W_Y: origin
- PW: phase of link between World and Joint 1
- LW1: Length of link between World and Joint 1

Parameters (2):
- L1E: length of link Joint 1 to End Effector
- P1: Offset angle of Joint 1
Inputs (1):
- T1: angle of joint 1
Outputs (3):
- E(X,Y,T): position of the end effector XY and the direction it's pointing to

Forward Kinematic:
- E_X = L1E*cos(P1 +T1)
- E_Y = L1E*sin(P1 +T1)
- E_T = P1 +T1

Forward Sensitivity:
- E_X(T1) = -L1E*sin(P1 +T1)
- E_Y(T1) = L1E*cos(P1 +T1)
- E_T(T1) = 1

Inverse Kinematic:

# Inverse Domain
The core function for the inverse is the arcsin, which has domain -1,1
It's what introduces boundaries of the validity of the inverse equation
Distance from the boundaries tells how far it's from feasibility
0 inside, above 0 is either below -1 or above +1 in absolute value, telling how hard outside the limits the position is
it's probably the best way to trace the feasibility of a position


