
###################################################################################################################
# Init
###################################################################################################################

# escape codes

esc = chr(27) #'\x1B'
ff  = chr(12)

# temp height / width

w = 80
h = 1000

# tmp registr

escape_reg_count    = 50
escape_register     = [0 for x in range(escape_reg_count)]

###################################################################################################################
# wrt
###################################################################################################################

#------------------------------------------------------------------------------
def wrt ( c ):
    global matrix
    global fg_matrix
    global bg_matrix
    global xpos
    global ypos
    global fg_color
    global bg_color

    if c == ff:
        pass;
        xpos = 0
        ypos = 0
        #CLRSCR;
    else:
        if xpos < w and ypos < h and xpos >= 0 and ypos >= 0:
            
            matrix[xpos][ypos] = ord(c)
            fg_matrix[xpos][ypos] = fg_color
            bg_matrix[xpos][ypos] = bg_color

            xpos += 1
            if xpos > 79: #emulate old dos screen, auto move to next line
                ypos += 1
                xpos = 0

    #print ('x:'+str(xpos)+' y:'+str(ypos)+' '+c)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def set_graphics():
    global escape_mode
    global escape_str
    global escape_number
    global escape_register
    global lightcolor
    global fg_color
    global bg_color
    global matrix
    global xpos
    global ypos

    for i in range(1, escape_number+1):

        #print (str(i)+'------> '+str(escape_register[i]))
        if escape_register[i] == 0:
            lightcolor = False

            #if escape_number != 1:
            #DONT ALWAYS SET TO ZERO!
            #if fg_color == 7: 
            #    fg_color = 0 #reset color back to old color (else fg_color = 0)       
            #else:
            #    fg_color = 15     
            fg_color = 15  
            #fg_color = 7
            bg_color = 16 

        elif escape_register[i] == 1:
            lightcolor = True
        elif escape_register[i] == 5:
            bg_color = bg_color
            #bg_color += 8 #blink 
        elif escape_register[i] == 7:
            tmp_color = fg_color
            fg_color = bg_color
            bg_color = tmp_color
        elif escape_register[i] == 8: #new?!
            fg_color = 0
            bg_color = 16

        elif escape_register[i] == 30:  
            fg_color = 0 #black
        elif escape_register[i] == 31:  
            fg_color = 4 #red
        elif escape_register[i] == 32: 
            fg_color = 2 #green
        elif escape_register[i] == 33:  
            fg_color = 6 #brown
        elif escape_register[i] == 34:  
            fg_color = 1 #blue
        elif escape_register[i] == 35:  
            fg_color = 5 #magenta
        elif escape_register[i] == 36:  
            fg_color = 3 #cyan
        elif escape_register[i] == 37:  
            fg_color = 7 #white

        elif escape_register[i] == 40: 
            bg_color = 16 #black;
        elif escape_register[i] == 41:  
            bg_color = 20 #red;
        elif escape_register[i] == 42:  
            bg_color = 18 #green;
        elif escape_register[i] == 43:  
            bg_color = 22 #yellow;
        elif escape_register[i] == 44:  
            bg_color = 17 #blue;
        elif escape_register[i] == 45:  
            bg_color = 21 #magenta;
        elif escape_register[i] == 46:  
            bg_color = 19 #cyan;
        elif escape_register[i] == 47:  
            bg_color = 23 #white;

        #what about ICE colors?
        
        if (lightcolor) and (fg_color < 8):
            fg_color = fg_color + 8
        if (lightcolor == False) and (fg_color > 7):
            fg_color = fg_color - 8

    #fg_color = 7
    # bg_color = 0        
    #TEXTCOLOR ( FG );
    #TEXTBACKGROUND ( BG );
    #escape_mode = False
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def moveup():
    global xpos
    global ypos
    global escape_register
        
    if escape_register [1] < 1:
        escape_register [1] = 1
    ypos -= escape_register [1]

    #print 'up        x '+str(xpos)+' y '+str(ypos)
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def movedown():
    global xpos
    global ypos
    global escape_register  
    
    if escape_register [1] < 1:
        escape_register [1] = 1
    ypos += escape_register [1]

    #print 'down      x '+str(xpos)+' y '+str(ypos)
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def moveforward():
    global xpos
    global ypos
    global escape_register   
    global matrix

    if escape_register [1] < 1:
        escape_register [1] = 1
        
    for i in range (0, escape_register [1]):
        
        xpos += 1
        if xpos > 79: #emulate old dos screen, auto move to next line
            ypos += 1
            xpos = 0
    
    #print 'right     x '+str(xpos)+' y '+str(ypos)
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def movebackward():
    global xpos
    global ypos
    global escape_register    

    if escape_register [1] < 1:
        escape_register [1] = 1
    xpos -= escape_register [1]

    if xpos < 0:
      xpos = 0

    #print 'left      x '+str(xpos)+' y '+str(ypos)
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def savecursorpos():
    global xpos
    global ypos
    global saved_xpos
    global saved_ypos

    saved_xpos = xpos
    saved_ypos = ypos
#------------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def restorecursorpos():
    global xpos
    global ypos
    global saved_xpos
    global saved_ypos

    xpos = saved_xpos
    ypos = saved_ypos
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def addr_cursor():
    global escape_number
    global escape_register
    global escape_mode
    global xpos
    global ypos
    
    if escape_number == 1:
        escape_register [1] = 1
        escape_register [2] = 1
    elif escape_number == 2:
        escape_register [2] = 1
    #else:
    #    pass

    #if escape_register [1] == 25:
    #    xpos = escape_register [2] 
    #    ypos = 25
    #else:
    xpos = escape_register [2] - 1 #-1 because we work with 0-79
    ypos = escape_register [1] - 1 #-1 because we work with 0-79
    
    escape_mode = False

    #print 'addr      x '+str(xpos)+' y '+str(ypos)
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def clear_scr():
    global escape_number
    global escape_register
    global escape_mode
    global xpos
    global ypos

    if (escape_number == 1) and ( escape_register [1] == 2 ):
        xpos = 0
        ypos = 0
        
        #clear matrix?
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def clear_line():
    global escape_number
    global escape_register
    global escape_mode
    global xpos
    global ypos

    if (escape_number == 1) and ( escape_register [1] == 0 ):
        xpos = 79
        #ypos += 1 
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def process_escape ( c ):
    global escape_mode
    global escape_str
    global escape_number
    global escape_register
    global matrix
    global xpos
    global ypos
    
    #print ( 'ESC '+c )
    escape_str = escape_str + c

    if c == '[':
        return
    elif c == 'f' or c == 'H':
        addr_cursor()
        escape_mode = False
        return
    elif c == 'J':
        clear_scr()
        escape_mode = False
        return
    elif c == 'K':
        clear_line()
        escape_mode = False
        return
    elif c == 'm':
        set_graphics()
        escape_mode = False
        return
    elif c == 's':
        savecursorpos()
        escape_mode = False
        return
    elif c == 'u':
        restorecursorpos()
        escape_mode = False
        return
    elif c == 'A':
        moveup()
        escape_mode = False
        return
    elif c == 'B':
        movedown()
        escape_mode = False
        return
    elif c == 'C':
        moveforward()
        escape_mode = False
        return
    elif c == 'D':
        movebackward()
        escape_mode = False
        return
    elif c == 'h':
        escape_mode = False
        return
    elif c in ['0','1','2','3','4','5','6','7','8','9']:
        escape_register [escape_number] = int(escape_register [escape_number] * 10) + (ord ( c ) - ord ( '0' ))
        return
    elif c == ';' or c ==',':
        escape_number += 1
        escape_register [escape_number] = 0
        return

    #ch = upcase ( c );    
    #elif c in ['T', '#', '+', '-', '>', '<', '.', '=', '?']: #? is [?;7h
    #    return
#------------------------------------------------------------------------------

###################################################################################################################
# "screen" handler
###################################################################################################################

#------------------------------------------------------------------------------
def scrwrite ( c ):
    global escape_mode
    global escape_str
    global escape_number
    global escape_register
    global matrix
    global xpos
    global ypos

    if c == esc:
        escape_str = ""
        escape_number = 1
        escape_register [escape_number] = 0
        escape_mode = True
    else:
        if escape_mode:
            process_escape (c)
        else:
            if c == chr(13):
                ypos += 1
                xpos = 0
                return        
            if c == chr(10):
                return            
            if c == chr(26):
                return 
            
            wrt ( c )
            
            #print ( 'CHAR '+c )
#------------------------------------------------------------------------------


###################################################################################################################
# Main
###################################################################################################################

def ansi2mci(s,dumpquote=False,file=False):
    global lightcolor
    global escape_mode
    global escape_str
    global escape_number
    global escape_register

    global matrix
    global fg_matrix
    global bg_matrix
    global saved_xpos
    global saved_ypos
    global xpos
    global ypos

    global fg_color
    global bg_color


    matrix = [[32 for x in range(h)] for y in range(w)] 
    fg_matrix = [[15 for x in range(h)] for y in range(w)] 
    bg_matrix = [[16 for x in range(h)] for y in range(w)] 

    lightcolor      = False
    escape_str      = ""
    escape_mode     = True
    escape_number   = 0

    xpos = 0
    ypos = 0
    saved_xpos = 0
    saved_ypos = 0

    fg_color = 15
    bg_color = 16

    if file == True:
        with open(s) as f:
            while True:
                c = f.read(1)
                if not c:
                    break
                scrwrite ( c )
    else:
        for i in range(len(s)):
            c = s[i]        
            scrwrite ( c )
        
    y = 0
    lines = []

    while y <= ypos and y < h:
        x = 0
        line = ""

        fg_col = 0
        bg_col = 0

        while x < w:

            if dumpquote == False:
            
                #if fg_col <> fg_matrix[x][y] and fg_matrix[x][y] in [0,1,2,4,5,6,7,8,9,10,11,12,13,14,15]:
                if fg_col <> fg_matrix[x][y]:
                    line += "|"
                    line += str(fg_matrix[x][y]).zfill(2)
                    fg_col = fg_matrix[x][y]

                #if bg_col <> bg_matrix[x][y] and bg_matrix[x][y] in [16,17,18,19,20,21,22,23]:
                if bg_col <> bg_matrix[x][y]:
                    line += "|"
                    line += str(bg_matrix[x][y]).zfill(2)
                    bg_col = bg_matrix[x][y]


            line += chr(matrix[x][y])
            x += 1
        y += 1
        lines.append(line)         

    return lines
    
#ansi2mci('FILENAME.ANS',False,True):
