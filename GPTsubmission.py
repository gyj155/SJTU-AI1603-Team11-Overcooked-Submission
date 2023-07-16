import openai
openai.api_key = "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"
map_num=0
def my_controller(obs, action_space, is_act_continuous=False):
        agent_action = []
        action_ = sample_single_dim(obs,action_space, is_act_continuous)
        agent_action.append(action_)
        return agent_action


def sample_single_dim(obs,action_space_list_each, is_act_continuous):
    
    def get_pot_states(obs):
        pot_keys = {'empty','x_items','cooking','ready'}
        pot_states = {p_key:[] for p_key in pot_keys}
        for x in obs['objects']:
            if x['name'] == 'soup':
                if x['is_idle'] == True:
                    pot_states['x_items'].append(x['position'])
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
        pot_states['empty'] = empty
      
        return pot_states['empty'],pot_states['x_items'],pot_states['cooking'],pot_states['ready']
        
    def hold_dish(obs_ID): 
        if obs_ID['held_object'] == None:
            return False
        else:
            if obs_ID['held_object']['name'] == 'dish':
                return True
            else:
                return False
            
    def hold_soup(obs_ID):
        if obs_ID['held_object'] == None:
            return False
        else:
            if obs_ID['held_object']['name'] == 'soup':
                return True
            else:
                return False

    def hold_onion(obs_ID):
        if obs_ID['held_object'] == None:
            return False
        else:
            if obs_ID['held_object']['name'] == 'onion':
                return True
            else:
                return False
    pot_states = get_pot_states(obs)
    pot_emp,pot_items,pot_cooking,pot_ready = parse_pot_states(pot_states)
    p1_state = obs['players'][0]
    p1_pos=obs['players'][0]['position']
    p1_ori = p1_state['orientation']
    
    def get_chatgpt_decision():
        prompt1="现在由你来操控《分手厨房》游戏中两个角色其中的的一个角色，你可以选择六种活动：向上、向下、向左、向右、不动、互动；游戏机制：两位角色可以站立的坐标是（1,1）（1,2）（1,3）（2,1）（2,3）（3,1)  (3,2) (3,3)八块方格，中间（2,2）是不可以站立的桌子，每个玩家有一个朝向，可能朝向上、下、左、右；两口锅的位置是（0,3）和（1,4），角色只要站在（1,3）且面朝相应的锅就可以对这口锅进行操作。站在（3,1）选择”互动“可以拿起洋葱，站在（1,3）面向相应的锅选择”互动”可以把洋葱放进锅内，当锅内有三个洋葱时选择“互动”可以使锅开始烧汤；站在（2,1）朝向左选择“互动”可以拿起盘子，锅好了以后拿着盘子站在（1,3）面向相应的锅选择“互动”就可以取出汤，端着汤来到（3,3）朝向下选择“互动”就可以交出汤，得到奖励分。你的目标就是以最高效的方式送出尽可能多的汤。记住你一次只能拿着一件物品。下面是当前的地图状态："
        prompt2="你的位置是"+str(p1_pos)+"你的朝向是"+str(p1_ori)+"空着的锅是"+str(pot_emp)+"锅内有洋葱的是"+str(pot_items)+"正在煮的锅是"+str(pot_cooking)+"已经煮好的锅是"+str(pot_ready)+";"
        prompt3="你没有拿着洋葱" if hold_onion(p1_state)==0 else "你拿着洋葱"
        prompt4="你没有拿着盘子" if hold_dish(p1_state)==0 else "你拿着盘子"
        prompt5="你没有拿着汤" if hold_soup(p1_state)==0 else "你拿着汤"
        prompt6="现在请你根据已有信息做出最合理的行动，只输出\"向上、向下、向左、向右、不动、互动\"这六个词中的一个,别的什么都不要输出"
        # 调用ChatGPT API，传递游戏状态获取ChatGPT的决策
        response = openai.Completion.create(
            engine="text-davinci-003",
            
            prompt = prompt1+prompt2+prompt3+prompt4+prompt5+prompt6,
            max_tokens=1000
        )
        chatgpt_decision = response['choices'][0]['text']
        return chatgpt_decision
    
    each = []
    each = [0] * 6
    response =get_chatgpt_decision()
    int_action = 4
    if "向上" in response:
        int_action=0

    if "向下" in response:
        int_action=1

    if "向右" in response:
        int_action=2
        
    if "向左" in response:
        int_action=3
        
    if "不动" in response:
        int_action=4
        
    if "互动" in response:
        int_action=5

    each[int_action]=1
    print (each)
    return each



