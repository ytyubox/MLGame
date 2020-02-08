"""The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)
ball_last_x = 0
ball_last_y = 0
ball_hitPoint = [0,0]
def get_ball_direction(x,y):

    global ball_last_y
    # print(y,ball_last_y)
    d = y - ball_last_y
    is_go_down = False
    if d > 0:
        # print("⏬")
        is_go_down = True
    # else: 
        # print("⏫")

    ball_last_y = y
    return is_go_down
    
def ml_loop():
    """The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information
        ball_x = scene_info.ball[0]
        ball_y = scene_info.ball[1]
        platform_x = scene_info.platform[0]
        direction = get_ball_direction(ball_x, ball_y)
        print("ball move down:", direction)
        # if ball_x < platform_x:
        #     comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        # else:
        #     comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        # 3.4. Send the instruction for this frame to the game process
