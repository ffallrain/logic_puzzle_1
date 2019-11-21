import sys,os
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import math

# add a line
def make_board():
    l = list()
    for i in range(0,5):
        for j in range(0,5):
            l.append((i,i,0,4))
            l.append((0,4,i,i))
    return l

def make_blank_board_line_ids():
    ids = { 'h':list(),'v':list() }
    for x in range(4):
        for y in range(5):
            ids['h'].append( (x,y) )
    for x in range(5):
        for y in range(4):
            ids['v'].append( (x,y) )
    return ids

# draw lines
def draw_lines(lines,ax,color='grey',lw=5,alpha=0.3,gid=None):
    for l in lines:
        x = l[0:2]
        y = l[2:4]
        line = mlines.Line2D(x , y, lw=lw, alpha=alpha,color=color,gid=gid)
        ax.add_line(line)
    
# draw piece
def draw_piece(lines,ax,color='g',lw=15,alpha=0.7,gid="P"):
    draw_lines(lines,ax,color,lw,alpha,gid=gid)
    pass

# generate piece all possible locations
def generate_all_loc():
    loc = list()
    for i in range(-1,5):
        for j in range(-1,5):
            for k in range(8):
                loc.append((i,j,k))
    loc = np.array(loc)
    return loc

# generate logical all possible locations
def generate_logic_all_loc(piece,board=None):
    all_loc = generate_all_loc()
    keep_loc = list()
    for loc in all_loc:
        ids = derive_piece_line_ids(piece,loc)
        if check_lines_in_board(ids,board=board):
            keep_loc.append(loc)
    return keep_loc

# derive piece line_ids :
def derive_piece_line_ids(piece,loc):
    piece = np.array(piece)
    ids = { 'h':list(),'v':list() }
    # Treat mirror
    if loc[2] in (4,5,6,7):
        for i in range(len(piece)):
            piece[i][0] = 0 - piece[i][0]
    # Rotate
    new_piece = list()
    A = math.pi * 0.5 * (loc[2]%4)
    cosA = math.cos(A)
    sinA = math.sin(A)
    for tmp in piece :
        x,y = tmp
        nx = round(x * cosA - y * sinA)
        ny = round(x * sinA + y * cosA)
        new_piece.append( (nx,ny) )
    for tmp in new_piece:
        if tmp[0]%2==0 and tmp[1]%2==1: # horizonal 
            x = tmp[0]/2. + loc[0]
            y = (tmp[1]+1)/2. + loc[1]
            ids['h'].append( (x,y) )
        elif tmp[0]%2==1 and tmp[1]%2==0: # vertical 
            x = (tmp[0]+1)/2. + loc[0]
            y = tmp[1]/2. + loc[1]
            ids['v'].append( (x,y) )
        else:
            print("Error")
            raise Exception
    return ids

# derive piece lines:
def derive_piece_lines( ids ):
    all_lines = list()
    if check_lines_in_board(ids):
        pass
    else:
        return False
    for a in ids['v'] : # vertical
        x,y = a
        x0 = x
        x1 = x
        y0 = y
        y1 = y+1
        all_lines.append( (x0,x1,y0,y1) )
    for a in ids['h'] : # horizonal
        x,y = a
        x0 = x
        x1 = x + 1
        y0 = y
        y1 = y
        all_lines.append( (x0,x1,y0,y1) )
    return all_lines

# derive piece lines interface:
def compute_piece_lines( piece, loc ):
    ids = derive_piece_line_ids(piece,loc)
    lines = derive_piece_lines(ids)
    return lines

def check_lines_in_board( ids,board = None ):
    in_board = True
    for a in ids['v'] : # vertical
        x,y=a
        if 0<=x<5 and 0<=y<4:
            pass
        else:
            in_board = False
    for a in ids['h'] : # horizonal
        x,y=a
        if 0<=x<4 and 0<=y<5:
            pass
        else:
            in_board = False
    if board != None:
        for a in ids['v']:
            if a in board['v']:
                in_board = False
        for a in ids['h']:
            if a in board['h']:
                in_board = False
    return in_board

if True:
    piece_h = ( (0,1) ,(1,0), (-1,0),(-1,2) )
    piece_x = ( (0,1) ,(2,1), (1,0), (1,2)  )
    piece_w = ( (-1,2),(1,0), (0,1), (2,-1) )
    piece_u = ( (-1,0),(0,-1),(2,-1),(3,0)  )
    piece_s = ( (-1,2),(0,1), (0,-1),(1,0)  )
    piece_l = ( (-1,0),(-1,2),(-1,4),(0,-1) )
    piece_j = ( (-1,0),(-1,2),(1,0), (0,-1) )
    piece_n = ( (-1,0),(-1,2),(0,1), (0,-1) )
    piece_t = ( (-1,0),(-1,2),(-1,4),(0,1)  )
    piece_y = ( (-1,2),(1,0), (0,1), (2,1)  )

    all_pieces = { 'h': piece_h ,
                   'x': piece_x ,
                   'w': piece_w ,
                   'u': piece_u ,
                   's': piece_s ,
                   'l': piece_l ,
                   'j': piece_j ,
                   'n': piece_n ,
                   't': piece_t ,
                   'y': piece_y ,
    }
    piece_colors ={'h': "dimgray" ,
                   'x': "green" ,
                   'w': "magenta" ,
                   'u': "black" ,
                   's': "red" ,
                   'l': "blue" ,
                   'j': "purple" ,
                   'n': "orange" ,
                   't': "brown" ,
                   'y': "yellow" ,
    }

    def _generate_legal_loc_for_piece( piece ):
        all_loc = list()
        keep_uniq = list()
        for i in range(-1,5):
            for j in range(-1,5):
                for k in range(8):
                    loc = (i,j,k)
                    ids = derive_piece_line_ids(piece,loc)
                    if check_lines_in_board(ids):
                        a = list(ids['h'])
                        b = list(ids['v'])
                        a.sort()
                        b.sort()
                        uniq = a+b
                        if uniq not in keep_uniq:
                            keep_uniq.append(uniq)
                            all_loc.append(loc)
        return all_loc
    piece_locs = dict()
    for name,piece in all_pieces.items():
        piece_locs[name] = _generate_legal_loc_for_piece(piece)

for name,piece in all_pieces.items():
    print(name,len(piece_locs[name]))

os.system("rm -r ?")
for name,piece in all_pieces.items():
    i = 0
    color = piece_colors[name]
    os.system("mkdir %s"%name)
    for loc in piece_locs[name]:
        piece_lines = compute_piece_lines( piece, loc )
        if piece_lines:
            fig, ax = plt.subplots()
            board_lines = make_board()
            draw_lines(board_lines,ax)
            draw_piece(piece_lines,ax,color=color)
            plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
            plt.axis('equal')
            plt.axis('off')
            plt.savefig("%s/%d.png"%(name,i))
            plt.close()
        i += 1

