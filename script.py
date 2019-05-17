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

    for command in commands:
        op = command['op']
        args = command['args']
        cs = stack
        if 'cs' in command and command['cs'] != None:
            cs = command['cs']
        if op == 'push':
            copy = cs[-1][:]
            cs.append(copy)
        elif op == 'pop':
            cs.pop()
        elif op == 'move':
            m = make_translate(float(args[0]),float(args[1]),float(args[2]))
            matrix_mult(cs[-1],m)
            cs[-1] = m
        elif op == 'rotate':
            m = new_matrix()
            a = float(args[1]) * (math.pi/180)
            if args[0] == "x":
                m = make_rotX(a)
            elif args[0] == "y":
                m = make_rotY(a)
            elif args[0] == "z":
                m = make_rotZ(a)
            matrix_mult(cs[-1],m)
            cs[-1] = m
        elif op == 'scale':
            m = make_scale(float(args[0]),float(args[1]),float(args[2]))
            matrix_mult(cs[-1],m)
            cs[-1] = m
        elif op == 'box':
            try:
                p = []
                cons = command['constants']
                add_box(p,float(args[0]),float(args[1]),float(args[2]),float(args[3]),float(args[4]),float(args[5]))
                matrix_mult(cs[-1],p)
                if cons != None:
                    draw_polygons( p, screen, zbuffer, view, ambient, light, symbols, cons)
                else:
                    draw_polygons( p, screen, zbuffer, view, ambient, light, symbols, reflect)
            except:
                continue
        elif op == 'sphere':
            try:
                p = []
                cons = command['constants']
                add_sphere(p,float(args[0]),float(args[1]),float(args[2]),float(args[3]),step_3d)
                matrix_mult(cs[-1],p)
                if cons != None:
                    draw_polygons( p, screen, zbuffer, view, ambient, light, symbols, cons)
                else:
                    draw_polygons( p, screen, zbuffer, view, ambient, light, symbols, reflect)
            except:
                continue
        elif op == 'torus':
            try:
                p = []
                cons = command['constants']
                add_torus(p,float(args[0]),float(args[1]),float(args[2]),float(args[3]),float(args[4]),step_3d)
                matrix_mult(cs[-1],p)
                if cons != None:
                    draw_polygons( p, screen, zbuffer, view, ambient, light, symbols, cons)
                else:
                    draw_polygons( p, screen, zbuffer, view, ambient, light, symbols, reflect)
            except:
                continue
        elif op == 'line':
            e = []
            add_edge(e, float(args[0]),float(args[1]),float(args[2]),float(args[3]),float(args[4]),float(args[5]))
            matrix_mult(cs[-1],e)
            draw_lines(e,screen,zbuffer,color)
        elif op == 'save':
            save_extension(screen, args[0])
        elif op == 'display':
            display(screen)
