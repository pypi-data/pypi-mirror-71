def builder(list,bmode =" ",speed=-1,net_colors=None):
    """

    Creat Neural network architectures:
    builder(list,bmode,speed,net_colors)
    list: a python list containing the number of units in each layers
    bmode: set to "night" for dark theme
    speed: configure the speed to build your networl (-1 for max speed)
    net_colors: a list containing colors for the edges conecting the layers

    """

    # Just a if esle to stop if user if color size is wrong
    if net_colors != None:
        if len(net_colors) >= (len(list)-1):
            #print("ok")
            pass
        else:
            print("Error: please provide n-1 colors for a n layer Neural net")
            return   # implicitly, this is the same as saying return None (stops program when error)

    try:
        import turtle
        import random
        turtle.clear()
       # Default Colors of normal mode
        b_color = 'white'
        pen_color = '#1B2631'

        screen = turtle.Screen()
        screen.title("EIFFEL: NEURAL NETWORK BUILDER")
        screen.setup(width=100,height=100)
        win_width, win_height= 2000, 2000
        turtle.setup()
        turtle.screensize(win_width, win_height)

       # change default colors if bmode ="night"
        if bmode == "night":
            pen_color ="white"
            b_color = ('#1B2631')

        screen.bgcolor(b_color)

        pen = turtle.Turtle()
        pen.hideturtle()
        pen.color(pen_color)
        turtle.color(b_color)
        pen.speed(speed)
        pen.width(0.2)



        ### NODES ####
        sub =0
        y=50
        x = -250
        y_history=[]
        x_history=[]
        architecture = list # a list conting the activation layers in form of their shape

        for j in range(len(architecture)):
            if j != 0: #do not do the following with the first element
                try:
                    sub = 10* (architecture[j-1] - architecture[j])  # give vertical tab to layers (if two layers have the same number of units then it does not give tab)
                except:
                    pass # so that the code can be excecuted since when we get to the alst element of the list there was an error

            y = y - sub  # create a dummi to sve the new y-coordinate with vertical tab
            y_cache = y  # save it in order to be used in next iteration
            x += 70      # give horizontal tab to x every itreation
            for i in range(architecture[j]):
                y_history.append(y)
                x_history.append(x)
                y -= 20
                pen.speed(speed)
                pen.penup()         # penup so we don't draw when we move
                pen.setpos((x  ,y)) # set positon
                pen.pendown()       # pendown so we can draw
                pen.circle(10)      # draw units
            y = y_cache # Since we changed y to draw nodes, lets regained our orignal value to use it for nex iteration

        ### EDGES ####

        p1=0
        p2=0
        p3=0


       ### iterate over each layer
        for j in range(0,len(architecture)-1):
            if net_colors != None:
                pen.color(net_colors[j])
            p2+=architecture[j]
            p3=architecture[j+1]

            for i in range(p1,p2):
                for a in range(p3):
                    pen.penup()
                    pen.setpos((x_history[i]+10,y_history[i]-10))
                    pen.down()
                    pen.setpos((x_history[p2+a]-5,y_history[p2+a]-10))

            p1+=architecture[j]

        #Turtle options

        def byebye(): #function to exit
            screen.bye()

        turtle.listen()           # enables turtle to wait for prevents
        turtle.onkey(byebye,"e")  # exit when e is pressed
        turtle.exitonclick()      # exit on click
    except:                       # used to restart thinker when it does not work
        builder(list,bmode,speed,net_colors)
