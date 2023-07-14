import random
act_same_num = 0
pre_act = None
map_num = 0
get_dish_Y = 1
get_onion_Y = 1
onions_p1 = 0
onions_p2 = 0
in_action = 0
onion_num = 0
agent_old = []
flag = 0
giving_onion = 0  
NORTH = (0, -1)
SOUTH = (0, 1)
EAST  = (1, 0)
WEST  = (-1, 0)
up       = [1, 0, 0, 0, 0, 0]
down     = [0, 1, 0, 0, 0, 0]
right    = [0, 0, 1, 0, 0, 0]
left     = [0, 0, 0, 1, 0, 0]
still    = [0, 0, 0, 0, 1, 0]
interact = [0, 0, 0, 0, 0, 1]
Ori_Helper = {1:NORTH,2:SOUTH,3:EAST,4:WEST}
Turn_Helper = {NORTH:0,SOUTH:1,EAST:2,WEST:3}
direction = { 
    NORTH :up,
    SOUTH :down,
    EAST  :right,
    WEST  :left
}
def my_controller(obs, action_space, is_act_continuous=False):
    #print(obs)
    global act_same_num,pre_act
    agent_action = []
    each_ = controller(obs,is_act_continuous = False)
    if pre_act != None:
        if pre_act == each_:
            act_same_num += 1
        else:
            act_same_num = 0
    if act_same_num > 10:
        act_same_num -= 0.1
        pre_act = None
        rand_action = [0]*6
        rand_action[my_random2()] = 1
        agent_action.append(rand_action)
        return agent_action
    pre_act = each_
    agent_action.append(each_)
    return agent_action

def get_map_num(observation):
    global map_num
    if observation['new_map'] == True:
        map_num += 1
    print('mapnum=',map_num)
    return ((map_num+1)//2)                       

def controller(obs,is_act_continuous = False):
    map_num=get_map_num(obs)
    if (map_num == 1):
        each = condition_judge1(obs,is_act_continuous)
        if each  == None or  has_only_single_one(each)==0:
            each_=[0]*6
            each_[my_random2()]=1
            return each_
        
        return each
    if (map_num == 2):
        each = condition_judge2(obs,is_act_continuous)
        if each  == None or  has_only_single_one(each)==0:
            each_=[0]*6
            each_[my_random2()]=1
            return each_
        
        return each
    if (map_num == 3):
        each = condition_judge3(obs,is_act_continuous)
        if each  == None or  has_only_single_one(each)==0:
            each_=[0]*6
            each_[my_random2()]=1
            return each_
        
        return each
    #print(condition_judge3(obs,is_act_continuous))
    #return condition_judge3(obs,is_act_continuous)

def judge_player2(i):
    if i==0:
        return 'alpha'
    else:
        return 'beta'

def judge_player1(i):
    if i==0:
        return 'right'
    else:
        return 'left'

def has_only_single_one(each):
    return each.count(1) == 1

def my_random1():
        if random.random() < 0.90:
            return 1
        else:
            return 0

def my_random2():
    rand_num = random.random()
    if rand_num < 0.25:
        return 0
    elif rand_num < 0.5:
        return 1
    elif rand_num < 0.75:
        return 2
    else:
        return 3   
 
def get_pot_states(obs):
    # 用pot_states['cooking']来得到cooking的坐标
    pot_keys = {'empty','x_items','cooking','ready'}
    pot_states = {p_key:[] for p_key in pot_keys}
    for x in obs['objects']:
        if x['name'] == 'soup':
            if x['is_idle'] == True:
                pot_states['x_items'].append(x['position'])#有空位
            elif x['is_cooking'] == True:
                pot_states['cooking'].append(x['position'])
            elif x['is_ready'] == True:
                pot_states['ready'].append(x['position'])
    return pot_states

def parse_pot_states(pot_states):
    empty = []
    if len(pot_states['x_items'])+len(pot_states['cooking'])+len(pot_states['ready'])!=2:
        if (3,0) not in pot_states['x_items'] and (3,0) not in pot_states['cooking'] and (3,0) not in pot_states['ready']:
            empty.append((3,0))
        if (4,1) not in pot_states['x_items'] and (4,1) not in pot_states['cooking'] and (4,1) not in pot_states['ready']:
            empty.append((4,1))
    pot_states['empty'] = empty #空锅的位置
    #print(pot_states)
    return pot_states['empty'],pot_states['x_items'],pot_states['cooking'],pot_states['ready']
    """pot_x_items = []
    keys = ['1_items','2_items','3_items']
    for key,value in pot_states.items():
        for key in keys:
            pot_x_items.extend(value)
    return pot_states['empty'],pot_x_items,pot_states['cooking'],pot_states['ready']"""

def condition_judge1(obs, is_act_continuous):#credit.tjg
    each = []
    if judge_player1(obs['controlled_player_index']) == 'left':
        action = [0]*6
        #获取物品信息
        obj = obs['objects']
        #获取锅当前状态
        pot_states = get_pot_states(obs)
        pot_emp,pot_items,pot_cooking,pot_ready = parse_pot_states(pot_states)
        #获取玩家当前状态
        p1_state = obs['players'][1]
        p2_state = obs['players'][0]
        p1_pos = p1_state['position']
        p1_ori = p1_state['orientation']
        num_dish = 0
        global in_action,giving_onion
        if (2,1) not in onions_pos(obj) and in_action not in [2,3]:
            in_action = 1
            if p1_pos != (1,1):
                action[0] = 1
            else:
                if hold_onion(p1_state) == False:
                    if p1_ori != (-1,0):
                        action[3] = 1
                    else:
                        action[5] = 1
                else:
                    if p1_ori != (1,0):
                        action[2] = 1
                    else:
                        action[5] = 1
                        in_action = 0
            each = action
            return each
        if (2,2) not in onions_pos(obj) and in_action not in [1,3]:
            in_action = 2
            if p1_pos != (1,2):
                if p1_pos == (1,3):
                    action[0] = 1
                else:
                    action[1] = 1
            else:
                if hold_onion(p1_state) == False:
                    if p1_ori != (-1,0):
                        action[3] = 1
                    else:
                        action[5] = 1
                else:
                    if p1_ori != (1,0):
                        action[2] = 1
                    else:
                        action[5] = 1
                        in_action = 0
            each = action
            return each
        if (2,3) not in dishes_pos(obj) and in_action not in [1,2]:
            in_action = 3
            if p1_pos != (1,3):
                action[1] = 1
            else:
                if hold_dish(p1_state) == False:
                    if p1_ori != (-1,0):
                        action[3] = 1
                    else:
                        action[5] = 1
                else:
                    if p1_ori != (1,0):
                        action[2] = 1
                    else:
                        action[5] = 1
                        in_action = 0
            each =  action
            return each
        else:
            return [0,0,0,0,1,0]

    
    
    else:
        action = [0]*6
        #获取物品信息
        obj = obs['objects']
        #获取锅当前状态
        pot_states = get_pot_states(obs)
        pot_emp,pot_items,pot_cooking,pot_ready = parse_pot_states(pot_states)
        #获取玩家当前状态
        p1_state = obs['players'][1]
        p2_state = obs['players'][0]
        p1_pos = p1_state['position']
        p2_pos = p2_state['position']
        p2_ori = p2_state['orientation']
        global onions_p1,onions_p2
        if onions_p1 == 3 or onions_p2 == 3:
            giving_onion = 0
            if onions_p1 == 3:
                onions_p1 = 0
            if onions_p2 == 3:
                onions_p2 = 0
            action[5] = 1
            each = action
            return action
        if hold_soup(p2_state) == True: #如果拿着汤，去送汤
            if p2_pos!=(3,3):
                action[1] = 1
            else:
                if p2_ori != (0,1):
                    action[1] = 1
                else:
                    action[5] = 1
            each = action
            return each
        
        if hold_dish(p1_state) and (2,3) in dishes_pos(obj) and (2,2) not in onions_pos(obj) and (2,1) not in onions_pos(obj) and hold_dish(p2_state) == False and hold_onion(p2_state) == False:
            if p2_pos!=(3,3):
                action[1] = 1
            else:
                if p2_ori != (-1,0):
                    action[3] = 1
                else:
                    action[5] = 1
            each = action
            return each
        if hold_dish(p2_state) and (3,0) not in pot_ready and (4,1) not in pot_ready:
            if p2_pos != (3,3):
                action[1] = 1
            else:
                if p2_ori != (1,0):
                    action[2] = 1
                else:
                    action[5] = 1
            each = action
            return each
        
        if ((3,0) in pot_ready or (4,1) in pot_ready) and (hold_dish(p2_state)==False) and hold_onion(p2_state)==False:
            #如果有锅已经做好汤，但还没有拿盘子，就去拿盘子
            global get_dish_Y
            if p2_pos!=(3,1) and get_dish_Y == 1:
                action[0] = 1
            else:
                if (2,get_dish_Y) in dishes_pos(obj):
                    if p2_ori != (-1,0):
                        action[3] = 1
                    else:
                        action[5] = 1
                        get_dish_Y = 1
                elif (4,get_dish_Y) in dishes_pos(obj):
                    if p2_ori != (1,0):
                        action[2] = 1
                    else:
                        action[5] = 1
                        get_dish_Y = 1
                else:
                    if get_dish_Y != 3:
                        action[1] = 1
                        get_dish_Y+=1
                    else:
                        action[0] = 1
                        get_dish_Y -= 1
        elif ((3,0) in pot_ready or (4,1) in pot_ready) and (hold_dish(p2_state)==True):
            #如果有锅已经做好汤，且盘子已经拿好，就去拿汤
            if (3,0) in pot_ready:
                if p2_pos!=(3,1):
                    action[0] = 1
                else:
                    if p2_ori != (0,-1):
                        action[0] = 1
                    else:
                        action[5] = 1
            if(4,1) in pot_ready:
                if p2_pos!=(3,1):
                    action[0] = 1
                else:
                    if p2_ori != (1,0):
                        action[2] = 1
                    else:
                        action[5] = 1
        elif len(pot_cooking) == 2 and giving_onion == 0 and hold_onion(p2_state)==False: #如果两个锅都正在做汤,拿盘子去（3，1）等候
            if hold_dish(p2_state):
                if p2_pos != (3,1):
                    action[0] = 1
                else:
                    action[5] = 1
            else:
                if p2_pos != (3,3):
                    action[1] = 1
                else:
                    if p2_ori!=(-1,0):
                        action[3] = 1
                    else:
                        action[5] = 1
        else: #放洋葱到锅里并开火
            if p2_pos == (3,2) and (2,2) in onions_pos(obj) and hold_onion(p2_state)==False:
                if p2_ori != (-1,0):
                        action[3] = 1
                else:
                        action[5] = 1
                each = action
                return each
            if p2_pos == (3,1) and (2,2) in onions_pos(obj) and (2,1) not in onions_pos(obj) and hold_onion(p2_state)==False:
                if p1_pos != (1,1):
                    action[1] = 1
                elif hold_onion(p1_state)==False:
                    action[1] = 1
                else:
                    action[3] = 1
                each = action
                return each
            if hold_onion(p2_state) == False:
                global get_onion_Y
                if p2_pos != (3,1) and get_onion_Y==1:
                    action[0] = 1
                else:
                    if (2,get_onion_Y) in onions_pos(obj):
                        if p2_ori != (-1,0):
                            action[3] = 1
                        else:
                            action[5] = 1
                            get_onion_Y = 1
                    elif (4,get_onion_Y) in onions_pos(obj):
                        if p2_ori != (1,0):
                            action[2] = 1
                        else:
                            action[5] = 1
                            get_onion_Y = 1
                    else:
                        if get_onion_Y!=3:
                            action[1] = 1
                            get_onion_Y += 1
                        else:
                            action[0] = 1
                            get_onion_Y -= 1
            else:#若拿了洋葱，查看哪个锅缺洋葱
                if p2_pos != (3,1):
                    action[0] = 1
                else:
                    if (3,0) in pot_items or (3,0) in pot_emp:#如果（3，0）处的锅缺洋葱
                        giving_onion = 1
                        if p2_pos != (3,1):
                            action[0] = 1
                        else:
                            if p2_ori != (0,-1):
                                action[0] = 1
                            else:
                                action[5] = 1
                                onions_p1+=1
                    elif (4,1) in pot_items or (4,1) in pot_emp:
                        giving_onion = 2
                        if p2_pos != (3,1):
                            action[0] = 1
                        else:
                            if p2_ori != (1,0):
                                action[2] = 1
                            else:
                                action[5] = 1
                                onions_p2+=1
        if action == []:
            print('stay')
            action[4] = 1
        each = action
        return each
every_table2_dic = {
        (0,1): WEST,
        (0,2): WEST,
        (0,3): WEST,
        (1,0): NORTH,
        (1,4): SOUTH,
        (2,0): NORTH,
        (2,2): 0,
        (3,4): SOUTH,
        (4,2): EAST,
        (4,3): EAST
    }#direction = every_table3.get(coord)
every_table2_set = {
        (0,1),
        (0,2),
        (0,3),
        (1,0),
        (1,4),
        (2,0),
        (2,2),
        (3,4),
        (4,2),
        (4,3)
    }
table_stand2={ #到目标桌子的站位
        (0,1): (1,1),
        (0,2): (1,2),
        (0,3): (1,3),
        (1,0): (1,1),
        (1,4): (1,3),
        (2,0): (2,1),
        (3,4): (3,3),
        (4,2): (3,2),
        (4,3): (3,3),
        (2,2): ()
        
    }     
    
def action_to_go_to(target_position,now_position,another_agent_pos):
    #例如输入action_to_go_to('（1， 2）','（2， 3)'）
            target_x = target_position[0]
            target_y = target_position[1]
            now_x = now_position[0]
            now_y = now_position[1]
            each_=[0]*6
            
            if(now_x==target_x and now_y==target_y):
                each_[4]=1
                return each_
             
            path1 = []
            path2 = []
            every_grid=[(1,1),(2,1),(3,1),(3,2),(3,3),(2,3),(1,3),(1,2)]
            # target_position = '3,1'
            # now_position = '2,3'
            # 路径1: [(2, 3), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1)]
            # 路径2: [(2, 3), (3, 3), (3, 2), (3, 1)]
            index1=index2=0 
        
            for i, grid in enumerate(every_grid):
                if grid == target_position:
                    index1=i
            for j, grid in enumerate(every_grid):
                if grid == now_position:
                    index2=j
                

            if index1 > index2:#index1较小
                index1, index2 = index2, index1
                
            path1=every_grid[index1:index2+1]
            path2=every_grid[index2:8]+every_grid[0:index1+1]
            if path1[0]!=now_position:
                path1.reverse()
            if path2[0]!=now_position:
                path2.reverse()
                
            print(path1,path2)    
            def choose_action(path):
                    each_tmp=[0,0,0,0,0,0]
            
                    next_pos=path[1]
                    next_x = next_pos[0]
                    next_y = next_pos[1]
                    if now_x-next_x==1:
                        each_tmp[3]=1
                
                    if now_y-next_y==1:
                        each_tmp[0]=1
                    
                    if next_x-now_x==1:
                        each_tmp[2]=1
                
                    if next_y-now_y==1:
                        each_tmp[1]=1
                        
                    return each_tmp
                
            if another_agent_pos==target_position:#对方站在目标上，随机动一下
                if random.random()<0.5:
                    each_ = choose_action(path1)
                else:
                    each_ = choose_action(path2)
                        
            if another_agent_pos in path1:
                each_ = choose_action(path2)
            else:
                each_ = choose_action(path1)
                
            return each_
 
def find_nearest_coordinate(coord1, coordinate_list):
    #找出离给定坐标最近的坐标及其索引
    min_distance = float('inf')
    nearest_coordinate = None
    nearest_index = None

    for i, coord in enumerate(coordinate_list):
        distance = abs(coord[0] - coord1[0]) + abs(coord[1] - coord1[1])
        if distance < min_distance:
            min_distance = distance
            nearest_coordinate = coord
            nearest_index = i

    return nearest_coordinate

def table_filter2(obs,all_table_pos):
    onion_positions = []
    dish_positions = []

    for obj in obs['objects']:
        if obj['name'] == 'onion':
            onion_positions.append(obj['position'])
        elif obj['name'] == 'dish':
            dish_positions.append(obj['position'])
    onion_positions.append((0,3))
    onion_positions.append((1,4))
    dish_positions.append(((0,2)))
    onion_positions = set(onion_positions)
    dish_positions = set(dish_positions)
    empty_positions=all_table_pos-onion_positions-dish_positions
        
    return onion_positions, dish_positions, empty_positions   

def go2table2(now_pos,now_ori,table_pos,another_agent_pos):
    #前往目标桌子,调整方向,采取行动
    if table_pos==(2,2):
        if now_pos==(1,1):
            return right
        if now_pos==(3,1):
            return down
        if now_pos==(1,3):
            return right
        if now_pos==(3,3):
            return left
        if now_pos==(2,1):
            if now_ori!=SOUTH:
                return down
            return interact
        if now_pos==(3,2):
            if now_ori!=WEST:
                return left
            return interact
        if now_pos==(2,3):
            if now_ori!=NORTH:
                return up
            return interact
        if now_pos==(1,2):
            if now_ori!=EAST:
                return right
            return interact
    
    else:    
        stand_pos=table_stand2.get(table_pos)
        if(now_pos!=stand_pos):
            return action_to_go_to(stand_pos,now_pos,another_agent_pos)
        
        elif(now_ori!=every_table2_dic.get(table_pos)):
            return direction.get(every_table2_dic.get(table_pos))
        
        else:
            return interact
             
def condition_judge2(obs, is_act_continuous=False ):#credit.gyj
    pot_states = get_pot_states(obs)
    pot_emp,pot_items,pot_cooking,pot_ready = parse_pot_states(pot_states)
    p1_state = obs['players'][0]
    p2_state = obs['players'][1]
    p1_pos=obs['players'][0]['position']
    p2_pos=obs['players'][1]['position']
    p1_ori = p1_state['orientation']
    p2_ori = p2_state['orientation']
   
    pot_pos=(3,1)
    deliver_pos=(2,3)
    pot1=(3,0)
    pot2=(4,1)
    up=[1,0,0,0,0,0]
    down=[0,1,0,0,0,0]
    right=[0,0,1,0,0,0]
    left=[0,0,0,1,0,0]
    still=[0,0,0,0,1,0]
    interact=[0,0,0,0,0,1]
    
    #用于judge2
    onion_positions, dish_positions, empty_positions = table_filter2(obs,every_table2_set)             
    #蓝帽子是alpha            
    if judge_player2(obs['controlled_player_index']) == 'alpha':
        p1_state = obs['players'][0]
        p2_state = obs['players'][1]
        p1_pos=obs['players'][0]['position']
        p2_pos=obs['players'][1]['position']
        p1_ori = p1_state['orientation']
        p2_ori = p2_state['orientation']
    else:
        p1_state = obs['players'][1]
        p2_state = obs['players'][0]
        p1_pos=obs['players'][1]['position']
        p2_pos=obs['players'][0]['position']
        p1_ori = p1_state['orientation']
        p2_ori = p2_state['orientation']
        
    if my_random1()==0:
        print('random!!!!!!!!!')
        each_=[0]*6
        each_[my_random2()]=1
        return each_
    
    #如果手上有汤去交汤
    if hold_soup(p1_state):
        print('手上有汤去交汤')
        if p1_pos!=deliver_pos:
            return action_to_go_to(deliver_pos,p1_pos,p2_pos)
        elif p1_ori!=(0,1):
            return down
        else:
            return interact
        
    #有汤好了且手上有盘 去拿汤
    if (((pot1 in pot_ready) or (pot2 in pot_ready) )and (hold_dish(p1_state))):
        print('有汤好了且手上有盘 去拿汤')
        if p1_pos!=pot_pos:
            return action_to_go_to(pot_pos,p1_pos,p2_pos)
        elif pot1 in pot_ready:
            if p1_ori!=NORTH:
                return up
            return interact 
        elif pot2 in pot_ready:
            if p1_ori!=EAST:
                return right
            return interact 
        
  
      
    #如果两个锅正在煮  去拿盘子
    if  ((pot1 in pot_cooking) or( pot1 in pot_ready)) and ((pot2 in pot_cooking) or( pot2 in pot_ready)) and (hold_dish(p1_state)==0):
        if hold_onion(p1_state)==1:#拿着洋葱就去放下
            print('放下洋葱')
            target_table=find_nearest_coordinate(p1_pos, empty_positions)
            action = go2table2(p1_pos,p1_ori,target_table,p2_pos)
            return action
        print('去拿盘子')
        target_table=find_nearest_coordinate(p1_pos,dish_positions)
        action=go2table2(p1_pos,p1_ori,target_table,p2_pos)
        return action       
    

        
    #如果有煮好的  去拿盘子
    if  (( pot1 in pot_ready) or (pot2 in pot_ready) ) and (hold_dish(p1_state)==0):
        
        if hold_onion(p1_state)==1:#拿着洋葱就去放下
            print('放下洋葱')
            target_table=find_nearest_coordinate(p1_pos, empty_positions)
            action = go2table2(p1_pos,p1_ori,target_table,p2_pos)
            return action
        else:    
            print('在煮去拿盘子')
            target_table=find_nearest_coordinate(p1_pos,dish_positions)
            action=go2table2(p1_pos,p1_ori,target_table,p2_pos)
            return action
        
    #拿了盘子没有汤则放下盘子
    if hold_dish(p1_state) and len(pot_ready)==0:
        target_table=find_nearest_coordinate(p1_pos, empty_positions)
        action = go2table2(p1_pos,p1_ori,target_table,p2_pos)
        return action
        
    
        
    
  
    
     #如果有锅缺洋葱且player没有拿盘子
    if (pot1 not in pot_cooking) or (pot2 not in pot_cooking):
        if (ingredient_num(obs,pot1)==3) and (pot1 not in pot_cooking) and (pot1 not in pot_ready):#pot1三个洋葱没开火
            
            if hold_onion(p1_state) or hold_dish(p1_state):#把手上东西放下
                print('放下东西')
                target_table=find_nearest_coordinate(p1_pos,empty_positions)
                action=go2table2(p1_pos,p1_ori,target_table,p2_pos)
                return action
            
            print('去开火')
            if p1_pos!=pot_pos:
                return action_to_go_to(pot_pos,p1_pos,p2_pos)
            elif p1_ori==NORTH:
                return interact
            else:
                return up
            
        if (ingredient_num(obs,pot2)==3) and (pot2 not in pot_cooking) and (pot2 not in pot_ready):#pot2三个洋葱没开火
            
            if hold_onion(p1_state) or hold_dish(p1_state):#把手上东西放下
                print('放下东西')
                target_table=find_nearest_coordinate(p1_pos,empty_positions)
                action=go2table2(p1_pos,p1_ori,target_table,p2_pos)
                return action
            
            print('去开火')
            if p1_pos!=pot_pos:
                return action_to_go_to(pot_pos,p1_pos,p2_pos)
            elif p1_ori==EAST:
                return interact
            else:
                return right
        
        #不到三个洋葱
                
        if(hold_onion(p1_state)):#拿着洋葱就去放
            
            print('去放洋葱')
            if p1_pos!=pot_pos:
                return action_to_go_to(pot_pos,p1_pos,p2_pos)
            if ingredient_num(obs,pot2)==2:#pot2差一个就放pot2否则优先pot1
                if p1_ori==EAST:
                    return interact
                else:
                    return right
                
            elif pot1 not in pot_cooking:
                if p1_ori==NORTH:
                    return interact
                else:
                    return up
            elif pot2 not in pot_cooking:
                if p1_ori==EAST:
                    return interact
                else:
                    return right
        
            
        else: #没拿洋葱去拿
            print('去拿洋葱')
            target_table=find_nearest_coordinate(p1_pos,onion_positions)
            print('targettable=',target_table)
            action=go2table2(p1_pos,p1_ori,target_table,p2_pos)
            return action
    
    print('去（3,3）')   
    return action_to_go_to((3,3),p1_pos,p2_pos)
      
def table_filter3(obs,all_table_pos):
        onion_positions = []
        dish_positions = []

        for obj in obs['objects']:
            if obj['name'] == 'onion':
                onion_positions.append(obj['position'])
            elif obj['name'] == 'dish':
                dish_positions.append(obj['position'])
        onion_positions.append((0,1))
        onion_positions.append((4,1))
        dish_positions.append(((1,3)))
        onion_positions = set(onion_positions)
        dish_positions = set(dish_positions)
        empty_positions=all_table_pos-onion_positions-dish_positions
            
        return onion_positions, dish_positions, empty_positions

def go2table(now_pos,now_ori,table_pos,another_agent_pos):
    #前往目标桌子,调整方向,采取行动
    stand_pos=table_stand.get(table_pos)
    if(now_pos!=stand_pos):
        return find_action(stand_pos,now_pos,another_agent_pos)
    
    elif(now_ori!=every_table3_dic.get(table_pos)):
        return direction.get(every_table3_dic.get(table_pos))
    
    else:
        return interact
        
def find_action(target_position,now_position,another_agent_pos):
    target_x = target_position[0]
    target_y = target_position[1]
    now_x = now_position[0]
    now_y = now_position[1]
    each_=[0]*6
    if my_random1()==0:
        print('random!!!!!!!!!')
        each_[my_random2()]=1
        return each_
        
    if(now_x==target_x and now_y==target_y):
        each_[4]=1
        return each_
    
    every_grid=[(1,1),(2,1),(3,1),(3,2),(2,2),(1,2)]
    if(now_x==target_x and now_y==target_y):
        each_[4]=1
        return each_
    
    index1=index2=0 
    
    for i, grid in enumerate(every_grid):
        if grid == target_position:
            index1=i
    for j, grid in enumerate(every_grid):
        if grid == now_position:
            index2=j
        

    if index1 > index2:#index1较小
        index1, index2 = index2, index1
        
    path1=every_grid[index1:index2+1]
    path2=every_grid[index2:6]+every_grid[0:index1+1]
    if path1[0]!=now_position:
        path1.reverse()
    if path2[0]!=now_position:
        path2.reverse()
    #print(path1,path2)
    
    def choose_action(path):
        each_ = [0]*6
        if len(path)==1:
            each_[4]=1
        if len(path)==0:
            each_[4]=1
        else:
            next_pos=path[1]
            next_x = next_pos[0]
            next_y = next_pos[1]
            if now_x-next_x==1:
                each_[3]=1
            if now_y-next_y==1:
                each_[0]=1
            if next_x-now_x==1:
                each_[2]=1
            if next_y-now_y==1:
                each_[1]=1
    if another_agent_pos==target_position:#对方站在目标上，随机动一下
                if random.random()<0.5:
                    each_ = choose_action(path1)
                else:
                    each_ = choose_action(path2)
                
    if another_agent_pos in path1:
        choose_action(path2)
    else:
        choose_action(path1)
        
    return each_

every_table3_dic = {
    (0, 2): WEST,
    (1, 0): NORTH,
    (3, 0): NORTH,
    (4, 2): EAST,
    (2, 3): SOUTH,
    (0, 1): WEST,
    (4, 1): EAST,
    (1, 3): SOUTH
}#direction = every_table3.get(coord)
every_table3_set = {
    (0, 2),
    (1, 0),
    (3, 0),
    (4, 2),
    (2, 3),
    (0, 1),
    (4, 1),
    (1, 3)
}
table_stand={ 
    (0,1):(1,1),
    (1,0):(1,1),
    (0,2):(1,2),
    (1,3):(1,2),
    (2,3):(2,2),
    (3,0):(3,1),
    (4,1):(3,1),
    (4,2):(3,2)
    #到目标桌子的站位
}

Controller_Helper = {(1,1):{'i':[1,4],'a':[2,3]},
                    (1,2):{'i':[2,4],'a':[1,3]},
                    (2,1):{'i':[1],'a':[2,3,4]},
                    (2,2):{'i':[2],'a':[1,3,4]},
                    (3,1):{'i':[1,3],'a':[2,4]},
                    (3,2):{'i':[2,3],'a':[1,4]}
                    }# i: interactive a: accessible

 
# def condition_judge3(obs,is_act_continuous=False):#credit.gyj
        
    
#     pot_states = get_pot_states(obs)
#     pot_emp,pot_items,pot_cooking,pot_ready = parse_pot_states(pot_states)
    
    
#     pot_pos=(2,1)
#     pot=(2,0)
#     deliver_pos=(3,2)
    
#     onion_positions, dish_positions, empty_positions = table_filter3(obs,every_table3_set)
    

    
#     if judge_player2(obs['controlled_player_index']) == 'alpha':
#         p1_state = obs['players'][0]
#         p2_state = obs['players'][1]
#         p1_pos=obs['players'][0]['position']
#         p2_pos=obs['players'][1]['position']
#         p1_ori = p1_state['orientation']
#         p2_ori = p2_state['orientation']
#     else:
#         p1_state = obs['players'][1]
#         p2_state = obs['players'][0]
#         p1_pos=obs['players'][1]['position']
#         p2_pos=obs['players'][0]['position']
#         p1_ori = p1_state['orientation']
#         p2_ori = p2_state['orientation']
        
#     each_=[0]*6
#     if my_random1()==0:
#         print('random!!!!!!!!!')
#         each_[my_random2()]=1
#         return each_
#     #如果手上有汤去交汤
#     if hold_soup(p1_state):
#         print('手上有汤去交汤')
#         if p1_pos!=deliver_pos:
#             return find_action(deliver_pos,p1_pos,p2_pos)
#         elif p1_ori!=(0,1):
#             return down
#         else:
#             return interact
        
#     #有汤好了且手上有盘 去拿汤
#     if (((pot in pot_ready) or (pot in pot_cooking) )and (hold_dish(p1_state))):
#         print('有汤好了且手上有盘 去拿汤')
#         if p1_pos!=pot_pos:
#             return find_action(pot_pos,p1_pos,p2_pos)
#         elif p1_ori!=(0,-1):
#             return up
#         else:
#             return interact     
        
  
#     #如果正在煮 且没拿盘子 去拿盘子
#     if  ((pot in pot_cooking) or( pot in pot_ready)) and (hold_dish(p1_state)==0):
        
#         if hold_onion(p1_state)==1:#拿着洋葱就去放下
#             print('放下洋葱')
#             target_table=find_nearest_coordinate(p1_pos, empty_positions)
#             action = go2table(p1_pos,p1_ori,target_table,p2_pos)
#             return action
#         else:    
#             print('在煮去拿盘子')
#             target_table=find_nearest_coordinate(p1_pos,dish_positions)
#             action=go2table(p1_pos,p1_ori,target_table,p2_pos)
#             return action
        
      
#     #拿了盘子没有汤则放下盘子
#     if hold_dish(p1_state) and len(pot_ready)==0:
#         target_table=find_nearest_coordinate(p1_pos, empty_positions)
#         action = go2table(p1_pos,p1_ori,target_table,p2_pos)
#         return action
        
        
    
    
    
#     #如果有锅缺洋葱
#     if (pot not in pot_cooking):
#         if (ingredient_num(obs,pot)==3) and (pot not in pot_cooking):#三个洋葱没开火
            
#             if hold_onion(p1_state) or hold_dish(p1_state):#把手上东西放下
#                 print('放下东西')
#                 target_table=find_nearest_coordinate(p1_pos,empty_positions)
#                 action=go2table(p1_pos,p1_ori,target_table,p2_pos)
#                 return action
            
#             print('去开火')
#             if p1_pos!=pot_pos:
#                 return find_action(pot_pos,p1_pos,p2_pos)
#             elif p1_ori==(0,-1):
#                 return interact
#             else:
#                 return up
        
#         #不到三个洋葱
                
#         if(hold_onion(p1_state)):#拿着洋葱就去放
            
#             print('去放洋葱')
#             if p1_pos!=pot_pos:
#                 return find_action(pot_pos,p1_pos,p2_pos)
#             elif p1_ori==(0,-1):
#                 return interact
#             elif p1_ori!=(0,-1):
#                 return up
        
            
#         else: #没拿洋葱去拿
#             print('去拿洋葱')
#             target_table=find_nearest_coordinate(p1_pos,onion_positions)
#             action=go2table(p1_pos,p1_ori,target_table,p2_pos)
#             return action
    
#     print('去（3,2）')   
#     return find_action((3,2),p1_pos,p2_pos)
  

def condition_judge3(obs,is_act_continuous = False):#cr.tjg
    global Controller_Helper,Ori_Helper,Turn_Helper
    global o1_choose,o2_choose,pot_oni_num,is_action
    each = []
    action = [0,0,0,0,0,0]
    idx_s = obs['controlled_player_index'] # idx_self, idx_other
    if idx_s:
        idx_o = 0
    else:
        idx_o = 1
    #获取物品信息
    obj = obs['objects']
    pot_states = get_pot(obs)
    #获取玩家信息
    s_state = obs['players'][idx_s]
    o_state = obs['players'][idx_o]
    s_pos,s_ori,s_held = get_player_info(s_state)
    o_pos,o_ori,o_held = get_player_info(o_state)
    #获取物品位置
    dishPos = dishes_pos(obj)
    onionPos = onions_pos(obj)
    #处理o1,o2
    if o_pos == Oni1 and o_held != None and o_held['name'] == 'onion':
        o1_choose = o1_choose+1
    if o_pos == Oni2 and o_held != None and o_held['name'] == 'onion':
        o2_choose = o2_choose+1
    #处理pot_oni_num
    if pot_states['cooking'] + pot_states['ready']:
        pot_oni_num = 0
    else:
        pot_oni_num = get_pot_oni(obj)
    player_oni_num = 0 
    if o_held!=None and o_held['name'] == 'onion':
        player_oni_num = 1
    #是否相邻
    next_flag = is_next(s_pos,o_pos)
    #若状态合适，直接interact
    #点火，取洋葱，放洋葱，取盘子，放盘子，取汤，放汤
    if is_proper_state(s_pos,s_ori,s_held,pot_states,pot_oni_num,o_pos):
        action[5] = 1
        each = action
        return each
    #若拿汤
    if s_held != None and s_held['name'] == 'soup':
        #alpha控制概率
        alpha_1 = 2
        if next_flag:
            alpha_1 = 3
        if s_pos == Sub and s_ori != Ori_Helper[2]:
            action[1] = 1
            each = action
            return each
        #去s处
        if random_num() > alpha_1:
            each = find_path(Sub,s_pos)
        #随机走
        else:
            each = shuffle(s_pos)
        return each
    #若拿洋葱
    if s_held != None and s_held['name'] =='onion':
        is_action = 0
        if pot_states['idle']+pot_states['empty'] and pot_oni_num!=3:
            alpha_2 = 2
            if o_held != None and o_held['name'] == 'onion':
                if o_pos == Oni2 and s_pos == Oni1 and s_ori[0] + o_ori[0] == 0:
                    return shuffle(s_pos)
                elif o_pos == Oni1 and s_pos == Oni2 and s_ori[0] + o_ori[0] == 0:
                    return shuffle(s_pos)
                alpha_2 = 4
            if s_pos == Pot and s_ori != Ori_Helper[1]:
                action[0] = 1
                each = action
                return each
            if random_num() > alpha_2:
                each = find_path(Pot,s_pos)
            else:
                each = shuffle(s_pos)
            return each
        else:
            if o_held!=None and o_held['name'] == 'dish':
                alpha_3 = 2
                if next_flag:
                    alpha_3 = 3
                if random_num() > alpha_3:
                    action[5] = 1
                    each = action
                else:
                    each = shuffle(s_pos)
                return each
            else:
                #return one list and turn to it
                idle_ori = check_border(dishPos,onionPos,s_pos)
                if idle_ori != []:
                    if s_ori in idle_ori:
                        action[5] = 1
                        each = action
                    else:
                        turn_ori = idle_ori[random.randint(0,len(idle_ori)-1)]
                        turn = Turn_Helper[turn_ori]
                        action[turn] = 1
                        each = action
                else:
                    each = shuffle(s_pos)
                return each
    #若拿盘子
    if s_held != None and s_held['name'] == 'dish':
        if pot_states['idle']+pot_states['empty']:
            #return one list and turn to it
            idle_ori = check_border(dishPos,onionPos,s_pos)
            if idle_ori != []:
                if s_ori in idle_ori:
                    action[5] = 1
                    each = action
                    return each
                else:
                    turn_ori = idle_ori[random.randint(0,len(idle_ori)-1)]
                    turn = Turn_Helper[turn_ori]
                    action[turn] = 1
                    each = action
                    return each
            else:
                each = shuffle(s_pos)
                return each
        else:
            if o_held!= None and o_held['name'] == 'dish':
                #if o_pos == (2,1):
                idle_ori = check_border(dishPos,onionPos,s_pos)
                if idle_ori != []:
                    if s_ori in idle_ori:
                        action[5] = 1
                        each = action
                        return each
                    else:
                        turn_ori = idle_ori[random.randint(0,len(idle_ori)-1)]
                        turn = Turn_Helper[turn_ori]
                        action[turn] = 1
                        each = action
                        return each
                else:
                    each = shuffle(s_pos)
                    return each
                """else:
                    #偷懒了
                    alpha_4 = 3
                    if random_num() > alpha_4:
                        action[5] = 1
                        each = action
                    else:
                        each = shuffle(s_pos)"""
            else:
                alpha_5 = 2
                if next_flag:
                    alpha_5 = 3
                if s_pos == Pot and s_ori != Ori_Helper[1]:
                    action[0] = 1
                    each = action
                    return each 
                if random_num() > alpha_5:
                    #choose pot and find path to pot
                    each = find_path(Pot,s_pos)
                    return each
                else:
                    each = shuffle(s_pos)
                    return each
    #若空手
    if s_held == None:
        if pot_states['idle'] == 1 and pot_oni_num == 3: #去点火
            if o_pos != Pot:
                if s_pos == Pot and s_ori != Ori_Helper[1]:
                    action[0] = 1
                    each = action 
                else:
                    alpha_9 = 2
                    if next_flag:
                        alpha_9 = 4
                    if random_num() > alpha_9:
                        each = find_path(Pot,s_pos)
                    else:
                        each = shuffle(s_pos)
                return each
        if pot_states['idle']+pot_states['empty'] and pot_oni_num != 3:
            #如果朝向处恰好有洋葱，直接拿起
            x = s_pos[0] + s_ori[0]
            y = s_pos[1] + s_ori[1]
            if (x,y) in onionPos:
                action[5] = 1
                each = action
                return action
            alpha_6 = 3
            if s_pos == Oni1 and s_ori!=Ori_Helper[4]:
                action[3] = 1
                each = action
                return each
            if s_pos == Oni2 and s_ori!=Ori_Helper[3]:
                action[2] = 1
                each = action 
                return each
            if random_num() > alpha_6:
                if is_action == 0:
                    choice = make_choice(s_pos,o_pos)
                    is_action = choice
                if is_action == 1:
                    each = find_path(Oni1,s_pos)
                if is_action == 2:
                    each = find_path(Oni2,s_pos)
                #choose onion and find path to onion
            else:
                each = shuffle(s_pos)
            print(each)
            return each
        else:
            is_action = 0
            if o_held == None or (o_held!=None and o_held['name'] == 'onion'):
                alpha_7 = 3
                x = s_pos[0] + s_ori[0]
                y = s_pos[1] + s_ori[1]
                if (x,y) in dishPos:
                    action[5] = 1
                    each = action
                    return action
                if s_pos == Dish and s_ori!=Ori_Helper[2]:
                    action[1] = 1
                    each = action
                    return each
                if random_num() > alpha_7:
                    #find path to dish
                    each = find_path(Dish,s_pos)
                    return each
                else:
                    each = shuffle(s_pos)
                    return each
            elif o_held['name'] == 'onion':
                alpha_7 = 3
                x = s_pos[0] + s_ori[0]
                y = s_pos[1] + s_ori[1]
                if (x,y) in dishPos:
                    action[5] = 1
                    each = action
                    return action
                if s_pos == Dish and s_ori!=Ori_Helper[2]:
                    action[1] = 1
                    each = action
                    return each
                if random_num() > alpha_7:
                    #find path to dish
                    each = find_path(Dish,s_pos)
                    return each
                else:
                    each = shuffle(s_pos)
                    return each
            else:
                if s_pos == Oni1 and s_ori!=Ori_Helper[4]:
                    action[3] = 1
                    each = action
                    return each
                if s_pos == Oni2 and s_ori!=Ori_Helper[3]:
                    action[2] = 1
                    each = action 
                    return each
                alpha_8 = 3
                if random_num() > alpha_8:
                    #choose oni and find path to oni
                    each = find_path(Oni2,s_pos)
                else:
                    each = shuffle(s_pos)
                return each

def get_pot(obs):
    pot_keys = {'empty','idle','cooking','ready'}
    pot_state = {key:0 for key in pot_keys}
    pot_state['empty'] = 1
    for x in obs['objects']:
        if x['name'] == 'soup':
            pot_state['empty'] = 0
            if x['is_idle'] == True:
                pot_state['idle'] = 1
            elif x['is_cooking'] == True:
                pot_state['cooking'] = 1
            elif x['is_ready'] == True:
                pot_state['ready']  = 1
            break
    return pot_state

def get_player_info(state):
    return state['position'],state['orientation'],state['held_object']

def dishes_pos(obj):
    position = []
    if obj == []:
        return position
    for x in obj:
        if x['name'] == 'dish':
            position.append(x['position'])
    return position

def onions_pos(obj):
    position = []
    if obj == []:
        return position
    for x in obj:
        if x['name'] == 'onion':
            position.append(x['position'])
    return position

def is_proper_state(s_pos,s_ori,s_held,pot_states,pot_oni_num,o_pos):
    if s_held == None:
        if s_pos == Oni1 and s_ori == Ori_Helper[4] and pot_states['ready']+pot_states['cooking'] == 0 and pot_oni_num!=3:
            return True
        if s_pos == Oni2 and s_ori == Ori_Helper[3] and pot_states['ready']+pot_states['cooking'] == 0 and pot_oni_num!=3:
            return True
        if s_pos == Oni2 and s_ori == Ori_Helper[3] and pot_states['cooking'] + pot_states['ready'] == 1 and o_pos == Pot:
            return True
        if s_pos == Oni1 and s_ori == Ori_Helper[4] and pot_states['cooking'] + pot_states['ready'] == 1 and o_pos == Pot:
            return True
        if s_pos == Dish and s_ori == Ori_Helper[2] and pot_states['empty']+pot_states['idle']==0:
            return True
        if s_pos == Pot and pot_oni_num == 3 and s_ori == Ori_Helper[1]:
            pot_oni_num = 0
            return True
    else:
        if s_held['name'] == 'dish' and pot_states['ready']+pot_states['cooking'] == 1:
            if s_pos == Pot and s_ori == Ori_Helper[1]:
                return True
        if s_held['name'] == 'onion' and pot_states['empty'] + pot_states['idle'] == 1 and pot_oni_num < 3:
            if s_pos == Pot and s_ori == Ori_Helper[1]:
                return True
        if s_held['name'] == 'soup':
            if s_pos == Sub and s_ori == Ori_Helper[2]:
                return True
    return False

def random_num():
    return random.randint(1,10)

def find_path(end,start):
    action = [0]*6
    actionX = 0
    actionY = 0
    if end[0]<start[0]:
        actionX = 3
    elif end[0]>start[0]:
        actionX = 2
    if end[1]<start[1]:
        actionY = 0
    elif end[1]>start[1]:
        actionY = 1
    if actionX == 0:
        action[actionY] = 1
        return action
    if actionY == 0:
        action[actionX] = 1
        return action
    if random.randint(0,1) == 0:
        action[actionY] = 1
        return action
    else:
        action[actionX] = 1
        return action

def shuffle(pos):
    global Controller_Helper
    action = [0]*6
    prob = Controller_Helper[pos]['a']
    if len(prob) == 2:
        action[prob[random.randint(0,1)]-1] = 1
        return action 
    action[prob[random.randint(0,2)]-1] = 1
    return action 

def check_border(dishPos,onionPos,pos):
    global Controller_Helper,Ori_Helper
    final_ori = []
    terrain = [(3,3),(0,1),(4,1),(2,0),(1,3)]
    prob = Controller_Helper[pos]['i']
    for ori in prob:
        x = Ori_Helper[ori][0] + pos[0]
        y = Ori_Helper[ori][1] + pos[1]
        if (x,y) not in terrain and (x,y) not in onionPos and (x,y) not in dishPos:
            final_ori.append(Ori_Helper[ori])
    return final_ori

def make_choice(s_pos,o_pos):
    if s_pos[0] == Oni1[0]:
        return 1
    if s_pos[0] == Oni2[0]:
        return 2
    if o_pos[0] == Oni1[0]:
        return 2
    if o_pos[0] == Oni2[0]:
        return 1
    if o1_choose > o2_choose:
        return 2
    if o1_choose < o2_choose:
        return 1
    return random.randint(1,2)

def get_pot_oni(obj):
    for x in obj:
        if x['name'] == 'soup':
            return len(x['_ingredients'])
    return 0

def is_next(s_pos,o_pos):
    if s_pos[0] == o_pos[0]:
        if abs(s_pos[1]-o_pos[1]==1):
            return True 
    if s_pos[1] == o_pos[1]:
        if abs(s_pos[0]-o_pos[0]==1):
            return True










    































    





















     

        
       
    #     #如果锅2缺洋葱且player没有拿盘子
    #     if(pot not in pot_cooking):
    #         #（4,1）锅不在烧
    #         if (ingredient_num(obs,pot)==3) and (pot not in pot_cooking):#三个洋葱没开火
    #             print('去开火')
    #             if p2_pos!=pot_pos:
    #                 return find_action(pot_pos,p2_pos,p1_pos)
    #             elif p2_ori!=(0,-1):
    #                 return up
    #             else:
    #                 return interact
              
    #         #不到三个洋葱
                    
    #         if(hold_onion(p2_state)):#拿着洋葱就去放
                
    #             print('去放洋葱')
    #             if p2_pos!=pot_pos:
    #                 return find_action(pot_pos,p2_pos,p1_pos)
    #             elif p2_ori==(0,-1):
    #                 return interact
               
    #             return up
               
                
    #         elif p2_pos!=onion_pos2: #没拿洋葱去拿
    #             print('去拿洋葱')
    #             return find_action(onion_pos2,p2_pos,p1_pos)
    #         else:
    #             print('拿洋葱')
    #             if p2_ori!=(1,0):
    #                 return right
                
    #             return interact
    #     print('不动')  
    #     return still        
                     
def is_holding(p_state):
    if hold_dish(p_state) and hold_soup(p_state) and hold_onion(p_state):
        return 1
    else:
        return 0

def hold_dish(obs_ID):  #player是否拿盘子
    if obs_ID['held_object'] == None:
        return False
    else:
        if obs_ID['held_object']['name'] == 'dish':
            return True
        else:
            return False
        
def hold_soup(obs_ID): #player是否拿汤
    if obs_ID['held_object'] == None:
        return False
    else:
        if obs_ID['held_object']['name'] == 'soup':
            return True
        else:
            return False

def hold_onion(obs_ID): #player是否拿洋葱
    if obs_ID['held_object'] == None:
        return False
    else:
        if obs_ID['held_object']['name'] == 'onion':
            return True
        else:
            return False

def dishes_pos(obj):
    position = []
    if obj == []:
        return position
    for x in obj: 
        if x['name'] == 'dish':
            position.append(x['position'])  
    return position

def onions_pos(obj):
    position = []
    if obj == []:
        return position
    for x in obj: 
        if x['name'] == 'onion':
            position.append(x['position'])  
    return position
 
def ingredient_num(obs, position):#ingredient_num(obs,(3,0))返回的是（3,0）锅有几个洋葱
    for obj in obs['objects']:
        if obj['name'] == 'soup' and obj['position'] == position:
            return obj['_ingredients'].count({'name': 'onion', 'position': position})
    return 0  # 如果没有找到匹配的 soup 对象，则返回 0




def pp():
    pass
    # import random
    # import math
    # """
    # XXPXX
    # O   O
    # X   X
    # XDXSX
    # """
    # NORTH = (0, -1)
    # SOUTH = (0, 1)
    # EAST = (1, 0)
    # WEST = (-1, 0)

    # Ori_Helper = {1:NORTH,2:SOUTH,3:EAST,4:WEST}
    # Turn_Helper = {NORTH:0,SOUTH:1,EAST:2,WEST:3}
    # # i: interactive a: accessible
    # Controller_Helper = {(1,1):{'i':[1,4],'a':[2,3]},
    #                     (1,2):{'i':[2,4],'a':[1,3]},
    #                     (2,1):{'i':[1],'a':[2,3,4]},
    #                     (2,2):{'i':[2],'a':[1,3,4]},
    #                     (3,1):{'i':[1,3],'a':[2,4]},
    #                     (3,2):{'i':[2,3],'a':[1,4]}
    #                     }

    # Sub = (3,2)
    # Oni1 = (1,1)
    # Oni2 = (3,1)
    # Dish = (1,2)
    # Pot = (2,1)

    # pot_oni_num=0

    # o1_choose = 0
    # o2_choose = 0
    # is_action = 0

def other3():
    pass
    # def condition_judge3(obs,is_act_continuous = False):
    #     global Controller_Helper,Ori_Helper,Turn_Helper
    #     global o1_choose,o2_choose,pot_oni_num,is_action
    #     each = []
    #     action = [0]*6
    #     idx_s = obs['controlled_player_index'] # idx_self, idx_other
    #     if idx_s:
    #         idx_o = 0
    #     else:
    #         idx_o = 1
    #     #获取物品信息
    #     obj = obs['objects']
    #     pot_states = get_pot(obs)
    #     #获取玩家信息
    #     s_state = obs['players'][idx_s]
    #     o_state = obs['players'][idx_o]
    #     s_pos,s_ori,s_held = get_player_info(s_state)
    #     o_pos,o_ori,o_held = get_player_info(o_state)
    #     #获取物品位置
    #     dishPos = dishes_pos(obj)
    #     onionPos = onions_pos(obj)
    #     #处理o1,o2
    #     if o_pos == Oni1 and o_held != None and o_held['name'] == 'onion':
    #         o1_choose = o1_choose+1
    #     if o_pos == Oni2 and o_held != None and o_held['name'] == 'onion':
    #         o2_choose = o2_choose+1
    #     #处理pot_oni_num
    #     if pot_states['cooking'] + pot_states['ready']:
    #         pot_oni_num = 0
    #     else:
    #         pot_oni_num = get_pot_oni(obj)
    #     player_oni_num = 0 
    #     if o_held!=None and o_held['name'] == 'onion':
    #         player_oni_num = 1
    #     #是否相邻
    #     next_flag = is_next(s_pos,o_pos)
    #     #若状态合适，直接interact
    #     #点火，取洋葱，放洋葱，取盘子，放盘子，取汤，放汤
    #     if is_proper_state(s_pos,s_ori,s_held,pot_states,pot_oni_num,o_pos):
    #         action[5] = 1
    #         each = action
    #         return each
    #     #若拿汤
    #     if s_held != None and s_held['name'] == 'soup':
    #         #alpha控制概率
    #         alpha_1 = 2
    #         if next_flag:
    #             alpha_1 = 3
    #         if s_pos == Sub and s_ori != Ori_Helper[2]:
    #             action[1] = 1
    #             each = action
    #             return each
    #         #去s处
    #         if random_num() > alpha_1:
    #             each = find_path(Sub,s_pos)
    #         #随机走
    #         else:
    #             each = shuffle(s_pos)
    #         return each
    #     #若拿洋葱
    #     if s_held != None and s_held['name'] =='onion':
    #         is_action = 0
    #         if pot_states['idle']+pot_states['empty'] and pot_oni_num!=3:
    #             alpha_2 = 2
    #             if o_held != None and o_held['name'] == 'onion':
    #                 if o_pos == Oni2 and s_pos == Oni1 and s_ori[0] + o_ori[0] == 0:
    #                     return shuffle(s_pos)
    #                 elif o_pos == Oni1 and s_pos == Oni2 and s_ori[0] + o_ori[0] == 0:
    #                     return shuffle(s_pos)
    #                 alpha_2 = 4
    #             if s_pos == Pot and s_ori != Ori_Helper[1]:
    #                 action[0] = 1
    #                 each = action
    #                 return each
    #             if random_num() > alpha_2:
    #                 each = find_path(Pot,s_pos)
    #             else:
    #                 each = shuffle(s_pos)
    #             return each
    #         else:
    #             if o_held!=None and o_held['name'] == 'dish':
    #                 alpha_3 = 2
    #                 if next_flag:
    #                     alpha_3 = 3
    #                 if random_num() > alpha_3:
    #                     action[5] = 1
    #                     each = action
    #                 else:
    #                     each = shuffle(s_pos)
    #                 return each
    #             else:
    #                 #return one list and turn to it
    #                 idle_ori = check_border(dishPos,onionPos,s_pos)
    #                 if idle_ori != []:
    #                     if s_ori in idle_ori:
    #                         action[5] = 1
    #                         each = action
    #                     else:
    #                         turn_ori = idle_ori[random.randint(0,len(idle_ori)-1)]
    #                         turn = Turn_Helper[turn_ori]
    #                         action[turn] = 1
    #                         each = action
    #                 else:
    #                     each = shuffle(s_pos)
    #                 return each
    #     #若拿盘子
    #     if s_held != None and s_held['name'] == 'dish':
    #         if pot_states['idle']+pot_states['empty']:
    #             #return one list and turn to it
    #             idle_ori = check_border(dishPos,onionPos,s_pos)
    #             if idle_ori != []:
    #                 if s_ori in idle_ori:
    #                     action[5] = 1
    #                     each = action
    #                     return each
    #                 else:
    #                     turn_ori = idle_ori[random.randint(0,len(idle_ori)-1)]
    #                     turn = Turn_Helper[turn_ori]
    #                     action[turn] = 1
    #                     each = action
    #                     return each
    #             else:
    #                 each = shuffle(s_pos)
    #                 return each
    #         else:
    #             if o_held!= None and o_held['name'] == 'dish':
    #                 #if o_pos == (2,1):
    #                 idle_ori = check_border(dishPos,onionPos,s_pos)
    #                 if idle_ori != []:
    #                     if s_ori in idle_ori:
    #                         action[5] = 1
    #                         each = action
    #                         return each
    #                     else:
    #                         turn_ori = idle_ori[random.randint(0,len(idle_ori)-1)]
    #                         turn = Turn_Helper[turn_ori]
    #                         action[turn] = 1
    #                         each = action
    #                         return each
    #                 else:
    #                     each = shuffle(s_pos)
    #                     return each
    #                 """else:
    #                     #偷懒了
    #                     alpha_4 = 3
    #                     if random_num() > alpha_4:
    #                         action[5] = 1
    #                         each = action
    #                     else:
    #                         each = shuffle(s_pos)"""
    #             else:
    #                 alpha_5 = 2
    #                 if next_flag:
    #                     alpha_5 = 3
    #                 if s_pos == Pot and s_ori != Ori_Helper[1]:
    #                     action[0] = 1
    #                     each = action
    #                     return each 
    #                 if random_num() > alpha_5:
    #                     #choose pot and find path to pot
    #                     each = find_path(Pot,s_pos)
    #                     return each
    #                 else:
    #                     each = shuffle(s_pos)
    #                     return each
    #     #若空手
    #     if s_held == None:
    #         if pot_states['idle'] == 1 and pot_oni_num == 3: #去点火
    #             if o_pos != Pot:
    #                 if s_pos == Pot and s_ori != Ori_Helper[1]:
    #                     action[0] = 1
    #                     each = action 
    #                 else:
    #                     alpha_9 = 2
    #                     if next_flag:
    #                         alpha_9 = 4
    #                     if random_num() > alpha_9:
    #                         each = find_path(Pot,s_pos)
    #                     else:
    #                         each = shuffle(s_pos)
    #                 return each
    #         if pot_states['idle']+pot_states['empty'] and pot_oni_num != 3:
    #             #如果朝向处恰好有洋葱，直接拿起
    #             x = s_pos[0] + s_ori[0]
    #             y = s_pos[1] + s_ori[1]
    #             if (x,y) in onionPos:
    #                 action[5] = 1
    #                 each = action
    #                 return action
    #             alpha_6 = 3
    #             if s_pos == Oni1 and s_ori!=Ori_Helper[4]:
    #                 action[3] = 1
    #                 each = action
    #                 return each
    #             if s_pos == Oni2 and s_ori!=Ori_Helper[3]:
    #                 action[2] = 1
    #                 each = action 
    #                 return each
    #             if random_num() > alpha_6:
    #                 if is_action == 0:
    #                     choice = make_choice(s_pos,o_pos)
    #                     is_action = choice
    #                 if is_action == 1:
    #                     each = find_path(Oni1,s_pos)
    #                 if is_action == 2:
    #                     each = find_path(Oni2,s_pos)
    #                 #choose onion and find path to onion
    #             else:
    #                 each = shuffle(s_pos)
    #             print(each)
    #             return each
    #         else:
    #             is_action = 0
    #             if o_held == None or (o_held!=None and o_held['name'] == 'onion'):
    #                 alpha_7 = 3
    #                 x = s_pos[0] + s_ori[0]
    #                 y = s_pos[1] + s_ori[1]
    #                 if (x,y) in dishPos:
    #                     action[5] = 1
    #                     each = action
    #                     return action
    #                 if s_pos == Dish and s_ori!=Ori_Helper[2]:
    #                     action[1] = 1
    #                     each = action
    #                     return each
    #                 if random_num() > alpha_7:
    #                     #find path to dish
    #                     each = find_path(Dish,s_pos)
    #                     return each
    #                 else:
    #                     each = shuffle(s_pos)
    #                     return each
    #             elif o_held['name'] == 'onion':
    #                 alpha_7 = 3
    #                 x = s_pos[0] + s_ori[0]
    #                 y = s_pos[1] + s_ori[1]
    #                 if (x,y) in dishPos:
    #                     action[5] = 1
    #                     each = action
    #                     return action
    #                 if s_pos == Dish and s_ori!=Ori_Helper[2]:
    #                     action[1] = 1
    #                     each = action
    #                     return each
    #                 if random_num() > alpha_7:
    #                     #find path to dish
    #                     each = find_path(Dish,s_pos)
    #                     return each
    #                 else:
    #                     each = shuffle(s_pos)
    #                     return each
    #             else:
    #                 if s_pos == Oni1 and s_ori!=Ori_Helper[4]:
    #                     action[3] = 1
    #                     each = action
    #                     return each
    #                 if s_pos == Oni2 and s_ori!=Ori_Helper[3]:
    #                     action[2] = 1
    #                     each = action 
    #                     return each
    #                 alpha_8 = 3
    #                 if random_num() > alpha_8:
    #                     #choose oni and find path to oni
    #                     each = find_path(Oni2,s_pos)
    #                 else:
    #                     each = shuffle(s_pos)
    #                 return each
