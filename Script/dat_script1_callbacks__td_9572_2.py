if 'active_words' not in globals():
    global active_words
    active_words = {}

def onCook(scriptOp):
    import time
    global active_words
    
    # 创建text operators的列表
    text_ops = [op(f'text{i}') for i in range(1, 11)]  # text1 到 text10
    
    words_positions = [
        # 第一象限（右上，x正y正）
        {"word": "happy", "x": 0.8, "y": 0.7},
        {"word": "joy", "x": 0.5, "y": 0.9},
        {"word": "love", "x": 0.3, "y": 0.6},
        {"word": "smile", "x": 0.7, "y": 0.4},
        
        # 第二象限（左上，x负y正）
        {"word": "peace", "x": -0.6, "y": 0.8},
        {"word": "dream", "x": -0.3, "y": 0.5},
        {"word": "hope", "x": -0.8, "y": 0.7},
        {"word": "gentle", "x": -0.4, "y": 0.3},
        
        # 第三象限（左下，x负y负）
        {"word": "quiet", "x": -0.7, "y": -0.6},
        {"word": "calm", "x": -0.4, "y": -0.8},
        {"word": "rest", "x": -0.2, "y": -0.5},
        {"word": "slow", "x": -0.5, "y": -0.3},
        
        # 第四象限（右下，x正y负）
        {"word": "dance", "x": 0.6, "y": -0.7},
        {"word": "play", "x": 0.3, "y": -0.4},
        {"word": "jump", "x": 0.8, "y": -0.5},
        {"word": "run", "x": 0.4, "y": -0.8}
    ]
    
    mouse_pos = op('mouseIn')
    mx = mouse_pos['tx'][0]
    my = mouse_pos['ty'][0]
    
    threshold = 0.4
    current_time = time.time()
    
    # 检查新的触发词
    for word_data in words_positions:
        dx = mx - word_data['x']
        dy = my - word_data['y']
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance < threshold:
            word_key = word_data['word']
            if word_key not in active_words:
                # 寻找一个可用的text operator
                available_text_op = None
                for text_op in text_ops:
                    if not any(info.get('text_op') == text_op.name for info in active_words.values()):
                        available_text_op = text_op
                        break
                
                if available_text_op:
                    print(f"Triggering word: {word_key} on {available_text_op.name}")
                    available_text_op.par.text = word_data['word']
                    available_text_op.par.positionx = word_data['x']*500
                    available_text_op.par.positiony = word_data['y']*500
                    available_text_op.par.fontalpha = 1
                    
                    active_words[word_key] = {
                        'start_time': current_time,
                        'x': word_data['x'],
                        'y': word_data['y'],
                        'text_op': available_text_op.name
                    }
    
    # 更新现有的词
    for word_key, word_info in list(active_words.items()):
        age = current_time - word_info['start_time']
        if age > 3:  # 10秒后消失
            # 重置text operator
            text_op = op(word_info['text_op'])
            text_op.par.text = ""
            text_op.par.fontalpha = 0
            del active_words[word_key]
        else:
            # 更新alpha值
            text_op = op(word_info['text_op'])
            alpha = 1.0 - (age / 3.0)
            text_op.par.fontalpha = alpha
            text_op.par.positionx = word_info['x']*500
            text_op.par.positiony = word_info['y']*500
    
    print(f"Active words: {list(active_words.keys())}")