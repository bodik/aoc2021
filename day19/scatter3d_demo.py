
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
#import numpy as np
#
#
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#
#ax.scatter([500], [0], [-500], c='b')
#ax.scatter([-500], [1000], [-1500], c='r')
#ax.scatter([1501], [0], [-500], c='r')
#
#ax.set_xlabel('X Label')
#ax.set_ylabel('Y Label')
#ax.set_zlabel('Z Label')


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

def animate(i):
    return ax.scatter(i, 0)

ani = animation.FuncAnimation(fig, animate, interval=20, blit=True, save_count=50)
# To save the animation, use e.g.
# ani.save("movie.mp4")


#plt.savefig("mygraph.png")
plt.show()
