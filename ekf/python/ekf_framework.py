from math import *
import numpy as np
import numpy.linalg as lng
import argparse
from collections import defaultdict
import matplotlib.pyplot as plt

def read_world_data(filename):
    world_dict = defaultdict()
    f = open(filename)
    for line in f:
        line_s  = line.split('\n')
        line_spl  = line_s[0].split(' ')
        world_dict[float(line_spl[0])] = [float(line_spl[1]),float(line_spl[2])]
    return world_dict

def read_sensor_data(filename):
    data_dict = defaultdict()
    id_arr =[]
    range_arr=[]
    bearing_arr=[]
    first_time = True
    timestamp=-1
    f = open(filename)
    for line in f:
        line_s = line.split('\n') # remove the new line character
        line_spl = line_s[0].split(' ') # split the line
        if (line_spl[0]=='ODOMETRY'):
            data_dict[timestamp,'odom'] = {'r1':float(line_spl[1]),'t':float(line_spl[2]),'r2':float(line_spl[3])}
            if (first_time == True):
                first_time= False
            else:
                data_dict[timestamp,'sensor'] = {'id':id_arr,'range':range_arr,'bearing':bearing_arr}
                id_arr=[]
                range_arr = []
                bearing_arr = []
            timestamp = timestamp+1

        if(line_spl[0]=='SENSOR'):
            id_arr.append(line_spl[1])
            range_arr.append(float(line_spl[2]))
            bearing_arr.append(float(line_spl[3]))
    data_dict[timestamp-1,'sensor'] = {'id':id_arr,'range':range_arr,'bearing':bearing_arr}
    return data_dict

def prediction_step(mu, sigma, odometry):
    # TODO Read in the state from the mu vector
    # TODO Read in the odometry i.e r1, t , r2
    # TODO Compute the noise free motion.
    # TODO Computing the Jacobian of G with respect to the state

    # TODO Use the Motion Noise as given in the exercise
    Q = [[0.2, 0,   0],
        [0,   0.2, 0],
        [0,   0,   0.02]]

    # TODO Predict the covariance
    return mu, sigma


def correction_step(mu, sigma, measurements, world_dict):
    # TODO Get the states
    # TODO Read in the ids and ranges  from measurements using dictionary indexing

    # Initialize the Jacobian of h
    H = np.zeros((len(ids),3))

    #Vectorize measurements
    for i in range(len(ids)):
          # TODO
          # For each measurement , compute a row of H
          #H[i,:]=

     # TODO Noise covariance for the measurements
     # TODO Kalman Gain
     # TODO Kalman correction for mean and covariance
    return mu,sigma

## Main loop Starts here
parser = argparse.ArgumentParser()
parser.add_argument('sensor_data', type=str, help='Sensor Data')
parser.add_argument('world_data', type=str, help='World Data')

args = parser.parse_args()

data_dict = read_sensor_data(args.sensor_data)
world_data = read_world_data(args.world_data)

#Initial Belief
mu = np.array([0.0,0.0, 0.0]).T
sigma =np.array([[1.0,0.0 , 0.0],[0.0, 1.0 , 0.0],[0.0, 0.0 , 1.0]])

# Landmark Positions
lx=[]
ly=[]

for i in range (len(world_data)):
    lx.append(world_data[i+1][0])
    ly.append(world_data[i+1][1])

plt.axis([0, 15, 0, 15])
plt.ion()
plt.show()

for t in range(len(data_dict)/2):
    # Perform the prediction step of the EKF
    [mu, sigma] = prediction_step(mu, sigma, data_dict[t,'odom'])
    # Perform the correction step of the EKF
    [mu, sigma] = correction_step(mu, sigma, data_dict[t,'sensor'], world_data)

    x_pos = mu[0]
    y_pos = mu[1]

    ''' Plotting  the state Estimate '''
    plt.plot(x_pos,y_pos,'ro',markersize=10)
    quiver_len = 3.0
    theta_n = mu[2]
    plt.quiver(x_pos, y_pos , quiver_len * np.cos(theta_n), quiver_len * np.sin(theta_n),angles='xy',scale_units='xy')

    plt.plot(lx,ly,'bo',markersize=10)
    plt.axis([-2, 15, 0, 15])
    plt.draw()
    plt.clf()