def go_game(board):
    print('Board:')
    [print(row) for row in board]

    return {'B': 3, 'W': 4}


if __name__ == '__main__':

    assert go_game(['++++W++++',
                    '+++WBW+++',
                    '++BWBBW++',
                    '+W++WWB++',
                    '+W++B+B++',
                    '+W+BWBWB+',
                    '++++BWB++',
                    '+B++BWB++',
                    '+++++B+++']) == {'B': 3, 'W': 4}