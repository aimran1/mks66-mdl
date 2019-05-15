import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    #print symbols
    for command in commands:
        op = command['op']
        args = command['args']
        if op == 'push':
            stack.append(stack[-1][:])
        elif op == 'pop':
            stack.pop()
        elif op == 'move':
            m = make_translate(args[0],args[1],args[2])
            matrix_mult(stack[-1],m)
        elif op == 'rotate':
            m = new_matrix()
            if args[0] == "x":
                m = make_rotX(args[1])
            elif args[0] == "y":
                m = make_rotY(args[1])
            elif args[0] == "z":
                m = make_rotZ(args[1])
            matrix_mult(stack[-1],m)
        elif op == 'scale':
            m = make_scale(args[0],args[1],args[2])
            matrix_mult(stack[-1],m)
        elif op == 'box':
            p = []
            add_box(p,args[0],args[1],args[2],args[3],args[4],args[5])
            matrix_mult(stack[-1],p)
            draw_polygons( p, screen, zbuffer, view, ambient, light, symbols, reflect)
        elif op == 'sphere':
            p = []
            add_sphere(p,args[0],args[1],args[2],args[3],step_3d)
            matrix_mult(stack[-1],p)
            draw_polygons( p, screen, zbuffer, view, ambient, light, symbols, reflect)
        elif op == 'torus':
            p = []
            add_torus(p,args[0],args[1],args[2],args[3],args[4],step_3d)
            matrix_mult(stack[-1],p)
            draw_polygons( p, screen, zbuffer, view, ambient, light, symbols, reflect)
            
            print command
