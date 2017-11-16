# -*- coding: utf8 -*-

import ConfigParser
import json
import logging
import re

config_parser = ConfigParser.ConfigParser()
config_parser.read('config.txt')

def serialize(value, delimiter='\t', key_list=list()):
    if isinstance(value, list):
        str_list = list()
        for item in value:
            str_list.append(serialize(item))
        return delimiter.join(str_list)

    if isinstance(value, dict):
        str_list = list()
        for key in key_list:
            if key in value:
                str_list.append(serialize(value[key]))
            else:
                str_list.append('')
        return delimiter.join(str_list)
    
    # unicode or str
    if isinstance(value, basestring):
        return value.encode('utf8')

    return str(value)


def convert_pinyin(pinyin):
    # split
    # 浬 lǐ ㄌㄧ3也读作hǎilǐ。    
    previous_end = 0
    pinyin_list = list()
    
    # 《新华字典》V1998
    pattern = re.compile(ur'chuang|shuang|zhuang|chang|cheng|chong|chuai|chuan|guang|huang|jiang|jiong|kuang|liang|niang|qiang|qiong|shang|sheng|shuai|shuan|xiang|xiong|zhang|zheng|zhong|zhuai|zhuan|bang|beng|bian|biao|bing|cang|ceng|chai|chan|chao|chen|chou|chua|chui|chun|chuo|cong|cuan|dang|deng|dian|diao|ding|dong|duan|fang|feng|gang|geng|gong|guai|guan|hang|heng|hong|huai|huan|jian|jiao|jing|juan|kang|keng|kong|kuai|kuan|lang|leng|lian|liao|ling|long|luan|mang|meng|mian|miao|ming|nang|neng|nian|niao|ning|nong|nuan|pang|peng|pian|piao|ping|qian|qiao|qing|quan|rang|reng|rong|ruan|sang|seng|shai|shan|shao|shei|shen|shou|shua|shui|shun|shuo|song|suan|tang|teng|tian|tiao|ting|tong|tuan|wang|weng|xian|xiao|xing|xuan|yang|ying|yong|yuan|zang|zeng|zhai|zhan|zhao|zhei|zhen|zhou|zhua|zhui|zhun|zhuo|zong|zuan|ang|bai|ban|bao|bei|ben|bie|bin|cai|can|cao|cen|cha|che|chi|chu|cou|cui|cun|cuo|dai|dan|dao|dei|den|dia|die|diu|dou|dui|dun|duo|eng|fan|fei|fen|fou|gai|gan|gao|gei|gen|gou|gua|gui|gun|guo|hai|han|hao|hei|hen|hng|hou|hua|hui|hun|huo|jia|jie|jin|jiu|jue|jun|kai|kan|kao|kei|ken|kou|kua|kui|kun|kuo|lai|lan|lao|lei|lia|lie|lin|liu|lou|lüe|lun|luo|mai|man|mao|mei|men|mie|min|miu|mou|nai|nan|nao|nei|nen|nia|nie|nin|niu|nou|nüe|nuo|pai|pan|pao|pei|pen|pie|pin|pou|qia|qie|qin|qiu|que|qun|ran|rao|ren|rou|rui|run|ruo|sai|san|sao|sen|sha|she|shi|shu|sou|sui|sun|suo|tai|tan|tao|tie|tou|tui|tun|tuo|wai|wan|wei|wen|xia|xie|xin|xiu|xue|xun|yan|yao|yin|you|yue|yun|zai|zan|zao|zei|zen|zha|zhe|zhi|zhu|zou|zui|zun|zuo|ai|an|ao|ba|bi|bo|bu|ca|ce|ci|cu|da|de|di|du|ei|en|er|fa|fo|fu|ga|ge|gu|ha|he|hm|hu|ji|ju|ka|ke|ku|la|le|li|lo|lu|lü|ma|me|mi|mo|mu|na|ne|ng|ni|nu|nü|ou|pa|pi|po|pu|qi|qu|re|ri|ru|sa|se|si|su|ta|te|ti|tu|wa|wo|wu|xi|xu|ya|ye|yi|yo|yu|za|ze|zi|zu|a|e|ê|m|n|o')
    
    # 删除调号
    pinyin_toneless = pinyin
    pinyin_toneless = re.sub(ur'[āáǎàɑ̄ɑ́ɑ̌ɑ̀ĀÁǍÀ]', 'a', pinyin_toneless)
    pinyin_toneless = re.sub(ur'[ēéěèĒÉĚÈ]', 'e', pinyin_toneless)
    pinyin_toneless = re.sub(ur'[īíǐìĪÍǏÌ]', 'i', pinyin_toneless)
    pinyin_toneless = re.sub(ur'[ōóǒòŌÓǑÒ]', 'o', pinyin_toneless)
    pinyin_toneless = re.sub(ur'[ūúǔùŪÚǓÙ]', 'u', pinyin_toneless)
    pinyin_toneless = re.sub(ur'[ǖǘǚǜǕǗǙǛ]', 'v', pinyin_toneless)
    pinyin_toneless = re.sub(ur'[ê̄ếê̌ề]', 'ê', pinyin_toneless)

    match_list = re.finditer(pattern, pinyin_toneless)
    for match in match_list:
#         print match.start()
#         print match.end()
#         print pinyin[match.start():match.end()]
        
        pinyin_list.append(pinyin[previous_end:match.start()])
        pinyin_list.append(match.group())
        if re.search(ur'ā|ɑ̄|ē|ī|ō|ū|ǖ|Ā|Ē|Ī|Ō|Ū|Ǖ|ê̄', pinyin[match.start():match.end()]):
            pinyin_list.append('1')
        elif re.search(ur'á|ɑ́|é|í|ó|ú|ǘ|Á|É|Í|Ó|Ú|Ǘ|ế', pinyin[match.start():match.end()]):
            pinyin_list.append('2')
        elif re.search(ur'ǎ|ɑ̌|ě|ǐ|ǒ|ǔ|ǚ|Ǎ|Ě|Ǐ|Ǒ|Ǔ|Ǚ|ê̌', pinyin[match.start():match.end()]):
            pinyin_list.append('3')
        elif re.search(ur'à|ɑ̀|è|ì|ò|ù|ǜ|À|È|Ì|Ò|Ù|Ǜ|ề', pinyin[match.start():match.end()]):
            pinyin_list.append('4')
        else:
            pinyin_list.append('5') 
         
        previous_end = match.end()

    return ''.join(pinyin_list)


def load_dict():
    line_list = list()
    entry_line_list = list()

    f = file('xinhua_' + config_parser.get('setting', 'version') + '.dic')
    for line in f:
        line = line.decode('utf8').rstrip()
        logging.debug(line)

        if len(line) == 0:
            entry_line_list.append(line_list)
            line_list = list()
            continue
        
        # a - C991
        line = line.replace(u'ɑ', 'a')
        # g - C9A1
        line = line.replace(u'ɡ', 'g')
        line_list.append(line)
    f.close()
    
    if len(line_list) > 0:
        entry_line_list.append(line_list)

    logging.debug(len(entry_line_list))
    
    return entry_line_list
    

def parse_entry(line_list):
    logging.debug('\t'.join(line_list))
        
    entry_dict = dict()
    try:        
        # 页码
        entry_dict['pages'] = list()
        entry_dict['images'] = list()
        page_list = line_list[0].split(u'、')
        for page in page_list:
            entry_dict['pages'].append(int(page))
            entry_dict['images'].append(page.zfill(4) + '.jpg')
         
        entry_dict['explanation'] = '<ys>' + ''.join(line_list[1:]) + '</ys>'

        # 字头
        # 啊 (△嗄) ○2 á ㄚ2
        # ☆（㬟u3B1F） fēn ㄈㄣ1
        item_list = line_list[1].split()
        entry_dict['form'] = item_list[0]

        # 拼音
        # 阿 ○1 ā ㄚ1
        # 癌 ái ㄞ2 (旧读yán)
        pinyin_set = set()
        # 替换缺字☆（㬟u3B1F），避免解析为拼音
        line, cnt = re.subn(ur'☆[（\(].*[）\)]', '', line_list[1])
        match_list = re.findall(ur'[A-Za-züêāáǎàɑ̄ɑ́ɑ̌ɑ̀ĀÁǍÀēéěèĒÉĚÈīíǐìĪÍǏÌōóǒòŌÓǑÒūúǔùŪÚǓÙǖǘǚǜǕǗǙǛê̄ếê̌ề]+', line)
        for match in match_list:
            pinyin_set.add(match)
        
        entry_dict['tags'] = list()
        for line in line_list[2:]:
            # 词组 
            # 【阿昌】阿昌族，我国少数民族名，参看附表。
            # [腌臜](-zɑ)不干净。
            match_list = re.findall(ur'[【\[](.*?)[】\]]', line)
            for match in match_list:
                entry_dict['tags'].append(match)
                logging.debug(match)

            # 替换缺字☆（㬟u3B1F），避免解析为拼音
            line, cnt = re.subn(ur'☆[（\(].*[）\)]?', '', line)
            # ‘嗄’又shà见397页。
            # ●5(旧读bì)靠近，挨着
            # 浬 lǐ ㄌㄧ3也读作hǎilǐ。
            # ○2 ē见106页。
            match_list = re.findall(ur'[又|旧读|也读作]([A-Za-züêāáǎàɑ̄ɑ́ɑ̌ɑ̀ĀÁǍÀēéěèĒÉĚÈīíǐìĪÍǏÌōóǒòŌÓǑÒūúǔùŪÚǓÙǖǘǚǜǕǗǙǛê̄ếê̌ề]+)', line)
            for match in match_list:
                pinyin_set.add(match)
            match_list = re.findall(ur'([A-Za-züêāáǎàɑ̄ɑ́ɑ̌ɑ̀ĀÁǍÀēéěèĒÉĚÈīíǐìĪÍǏÌōóǒòŌÓǑÒūúǔùŪÚǓÙǖǘǚǜǕǗǙǛê̄ếê̌ề]+)见(\d+|本)页', line)
            for match in match_list:
                pinyin_set.add(match[0])
        
        entry_dict['pinyins'] = sorted(list(pinyin_set))
        for pinyin in entry_dict['pinyins']:
            entry_dict['tags'].append(convert_pinyin(pinyin))
            
    except Exception as e:
        logging.error(e)
        logging.error('\t'.join(line_list))
        
    return entry_dict


def parse_dict(entry_line_list):
    entry_list = list()
    for line_list in entry_line_list:
        entry_dict = parse_entry(line_list)
        entry_dict['wordListName'] = u'《新华字典》第' + config_parser.get('setting', 'version') + u'版'
        entry_dict['sort'] = len(entry_list)
        entry_list.append(entry_dict)
    
    return entry_list
    

def dump_json(entry_list):
    f = file('xinhua_' + config_parser.get('setting', 'version') + '.json', 'w')
    f.write(json.dumps(entry_list, ensure_ascii=False, indent=4, separators=(',', ': ')).encode('utf8'))
    f.close()
    

def dump_tab(entry_list):
    f = open('xinhua_' + config_parser.get('setting', 'version') + '.txt', 'w')

    f.write('\t'.join(['wordListName', 'sort', 'form', 'pinyins', 'tags', 'explanation', 'pages', 'images']) + '\n')
    for entry in entry_list:
        f.write(serialize(entry, '\t', ['wordListName', 'sort', 'form']) + '\t')
        f.write(serialize(entry['pinyins'], '; ') + '\t')
        f.write(serialize(entry['tags'], '; ') + '\t')
        f.write(serialize(entry['explanation'], '; ') + '\t')
        f.write(serialize(entry['pages'], '; ') + '\t')
        f.write(serialize(entry['images'], '; ') + '\n')
        
    f.close()
    
    
def main():
    entry_line_list = load_dict()
    
    entry_list = parse_dict(entry_line_list)

    dump_json(entry_list)    
    dump_tab(entry_list)


if __name__ == '__main__':
    """ main """
    # Log
    logging.basicConfig(filename='xinhua_' + config_parser.get('setting', 'version') + '.log', filemode='w', level=logging.INFO, 
    format='[%(levelname)s\t%(asctime)s\t%(funcName)s\t%(lineno)d]\t%(message)s')

    try:
        main()

    except Exception as e:
        logging.error(e)
