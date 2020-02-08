"""The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( 
    SceneInfo, GameStatus, PlatformAction
)
ball_last_x = 0
ball_last_y = 0
ball_did_change_to_moving_down = False

def get_ball_direction(x,y):
    return get_ball_is_moving_right(x), get_ball_is_moving_down(y)

def get_ball_is_moving_right(x):
    global ball_last_x
    result = x - ball_last_x
    ball_last_x = x
    return result > 0

def get_ball_is_moving_down(y):

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
    global ball_did_change_to_moving_down
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
    hit_x = 0
    hit_y = 0
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

        # 取得 每幀的 ball 資訊 
        # ball_info 為 ball 的動態: True/False: (向右/左, 向下/上) as tuple
        #
        ball_info = get_ball_direction(ball_x, ball_y)
        ball_is_going_right = ball_info[0]
        ball_is_going_down  = ball_info[1]
        ## 取得 ball 在開始下墜的點: hit_x, hit_y
        if not ball_is_going_down:
            print("ball moving up")
            ball_did_change_to_moving_down = False
            continue
        if not ball_did_change_to_moving_down:
            ball_did_change_to_moving_down = True
            hit_x = ball_x
            hit_y = ball_y
        print("hit_x, hit_y:",hit_x, hit_y, ball_is_going_right)
        # if ball_x < platform_x:
        #     comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        # else:
        #     comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        # 3.4. Send the instruction for this frame to the game process
