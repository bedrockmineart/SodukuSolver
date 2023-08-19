# Soduku solver

import random
import copy

grid = [[[[],[],[]],[[],[],[]],[[],[],[]]],[[[],[],[]],[[],[],[]],[[],[],[]]],[[[],[],[]],[[],[],[]],[[],[],[]]]]
#grid = [[[['8', '0', '6'], ['0', '9', '0'], ['0', '0', '0']], [['0', '0', '0'], ['0', '0', '0'], ['6', '0', '0']], [['5', '0', '0'], ['0', '1', '0'], ['0', '0', '0']]], [[['0', '0', '0'], ['7', '0', '0'], ['0', '0', '0']], [['2', '0', '7'], ['0', '4', '0'], ['0', '0', '0']], [['6', '8', '0'], ['0', '0', '0'], ['0', '5', '9']]], [[['0', '7', '0'], ['0', '3', '0'], ['2', '0', '0']], [['0', '0', '6'], ['0', '1', '0'], ['8', '0', '9']], [['0', '0', '0'], ['0', '2', '5'], ['3', '0', '0']]]]
print( 'Input the number in horizontal order, 0 for blanks' )

numbers = ['1','2','3','4','5','6','7','8','9', '0']

zeros = 0

def printGrid( grid ):
    print( '-------------------------')
    for i in range(9):
        line = '|'
        for c in range(9):
            val = ' '
            special = ''
            if c%3 == 2:
                special = ' |'
            if c%3 < len( grid[ i//3 ][ c//3 ][ i%3 ] ):
                val = grid[ i//3 ][ c//3 ][ i%3 ][ c%3 ]
            line = line + ' ' + val + special
        print(line)
        if i % 3 == 2:
            print( '-------------------------')
def collectInfo():
    for i in range(81):
        inp = input()
        while not inp in numbers:
            if inp == '-':
                printGrid( grid )
            else:
                print( 'Not a valid input, try again:')
            inp = input()
        grid[ i//27 ][ ( i//3 )%3 ][ ( i//9 ) % 3 ].append(inp)
        #print(str((i//3)%3) + ' ' + str( i//27 ) + ' ' + str( ( i//9 ) % 3 ) + ' ' + str( i % 3 ) )


collectInfo()

def checkIfGridIsValid( grid ):
    for i in range(3):
        for c in range(3):
            number = []
            for d in range(9):
                if grid[i][c][d//3][d%3] != '0':
                    if grid[i][c][d//3][d%3] in number:
                        return False
                    else:
                        number.append(grid[i][c][d//3][d%3])
    
    for i in range(9):
        number = []
        for c in range(9):
            n = grid[ c//3 ][ i//3 ][ c%3 ][ i%3 ]
            if n != '0':
                if n in number:
                    return False
                else:
                    number.append(n)
    for i in range(9):
        number = []
        for c in range(9):
            n = grid[ i//3 ][ c//3 ][ i%3 ][ c%3 ]
            if n != '0':
                if n in number:
                    return False
                else:
                    number.append(n)
    return True

def closeGap( gridF ):
    changed = False
    firstDuo = []
    for i in range(3):
        for c in range(3):
            for d in range(3):
                for f in range(3):
                    if gridF[i][c][d][f] == '0':
                        fitting = []
                        tGrid = copy.deepcopy(gridF)
                        for e in range(9):
                            tGrid[i][c][d][f] = str(e+1)
                            if checkIfGridIsValid( tGrid ):
                                fitting.append(str(e+1))
                        tGrid[i][c][d][f] = '0'
                        if len(fitting) == 0:
                            #print( 'Cannot fit anything into ' + str(i) + ' ' + str(c) + ' ' + str(d) + ' ' + str(f) )
                            #printGrid(tGrid)
                            return False, firstDuo
                        if len(fitting) == 1:
                            changed = True
                            #print('Changing position to ' + fitting[0] )
                            gridF[i][c][d][f] = fitting[0]
                        else:
                            if len(fitting) == 2 and len(firstDuo) == 0:
                                firstDuo.append(i)
                                firstDuo.append(c)
                                firstDuo.append(d)
                                firstDuo.append(f)
                                firstDuo.append(fitting)
                            gridF[i][c][d][f] = '0'
    if changed:
        #print('looping')
        gridF, Duo = closeGap(gridF.copy())
        if len(Duo):
            firstDuo = Duo
    return gridF, firstDuo
#close gap > split on first double and add to list > close gap (return to start) but if one returns 0 then go back to next split

def countZeros( gridF ):
    count = 0
    for i in range(3):
        for c in range(3):
            for d in range(3):
                for f in range(3):
                    if gridF[i][c][d][f] == '0':
                        count += 1
    return count

def printForkLog( forkLog ):
    print('hi')

def solveGrid(grid):
    solved = False
    attempt = 1
    zerosAtStart = countZeros(grid)
    forks = [ copy.deepcopy(grid) ]
    forkLog = []
    while not solved:
        new, duo = closeGap( copy.deepcopy(forks[ 0 ]) )
        if not new:
            if len(forks) == 1:
                printGrid(forks[0])
                #printForkLog(forkLog)
                return
            forks.pop(0)
        else:
            if new == forks[ 0 ]:
                NewList2 = copy.deepcopy(forks[0])
                NewList = copy.deepcopy(forks[0])
                if len(duo) != 5 or duo[0] >= len(NewList2) or duo[1] >= len(NewList2[duo[0]]) or duo[2] >= len(NewList2[duo[0]][duo[1]]) or duo[3] >= len(NewList2[duo[0]][duo[1]][duo[2]]) or len(duo[4]) != 2:
                    if countZeros( forks[0] ) == 0:
                        print('I think i solved it lol')
                        printGrid(forks[0])
                    else:
                        print('Too hard for me to solve')
                    return
                NewList2[duo[0]][duo[1]][duo[2]][duo[3]] = duo[4][0]
                NewList[duo[0]][duo[1]][duo[2]][duo[3]] = duo[4][1]
                forks[0] = NewList2
                forks.append(NewList)
            else:
                forks[ 0 ] = copy.deepcopy(new)
        

if checkIfGridIsValid( grid ):
    print( 'Calculating...' )
    solveGrid(grid)
else:
    quit()

#grid = [[[['8', '0', '6'], ['0', '9', '0'], ['0', '0', '0']], [['0', '0', '0'], ['0', '0', '0'], ['6', '0', '0']], [['5', '0', '0'], ['0', '1', '0'], ['0', '0', '0']]], [[['0', '0', '0'], ['7', '0', '0'], ['0', '0', '0']], [['2', '0', '7'], ['0', '4', '0'], ['0', '0', '0']], [['6', '8', '0'], ['0', '0', '0'], ['7', '5', '9']]], [[['0', '7', '0'], ['0', '4', '0'], ['2', '0', '0']], [['4', '2', '6'], ['7', '1', '3'], ['8', '5', '9']], [['0', '0', '0'], ['0', '2', '5'], ['4', '0', '0']]]]
