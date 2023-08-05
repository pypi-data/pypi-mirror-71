# -*- coding: utf-8 -*-

"""
Copyright (C) 2019 Event-driven Perception for Robotics
Authors: Sim Bamford
This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with 
this program. If not, see <https://www.gnu.org/licenses/>.

Intended as part of importRosbag.

The importTopic function receives a list of messages and returns
a dict with one field for each data field in the message, where the field
will contain an appropriate iterable to contain the interpretted contents of each message.
In some cases, static info is repeated in each message; in which case a field may not contain an iterable. 

This function imports the ros message type defined at:    
http://docs.ros.org/melodic/api/geometry_msgs/html/msg/PoseStamped.html

The result is a ts plus a 7-column np array of np.float64,
where the cols are x, y, z, q-w, q-x, q-y, q-z, (i.e. quaternion orientation)

NOTE: QUATERNION ORDER GETS MODIFIED from xyzw to wxyz
"""

#%%

from tqdm import tqdm
import numpy as np

from .common import unpackRosString, unpackRosTimestamp, unpackRosFloat64Array

def importTopic(msgs, **kwargs):
    #if 'Stamped' not in kwargs.get('messageType', 'Stamped'):
    #    return interpretMsgsAsPose6qAlt(msgs, **kwargs)
    sizeOfArray = 1024
    tsAll = np.zeros((sizeOfArray), dtype=np.float64)
    poseAll = np.zeros((sizeOfArray, 7), dtype=np.float64)
    for idx, msg in enumerate(tqdm(msgs, position=0, leave=True)):
        if sizeOfArray <= idx:
            tsAll = np.append(tsAll, np.zeros((sizeOfArray), dtype=np.float64))
            poseAll = np.concatenate((poseAll, np.zeros((sizeOfArray, 7), dtype=np.float64)))
            sizeOfArray *= 2
        # TODO: maybe implement kwargs['useRosMsgTimestamps']
        data = msg['data']
        #seq = unpack('=L', data[0:4])[0]
        tsAll[idx], ptr = unpackRosTimestamp(data, 4)
        frame_id, ptr = unpackRosString(data, ptr)
        poseAll[idx, :], _ = unpackRosFloat64Array(data, 7, ptr)
    # Crop arrays to number of events
    numEvents = idx + 1
    tsAll = tsAll[:numEvents]
    poseAll = poseAll[:numEvents]
    point = poseAll[:, 0:3]
    rotation = poseAll[:, [6, 3, 4, 5]] # Switch quaternion form from xyzw to wxyz
    outDict = {
        'ts': tsAll,
        'point': point,
        'rotation': rotation}
    return outDict
