# # from OpenGL import *
# # from OpenGL.GL import *
# # from OpenGL.GLUT import *
# # from OpenGL.GLU import *
# # def showScreen():
# # 	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Remove everything from screen (i.e. displays all white)
# # glutInit() # Initialize a glut instance which will allow us to customize our window
# # glutInitDisplayMode(GLUT_RGBA) # Set the display mode to be colored
# # glutInitWindowSize(500, 500)   # Set the width and height of your window
# # glutInitWindowPosition(0, 0)   # Set the position at which this windows should appear
# # wind = glutCreateWindow("OpenGL Coding Practice") # Give your window a title
# # glutDisplayFunc(showScreen)  # Tell OpenGL to call the showScreen method continuously
# # glutIdleFunc(showScreen)     # Draw any graphics or shapes in the showScreen function at all times
# # glutMainLoop()  # Keeps the window created above displaying/running in a loop
# # # showScreen()

# import pygame
# from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# verticies = (
#     (1, -1, -1),
#     (1, 1, -1),
#     (-1, 1, -1),
#     (-1, -1, -1),
#     (1, -1, 1),
#     (1, 1, 1),
#     (-1, -1, 1),
#     (-1, 1, 1)
#     )

# edges = (
#     (0,1),
#     (0,3),
#     (0,4),
#     (2,1),
#     (2,3),
#     (2,7),
#     (6,3),
#     (6,4),
#     (6,7),
#     (5,1),
#     (5,4),
#     (5,7)
#     )
# surfaces = (
#     (0,1,2,3),
#     (3,2,7,6),
#     (6,7,5,4),
#     (4,5,1,0),
#     (1,5,7,2),
#     (4,0,3,6)
#     )
# colors = (
#     (1,0,0),
#     (0,1,0),
#     (0,0,1),
#     (0,1,0),
#     (1,1,1),
#     (0,1,1),
#     (1,0,0),
#     (0,1,0),
#     (0,0,1),
#     (1,0,0),
#     (1,1,1),
#     (0,1,1),
#     )

# def Cube():
#     glBegin(GL_QUADS)
#     for surface in surfaces:
#         x = 0
#         for vertex in surface:
#             x+=1
#             glColor3fv(colors[x])
#             glVertex3fv(verticies[vertex])
#     glEnd()

#     glBegin(GL_LINES)
#     for edge in edges:
#         for vertex in edge:
#             glVertex3fv(verticies[vertex])
#     glEnd()


# def main():
# 	# print("glGetString - GL_VENDOR: ", glGetString(GL_VENDOR))
# 	# print("glGetString - GL_RENDERER: ", glGetString(GL_RENDERER))
# 	# print("glGetString - GL_SHADING_LANGUAGE_VERSION:", glGetString(GL_SHADING_LANGUAGE_VERSION))
# 	# print("glGetString - GL_EXTENSIONS: ", glGetString(GL_EXTENSIONS))
# 	# print("gluGetString - GLU_VERSION: ", gluGetString(GLU_VERSION))
# 	# print("gluGetString - GLU_EXTENSIONS: ", gluGetString(GLU_EXTENSIONS))
# 	pygame.init()
# 	display = (800,600)
# 	pygame.display.set_mode(display, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.OPENGL)

# 	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

# 	glTranslatef(0,0, -10)

# 	glRotatef(25, 2, 1, 0)
# 	while True:
# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT:
# 				pygame.quit()
# 				quit()

# 			if event.type == pygame.KEYDOWN:
# 				if event.key == pygame.K_LEFT:
# 					glTranslatef(-0.5,0,0)
# 				if event.key == pygame.K_RIGHT:
# 					glTranslatef(0.5,0,0)

# 				if event.key == pygame.K_UP:
# 					glTranslatef(0,1,0)
# 				if event.key == pygame.K_DOWN:
# 					glTranslatef(0,-1,0)

# 			if event.type == pygame.MOUSEBUTTONDOWN:
# 				if event.button == 4:
# 					glTranslatef(0,0,1.0)

# 				if event.button == 5:
# 					glTranslatef(0,0,-1.0)

# 		#glRotatef(1, 3, 1, 1)
# 		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
# 		Cube()
# 		pygame.display.flip()
# 		pygame.time.wait(10)

# main()




window = 0
width,height = 500,400
def draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)                      # set window size
glutInitWindowPosition(0, 0)                           # set window position
window = glutCreateWindow(b"manas_sat")              # create window with title
glutDisplayFunc(draw)                                  # set draw function callback
glutIdleFunc(draw)                                     # draw all the time
glutMainLoop()   # start everything


# from matplotlib import *
# import matplotlib.pyplot as plt
# import matplotlib.image as img
# import numpy as np

# # a = np.random.randint(1,10,(3,2))

# # plt.plot([5,2,4])
# # plt.show()

# img1 = img.imread("learning.png")
# # print(img1)
# plt.imshow(img1)
# plt.show()
