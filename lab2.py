#!/usr/bin/env python
import rospy
import math
import threading
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped


xg = None
yg = None
zg = None
xgo = None
ygo = None
zgo = None
wgo = None
xp = None
yp = None
zp = None  
thep = None
thego = None

velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


def posecallback(data):
    #rospy.loginfo(data)
    global xp, yp, zp, thep
    xp = data.linear.x
    yp = data.linear.y
    zp = data.linear.z
    thep = data.angular.z
    if thep >=  math.pi and thep <= 2* math.pi :
        thep = thep -2 *math.pi
    #print 'thep in callback', thep


def goalcallback(data):
    global xg, yg, zg, xgo, ygo, zgo, wgo, thego
    xg = data.pose.position.x
    yg = data.pose.position.y
    zg = data.pose.position.z
    xgo = data.pose.orientation.x
    ygo = data.pose.orientation.y
    zgo = data.pose.orientation.z
    wgo = data.pose.orientation.w
    thego = math.atan2(2*(wgo*zgo+xgo*ygo), 1-2*(zgo**2+ygo**2))
    #print 'xg in callback', xg

def publisher_thread():
    while True:
        if xg != None:
            print 'xp in thread', xp
            vel_msg = Twist()
            k1= 0.6
            k2= 5
            k3= -3.5
            rho= math.sqrt((xg-xp)**2+(yg-yp)**2)
            alpha= -thep + math.atan2((yg-yp),(xg-xp))
            beta= thego - math.atan2((yg-yp),(xg-xp))
            print 'rho in if', rho
            v = (k1*rho)
            print ' v=', v
            w = (k2*alpha+k3*beta)
            vel_msg.linear.x = v
            vel_msg.linear.y = 0.0
            vel_msg.linear.z = 0.0
            vel_msg.angular.x = 0.0
            vel_msg.angular.y = 0.0
            vel_msg.angular.z = w
            velocity_publisher.publish(vel_msg)
    
            if rho < 0.003:
                vel_msg.linear.x = 0.0
                vel_msg.linear.y = 0.0
                vel_msg.linear.z = 0.0
                vel_msg.angular.x = 0.0
                vel_msg.angular.y = 0.0
                vel_msg.angular.z = 0.0
                velocity_publisher.publish(vel_msg)
                print 'yp', yp
                print 'yg', yg
                print ' xp', xp
                print ' xg', xg
                print 'thego', thego
                print ' thep', thep
                return



def lab2s():
    rospy.init_node('lab2s', anonymous=True)
    rospy.Subscriber('robot_pose', Twist, posecallback)
    rospy.Subscriber('/move_base_simple/goal', PoseStamped, goalcallback)
    worker = threading.Thread(target=publisher_thread)
    worker.start()    
    rospy.spin()

if __name__ == '__main__':
    lab2s()
