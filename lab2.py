#!/usr/bin/env python
import rospy
import math
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped

xg = None
yg = None
zg = None
xgo = None
ygo = None
zgo = None
wgo = None
thego = None

xp = 0.0
yp = 0.0
zp = 0.0  
thep = 0.0

vx = 0.0
vy = 0.0
vz = 0.0
wx = 0.0
wy = 0.0
wz = 0.0

def posecallback(data):
    #rospy.loginfo(data)
    global xp, yp, zp, thep
    xp = data.linear.x
    yp = data.linear.y
    zp = data.linear.z
    thep = data.angular.z
    #print 'xp in callback', xp

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
    print 'xg', xg
    print 'yg', yg
    print 'zg', zg
    print 'xgo', xgo
    print 'ygo', ygo
    print 'zgo', zgo
    print 'wgo', wgo
    print 'thego', thego

def dummy_goal():
    global xg, yg, zg, xgo, ygo, zgo, wgo, thego
    xg = 0.5
    yg = 0.9
    zg = 0.0
    xgo = 0.0
    ygo = 0.0
    zgo = 1.0
    wgo = 0.0
    thego = math.atan2(2*(wgo*zgo+xgo*ygo), 1-2*(zgo**2+ygo**2))
    # print 'xg', xg
    # print 'yg', yg
    # print 'zg', zg
    # print 'xgo', xgo
    # print 'ygo', ygo
    # print 'zgo', zgo
    # print 'wgo', wgo
    # print 'thego', thego
    print 'goal defined'

def velcallback(data):
    #rospy.loginfo(data)
    global vx,vy,vz,wx,wy,wz
    vx = data.linear.x
    vy = data.linear.y
    vz = data.linear.z

    wx = data.angular.x
    wy = data.angular.y
    wz = data.angular.z
    #print 'xp in callback', xp

def lab2s():
    rospy.init_node('lab2s', anonymous=True)
    rospy.Subscriber('robot_pose', Twist, posecallback)
    print 'xp', xp, 'yp', yp, 'thep', thep
    rospy.Subscriber('/move_base_simple/goal', PoseStamped, goalcallback)
    # dummy_goal()
    velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(1)

    k1= 1
    k2= 2
    k3= -0.8
    vel_msg = Twist()
    flag = 1
    count=0
    # rospy.Subscriber('robot_pose', Twist, posecallback)
    # print 'xp', xp, 'yp', yp, 'thep', thep

    while flag:
        if xg != None:
            rospy.Subscriber('robot_pose', Twist, posecallback)
            print 'xp', xp, 'yp', yp, 'thep', thep
            # flag=0

            rho= math.sqrt((xg-xp)**2+(yg-yp)**2)
            alpha= -thep + math.atan2((yg-yp),(xg-xp))
            beta= thego - math.atan2((yg-yp),(xg-xp))
            print 'rho', rho, 'alpha', alpha, 'beta', beta
            # print 'rho in if', rho 
            v = (k1*rho)
            w = (k2*alpha+k3*beta)
            print 'v', v, 'w',w
            # drho=(-k1* rho* math.cos(alpha)) 
            # dalpha=(k1* math.sin(alpha) -k2* alpha -k3* beta)
            # dbeta=(-k1* math.sin(alpha))

            vel_msg.linear.x = v 
            vel_msg.linear.y = 0.0
            vel_msg.linear.z = 0.0
            vel_msg.angular.x = 0.0
            vel_msg.angular.y = 0.0
            vel_msg.angular.z = w
            velocity_publisher.publish(vel_msg)
            print(vel_msg)

            rospy.Subscriber('/cmd_vel', Twist, velcallback)
            print 'vx',vx, 'vy',vy, 'vz',vz, 'wx',wx, 'wy',wy, 'wz',wz
            # for i in range(10):
            #     rospy.Subscriber('robot_pose', Twist, posecallback)
            #     print 'xp', xp, 'yp', yp, 'thep', thep
            # rho = rho +drho
            # alpha = alpha + dalpha
            # beta = beta + dbeta
            count+=1
            if count > 10:
                vel_msg.linear.x = 0.0
                vel_msg.linear.y = 0.0
                vel_msg.linear.z = 0.0
                vel_msg.angular.x = 0.0
                vel_msg.angular.y = 0.0
                vel_msg.angular.z = 0.0
                velocity_publisher.publish(vel_msg)
                flag = 0

            if rho < 0.005:
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
    rate.sleep()

if __name__ == '__main__':
    lab2s()
