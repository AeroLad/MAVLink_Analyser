import matplotlib
from matplotlib import pyplot as plt
import math
from matplotlib.widgets import Slider



fig = plt.figure()
ax = plt.gca()
plt.subplots_adjust(bottom=0.25)

obj_height  = 126.0 #mm
obj_width   = 224.0 #mm

l1_x = 10.0 #mm
l1_y = 150.0 #mm
l1_f = 220.0 #mm

l2_x = 270.0 #mm
l2_y = 150.0 #mm
l2_f = 260.0 #mm

ax_l1_f = plt.axes([0.1, 0.15, 0.35, 0.02])
sl_l1_f = Slider(ax_l1_f,'L1_F', 1.0,250.0,valinit=l1_f,valstep=1.0)

ax_l2_f = plt.axes([0.1, 0.1, 0.35, 0.02])
sl_l2_f = Slider(ax_l2_f,'L2_F', 1.0,400.0,valinit=l2_f,valstep=1.0)

ax_l1_x = plt.axes([0.1, 0.05, 0.35, 0.02])
sl_l1_x = Slider(ax_l1_x,'L1_x', 1.0,20.0,valinit=l1_x,valstep=1.0)

ax_l2_x = plt.axes([0.1, 0.00, 0.35, 0.02])
sl_l2_x = Slider(ax_l2_x,'L2_x', 1.0,500.0,valinit=l2_x,valstep=0.5)

ax_l1_y = plt.axes([0.55, 0.15, 0.3, 0.02])
sl_l1_y = Slider(ax_l1_y,'L1_y', 1.0,200.0,valinit=l1_y,valstep=1.0)

ax_l2_y = plt.axes([0.55, 0.1, 0.3, 0.02])
sl_l2_y = Slider(ax_l2_y,'L2_y', 1.0,200.0,valinit=l2_y,valstep=1.0)

def plot(l1_x,l1_y,l1_f,l2_x,l2_y,l2_f):
    do_1 = l1_x
    di_1 = (l1_f*do_1) / (do_1-l1_f)
    mag_1 = -1.0 * di_1 / do_1

    i1_height = obj_height * mag_1
    i1_width = obj_width * mag_1

    i1_x = l1_x + di_1

    do_2 = l2_x - i1_x
    di_2 = (l2_f*do_2) / (do_2-l2_f)

    mag_2 = -1.0 * di_2 / do_2

    i1_viewable_height = min([i1_height,l1_y,l2_y])
    i1_viewable_width = min(i1_width,obj_width)

    i2_height = mag_2 * i1_viewable_height
    i2_width = mag_2 * i1_viewable_width
    i2_x = l2_x + di_2

    #print("%.2f:\t%.2f,%.2f" %(i2_x,abs(i2_width*0.0393701),abs(i2_height*0.0393701)))

    #Object
    ax.plot([0,0],[-obj_height/2.0,obj_height/2.0], label="Object")

    ax.plot([l1_x,l1_x],[-l1_y/2.0,l1_y/2.0],label = "L1")
    ax.scatter(l1_x+l1_f,0,s=5)


    ax.plot([l2_x,l2_x], [-l2_y/2.0,l2_y/2.0], label="L2")
    ax.scatter(l2_x+l2_f,0,s=5)
    ax.scatter(l2_x-l2_f,0,s=5)


    #ax.add_artist(plt.Circle((l1_f+l1_x,0),0.5,color='b'))
    ax.plot([i1_x,i1_x],[-i1_height/2.0,i1_height/2.0],label="i1")
    ax.plot([i2_x,i2_x], [-i2_height/2.0,i2_height/2.0],label="i2",color='b')

    # Image Trace
    ax.plot([i1_x,l2_x], [i1_viewable_height/2.0,i1_viewable_height/2.0],color='b')
    ax.plot([i1_x,l2_x], [-i1_viewable_height/2.0,-i1_viewable_height/2.0],color='b')
    m = (0-i1_viewable_height/2.0)/(l2_f)
    c = i1_viewable_height/2.0-m*l2_x
    y = m*i2_x+c

    ax.plot([l2_x,i2_x],[i1_viewable_height/2.0,y],color='b')
    ax.plot([l2_x,i2_x],[-i1_viewable_height/2.0,-y],color='b')

    # Backlight Trace
    y1 = obj_height/2.0
    m = (0-y1)/(l1_f)
    c = y1-m*l1_x
    y = m*l2_x+c
    ax.plot([l1_x,l2_x],[y1,y],color='black')
    ax.plot([l1_x,l2_x],[-y1,-y],color='black')
    incident_angle = math.atan(m)
    refraction_theta = math.atan(abs(y1)/l2_f)
    exit_angle = incident_angle + refraction_theta

    y1 = y
    m = exit_angle
    c = y1-m*l2_x
    y = m*i2_x+c
    ax.plot([l2_x,i2_x],[y1,y],color='black')
    ax.plot([l2_x,i2_x],[-y1,-y],color='black')

    ax.legend()

plot(l1_x,l1_y,l1_f,l2_x,l2_y,l2_f)

def update(val):
    l1_f = sl_l1_f.val
    l1_x = sl_l1_x.val
    l2_f = sl_l2_f.val
    l2_x = sl_l2_x.val
    l1_y = sl_l1_y.val
    l2_y = sl_l2_y.val
    ax.clear()
    plot(l1_x,l1_y,l1_f,l2_x,l2_y,l2_f)
    #fig.canvas.draw_idle()

sl_l1_f.on_changed(update)
sl_l2_f.on_changed(update)
sl_l1_x.on_changed(update)
sl_l2_x.on_changed(update)
sl_l1_y.on_changed(update)
sl_l2_y.on_changed(update)

plt.show()
