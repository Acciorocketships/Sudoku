import sys
import random

# global variables
Nx = 3
Ny = 3


def list_copy (x):
    y = []
    for i in range(len(x)):
        y.append(x[i])
    return (y)

def list_shuffle (lx,iter=10):
    llx = list_copy(lx)

    if len(lx) <= 1:
        return (llx)

    # permutations with iter times
    for i in range(iter):
        j = int(random.random()*float(len(lx)))
        k = int(random.random()*float(len(lx)))
        if j == k: continue
        #print 'perm: ',j,k

        # swap j and k of a[]
        b      = llx[j]
        llx[j] = llx[k]
        llx[k] = b

    return (llx)


def list_shuffle_pair (lx,ly,iter=10):
    llx = list_copy(lx)
    lly = list_copy(ly)

    if len(lx) <= 1:
        return (llx,lly)

    # permutations with iter times
    for i in range(iter):
        j = int(random.random()*float(len(lx)))
        k = int(random.random()*float(len(lx)))
        if j == k: continue
        #print 'perm: ',j,k

        # swap j and k of a[]
        b      = llx[j]
        llx[j] = llx[k]
        llx[k] = b

        b      = lly[j]
        lly[j] = lly[k]
        lly[k] = b

    return (llx,lly)


def conv_ent (x):
    ascii_table = [' ',
                   '1','2','3','4','5','6','7','8','9',
                   '0',
                   'A','B','C','D','E','F','G',
                   'H','I','J','K','L','M','N',
                   'O','P','Q','R','S','T','U',
                   'V','W','X','Y','Z']
    if x == 0:
        return ' '
    elif x < 0:
        return '.'
    else:
        return '%c'%(ascii_table[x])

################
## sub board
def init_sub ():
    global Nx
    global Ny

    a = []
    for i in range(Nx*Ny):
        a.append(0)
    return a

def gen_sub (a, iter=10):
    global Nx
    global Ny

    # table for shift
    a_ = []
    for i in range(Nx*Ny):
        a_.append(i+1)
    # that is, a_ = [1,2,3,4,5,6,7,8,9] is expected for Nx = Ny = 3

    atmp = list_shuffle (z,iter)

    # single shift
    # generate a random index j in [0,8]
    j = int(random.random()*float(Nx*Ny))
    for i in range(Nx*Ny):
        a_[(i+j)%(Nx*Ny)] = atmp[i]

    return (a_)

# (i,j): (1,1), (1,2), ..., (1,Nx),
#        (2,1),        ..., (2,Nx),
#          :                  :
#        (Ny,1),       ..., (Ny,Nx).
def idx_sub (i,j):
    global Nx

    return i*Nx + j

def init_sub ():
    global Nx
    global Ny

    a = []
    for i in range(Nx*Ny):
        a.append(i)
    return a

def print_sub (sub):
    global Nx
    global Ny

    for i in range (Ny):
        if i%Ny == 0:
            #print '+-----+'
            for j in range (Nx):
                if j%Nx == 0:
                    print('+-', end=' ')
                else:
                    print('--', end=' ')
            print('+')

        for j in range (Nx):
            if j%Nx == 0:
                print('|%c'%(conv_ent(sub[idx_sub(i,j)])), end=' ')
            else:
                print(' %c'%(conv_ent(sub[idx_sub(i,j)])), end=' ')
        print('|')
    #print '+-----+\n'
    for j in range (Nx):
        if j%Nx == 0:
            print('+-', end=' ')
        else:
            print('--', end=' ')
    print('+')


################
## full board
def init_full ():
    global Nx
    global Ny

    a = []
    for i in range((Nx*Ny)*(Nx*Ny)):
        a.append(0)
    return a


# (i,j): (1,1), (1,2), ..., (1,Nxy),
#          :                  :
#        (Nxy,1),    ..., (Nxy,Nxy).
def idx_full (i,j):
    global Nx
    global Ny

    return i*(Nx*Ny) + j


def print_full (full):
    global Nx
    global Ny

    for i in range (Nx*Ny):
        if i%Ny == 0:
            for j in range (Nx*Ny):
                if j%Nx == 0:
                    print('+-', end=' ')
                else:
                    print('--', end=' ')
            print('+')
        for j in range (Nx*Ny):
            if j%Nx == 0:
                print('|%c'%(conv_ent(full[idx_full(i,j)])), end=' ')
            else:
                print(' %c'%(conv_ent(full[idx_full(i,j)])), end=' ')
        print('|')

    for j in range (Nx*Ny):
        if j%Nx == 0:
            print('+-', end=' ')
        else:
            print('--', end=' ')
    print('+')


def set_sub_in_full (full,i,j,sub):
    global Nx
    global Ny

    for isub in range(Ny):
        for jsub in range(Nx):
            full [idx_full(i*Ny+isub,j*Nx+jsub)] = sub [idx_sub(isub,jsub)]
    return full

# extract a sub board from full board
# NOTE: x,y = [0,2]
def get_sub_from_full (full, i, j):
    global Nx
    global Ny

    a = init_sub()
    for isub in range(Ny):
        for jsub in range(Nx):
            a[idx_sub(isub,jsub)] = full[idx_full(i*Ny+isub,j*Nx+jsub)]
    return a



################
## some utility

# return candidate digits for a[]
# that is, the digits not appeared in a[]
def candidates (a):
    global Nx
    global Ny

    x = []
    for i in range(Nx*Ny):
        x.append(i+1)
    # that is, x = [1,2,3,4,5,6,7,8,9] is expected for Nx = Ny = 3
    for i in range(len(a)):
        for j in range(len(x)):
            if x[j] == a[i]:
                x[j] = 0
    b = []
    for i in range(len(x)):
        if x[i] > 0:
            b.append(x[i])
    return b

# extract a row from full board
# NOTE: i = [0,8]
def row_from_full (full, i):
    global Nx
    global Ny

    a = []
    for j in range(Nx*Ny):
        a.append(full[idx_full(i,j)])
    return a

# extract a column from full board
# NOTE: j = [0,8]
def column_from_full (full, j):
    global Nx
    global Ny

    a = []
    for i in range(Nx*Ny):
        a.append(full[idx_full(i,j)])
    return a


def get_possibilities (full, i, j):
    global Nx
    global Ny

    row = row_from_full (full, i)
    can_row = candidates (row)

    col = column_from_full (full, j)
    can_col = candidates (col)

    sml = get_sub_from_full (full, int(i/Ny), int(j/Nx))
    can_sml = candidates (sml)

    b = []
    for k in range(1,(Nx*Ny)+1):
        if k in can_col and \
           k in can_row and \
           k in can_sml:
            b.append(k)
    return b


# return the list (i,j) for entries of 'z' in the full board
def list_extract_entries (full,z):
    global Nx
    global Ny

    li = []
    lj = []
    for i in range(Nx*Ny):
        for j in range(Nx*Ny):
            if full[idx_full(i,j)] == z:
                li.append(i)
                lj.append(j)
    return (li,lj)

# return the list of (i,j) for undefined entries of full board
def list_open_entries (full):
    return list_extract_entries (full,0)


# return the list (i,j) for defined entries of full board
def list_active_entries (full):
    global Nx
    global Ny

    li = []
    lj = []
    for i in range(Nx*Ny):
        for j in range(Nx*Ny):
            if full[idx_full(i,j)] > 0:
                li.append(i)
                lj.append(j)
    return (li,lj)



def count_zeros (a):
    n = 0
    for i in range(len(a)):
        if a[i] == 0:
            n += 1
    return n


def make_board():
    global Nx
    global Ny

    full = init_full()

    icount = 0
    while 1:
        # nz is the number of zeros at this moment, for checking
        #nz = 0
        for i in range(Nx*Ny):
            for j in range(Nx*Ny):
                if full[idx_full(i,j)] != 0:
                    continue

                c = get_possibilities (full, i, j)
                if len(c) == 0:
                    #nz += 1
                    # no possible number... we'll try again later
                    continue
                idx = int(random.random()*float(len(c)))
                x = c[idx]
                full[idx_full(i,j)] = x

        #print 'count',icount,'nz=',nz
        #print_full (full)

        if 0 not in full:
            # done!
            break

        # reset around undefined entries
        (li,lj) = list_open_entries (full)
        for k in range(len(li)):
            i = li[k]
            j = lj[k]

            row = row_from_full (full,i)
            n0 = count_zeros (row)
            if n0 < (Nx*Ny):
                while 1:
                    jj = int(random.random()*float(Nx*Ny))
                    if jj != j and full[idx_full(i,jj)] != 0:
                        break
                full[idx_full(i,jj)] = 0

            col = column_from_full (full,j)
            n0 = count_zeros (col)
            if n0 < (Nx*Ny):
                while 1:
                    ii = int(random.random()*float(Nx*Ny))
                    if ii != i and full[idx_full(ii,j)] != 0:
                        break
                full[idx_full(ii,j)] = 0

        icount += 1

    #print 'count',icount
    return (full)


def zeros_on_sub(s):
    global Nx
    global Ny

    li = []
    lj = []
    for i in range(Ny):
        for j in range(Nx):
            if s[idx_sub(i,j)] == 0:
                li.append(i)
                lj.append(j)
    return (li,lj)

# check possible entry for each value [1,9] by masking sub boards
# OUTPUT
#  (flag,xx) : where...
#  flag      : 0 un-updated
#            : 1 updated
#  xx        : updated full board
def check_by_mask (x):
    global Nx
    global Ny

    xx = list_copy(x)
    flag = 0

    for z in range(1,(Nx*Ny)+1):
        (li,lj) = list_extract_entries (xx,z)
        y = init_full()
        for k in range(len(li)):
            y[idx_full(li[k],lj[k])] = xx[idx_full(li[k],lj[k])]

        # mask by -1
        for i in range(len(x)):
            if xx[i] > 0 and y[i] == 0:
                y[i] = -1
        # 0  : open
        # -1 : given by other number except for 'z'

        for k in range(len(li)):
            # sweep li[k]
            for jj in range(Nx*Ny):
                if jj != lj[k] and y[idx_full(li[k],jj)] == 0:
                    y[idx_full(li[k],jj)] = -1
            # sweep lj[k]
            for ii in range(Nx*Ny):
                if ii != li[k] and y[idx_full(ii,lj[k])] == 0:
                    y[idx_full(ii,lj[k])] = -1
            # sweep sub cell of li[k],lj[k]
            # (i0,j0) is the number of sub cell, i0 = 0~(Nx-1), j0= 0~(Ny-1).
            # in full board, the left top corner is (i0*Nx, j0*Ny).
            # Note that the size of sub cell is (Ny, Nx).
            i0 = int(li[k]/Ny)
            j0 = int(lj[k]/Nx)
            for ii in range(Ny):
                for jj in range(Nx):
                    if y[idx_full(i0*Ny+ii,j0*Nx+jj)] == 0:
                        y[idx_full(i0*Ny+ii,j0*Nx+jj)] = -1

        # check for each sub boards
        for isub in range(Nx):
            for jsub in range(Ny):
                s = get_sub_from_full (y,isub,jsub)
                (li,lj) =  zeros_on_sub(s)
                if len(li) != 1:
                    continue

                if s[idx_sub(li[0],lj[0])] != 0:
                    print('something is wrong...')
                    sys.exit()
                flag = 1
                xx[idx_full(isub*Ny+li[0],jsub*Nx+lj[0])] = z

    return (flag,xx)


# OUTPUT
#  0 : unsolvable
#  1 : solvable
def check_solvability(x, i, j):
    flag_updated = 0

    c = get_possibilities (x, i, j)
    if len(c) == 1:
        # unique entry
        return 1

    # try further consideration...
    (flag_updated,xx) = check_by_mask(x)
    if flag_updated == 0:
        # no update
        return 0

    if xx[idx_full(i,j)] == 0:
        # updated but not on (i,j)
        return 0

    # (i,j) is restored
    return 1

def make_problem():
    answer = make_board()
    x  = list_copy(answer)
    while 1:
        # make a backup of the board
        x0 = list_copy(x)

        # make random site (ix,iy) whose value is non-zero
        (li, lj)  = list_active_entries (x)
        (lli,llj) = list_shuffle_pair (li,lj,iter=len(li)*len(li))

        flag_solv = 0
        for k in range(len(lli)):
            i = lli[k]
            j = llj[k]
            # z is backup of x[i,j]
            z = x[idx_full(i,j)]
            x[idx_full(i,j)] = 0
            # 1) first, 1-step check for (i,j)
            flag_check = check_solvability (x, i, j)
            if flag_check == 1:
                #solvable
                flag_solv = 1
                break
            # so, (i,j) could not be deleted.
            # restore x[], and...
            x[idx_full(i,j)] = z
            # try next choice

        if flag_solv == 0:
            # unsolvable
            break
        # try to remove entry further!

    # return the final "solvable" board
    return [x0[x*9:x*9+9] for x in range(9)]












class SudokuBoard:

    def __init__(self):
        self.board = [[None]*9]*9

    def generate(self):
        self.board = make_problem()
        # for i,row in enumerate(self.board):
        #     for j,element in enumerate(row):
        #         if element == 0:
        #             self.board[i][j] = None
        self.board = [[(el if el != 0 else None) for el in row] for row in self.board]
        return self.board
