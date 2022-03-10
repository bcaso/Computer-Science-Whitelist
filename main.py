import os
import sqlite3
import xml.etree.ElementTree as ET  # for xml

# 读取数据库并存入 whitelist_dics {{{
# whitelist_dics = {table_name_list[i]:{key_domain:(prefix, suffix, score, description)}}

conn = sqlite3.connect('whitelists.db')   # 如果文件不存在，会自动在当前目录创建:
cursor = conn.cursor()                    # 创建一个Cursor:


# get all table_name from database and save it to the variable {table_name_list} {{{
table_name_list = []

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()    
# print(table_names)   # [('wiki',), ('blogs',), ('library',), ('software',), ('video',), ('repository',), ('bbs',)]
for _ in table_names:
    table_name_list.append(_[0])

print(table_name_list)
# }}}


whitelist_dics = {} # {table_name_list[i]:{key_domain:(prefix, suffix, score, description)}}

for i in range(len(table_name_list)):
    sq = f"select * from {table_name_list[i]};"
    cursor.execute(sq)
    data_all = cursor.fetchall()
    
    #print(data_all)    #[(1,2,3,4,5),(1,2,3,4,5),]

    # 存入 whitelist_dics {{{
    tmp_dic = {}

    key_domain = ''
    tmp_lis = []


    for data in data_all:
        key_domain = data[0]
        tmp_lis = data[1:]

        tmp_dic[key_domain] = tmp_lis

    whitelist_dics[table_name_list[i]] = tmp_dic

    # }}}
        
    

print(whitelist_dics)


cursor.close()  # 关闭Cursor:
conn.commit()   # 提交事务:
conn.close()    # 关闭Connection:

# }}}

lis = []          # 临时列表
lis_total = []    # 总列表，递增添加所有名单，不减少


# generate urls_list {{{

def gen_urls_list(whitelist_dic, startwith_at=False):
    if not startwith_at : # @ 符号是 uBlacklist 的白名单的前缀
        '''
            uBlacklist whitelist rule:
                with prefix
                    @*://*.prefix.domain_name.suffix/*
                no prefix
                    @*://*.domain_name.suffix/*
                no prefix and no domain name, only the suffix
                    @*://*.suffix/*
        '''
        # k,v 即 domain:[prefix, suffix, score, description]
        # 将内容存到临时列表 lis = [url, url,,,], url='@*://prefix.domain_name.suffix'
        for k,v in whitelist_dic.items(): 
            url = '@*://*.'
            # 加前缀
            if v[0] != '':
                if v[0].startswith('http://') or v[0].startswith('https://'):
                    url = '@'+v[0]+'.'        # uBlacklist suppot rules like "@https://www.cnblogs.com/*"
            
                elif v[0].startswith('www'): # www.cnblogs.com/*
                    # 在 cse.google.com 中，"*.www.cnblogs.com/*" 不会匹配 https://www.cnblogs.com/*
                    #              但是     "*.my.oschina.net/*"  能匹配到 https://my.oschina.net/*
                    url = "@https://"+v[0]+'.'
                else:
                    url+=v[0] + '.'
            # 加域名
            if k != '':
                url += k.lower() # uBlacklist 对域名区分大小写 @*://*.stackoverflow.com/* 与 @*://*.StackOverflow.com/* 拦截效果不同
            else:
                url = url[:-1]   # change url('@*://*.') to '@*://*', 为了添加指定后缀的域名，如 @*://*.edu

            # 加后缀
            if v[1] != '':    
                #  @*://*.docin.com/p-* , 后缀以 "p-" 开头，如 “https://www.docin.com/p-1706944942.html”
                if '/' in v[1]:
                    url+='.'+v[1]+'*'  # 这个可以取代下面的写法
                # 添加完全后缀, @*://*.mathsisfun.com/*
                else: 
                    url+='.'+v[1]+'/*'

            #print(url)
            lis.append(url)
            lis_total.append(url)
    else:
        # for google cse annotations
        # lis = [[url,score,description], [url,score,description],,, ]
        '''
        cse whitelist rule:
            with prefix
                *.prefix.domain_name.suffix/*
                https://prefix.domain_name.suffix/*

            no prefix
                *.domain_name.suffix/*
            no prefix and no domain name, only the suffix
                *.suffix/*
        '''
        for k,v in whitelist_dic.items(): 
            url = '*.'
            # 加前缀
            if v[0] != '':
                if v[0].startswith('http://') or v[0].startswith('https://'):   # http(s)://www
                    url = v[0]+'.'             
                elif v[0].startswith('www'): # www.cnblogs.com/*
                    # 在 cse.google.com 中，"*.www.cnblogs.com/*" 不会匹配 https://www.cnblogs.com/*
                    #              但是     "*.my.oschina.net/*"  能匹配到 https://my.oschina.net/*
                    url = "https://"+v[0]+'.'
                else:
                    url+=v[0] + '.'
            # 加域名
            if k != '':
                url += k.lower()
            else:
                url = url[:-1]   # 为了添加指定后缀的域名，如 *.edu

            # 加后缀, *.docin.com/p-* , 后缀以 "p-" 开头，如 “https://www.docin.com/p-1706944942.html”
            if v[1] != '':    
                if '/' in v[1]:
                    url+='.'+v[1]+'*'
                # 添加完全后缀, *.mathsisfun.com/*
                else: 
                    url+='.'+v[1]+'/*'

            #print(url)
            # annotations.xml 中的 score 是字符串格式： https://developers.google.com/custom-search/docs/annotations
            lis.append([url, str(v[2]), v[3]]) # lis = [[url,str(score),description], [url,str(score),description],,, ]
            lis_total.append(url)
        ...
# }}}

# uBlacklist txt subscription txt {{{
def gen_subscription_txt():
    # generate whitelist rule text
    with open( output + '/whitelist.txt', 'w') as f:
        f.write(r'*://*/*')

    for k,v in whitelist_dics.items():
        #print(k, v)
        gen_urls_list(v)
        filename = output + '/' + k + '.txt'
        with open(filename, 'w') as f:
            for each in lis:
                f.write(each+'\n')

        lis.clear()
# }}}

# 汇总 txt {{{
# 汇总列表，for uBlacklist
def gen_subscription_combined_txt():
    with open(output + '/whitelists_combined.txt', 'w') as f:
        for each in lis_total:
            f.write(each+'\n')

# 汇总域名列表，for other ways："cse.google.com"，油猴插件
def gen_domain_name_txt():
    with open(output + '/domain_name.txt', 'w') as f:
        for each in lis_total:
            if each.startswith('@http'):  # @http(s)://www.cnblogs.com/*
                f.write(each[1:]+'\n')    # http(s)://www.cnblogs.com/*
            else:
                f.write(each[5:]+'\n') # *.prefix.domain_name.suffix
                #print(each[5:])

# }}}

# 增加换行符 {{{
# https://vae-0118.github.io/2017/11/06/Python%E4%B8%ADXML%E7%9A%84%E8%AF%BB%E5%86%99%E6%80%BB%E7%BB%93/
def __indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            __indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
# }}}

# facet_items {{{
# weight from -1.0 to 1.0
facet_items = {
        'wiki':{'Label_name':'wiki',
          'Label_mode':'FILTER',
          'Label_weight':'0.9',
          'Label_enable_for_facet_search':'true',
          'Rewrite':'',
          'entities':['/m/01mf_','/m/05z1_','/m/01mkq','/m/04rjg']},
        'bbs':{'Label_name':'bbs',
          'Label_mode':'FILTER',
          'Label_weight':'0.8',
          'Label_enable_for_facet_search':'true',
          'Rewrite':'',
          'entities':['/m/01mf_','/m/05z1_','/m/01mkq','/m/04rjg']},
        'repository':{'Label_name':'repository',
          'Label_mode':'FILTER',
          'Label_weight':'0.8',
          'Label_enable_for_facet_search':'true',
          'Rewrite':'',
          'entities':['/m/01mf_','/m/05z1_','/m/01mkq','/m/04rjg']},
        'blogs':{'Label_name':'blogs',
          'Label_mode':'FILTER',
          'Label_weight':'0.7',
          'Label_enable_for_facet_search':'true',
          'Rewrite':'',
          'entities':['/m/01mf_','/m/05z1_','/m/01mkq','/m/04rjg']},
        'library':{'Label_name':'library',
          'Label_mode':'FILTER',
          'Label_weight':'0.4',
          'Label_enable_for_facet_search':'true',
          'Rewrite':'',
          'entities':['/m/01mf_','/m/05z1_','/m/01mkq','/m/04rjg']},
        'software':{'Label_name':'software',
          'Label_mode':'FILTER',
          'Label_weight':'0.5',
          'Label_enable_for_facet_search':'false',
          'Rewrite':'',
          'entities':[]},
        'pdf':{'Label_name':'pdf',
          'Label_mode':'BOOST',
          'Label_weight':'0.5',
          'Label_enable_for_facet_search':'false',
          'Rewrite':'filetype:pdf',
          'entities':[]},
        'video':{'Label_name':'video',
          'Label_mode':'FILTER',
          'Label_weight':'0',
          'Label_enable_for_facet_search':'true',
          'Rewrite':'',
          'entities':['/m/01mf_']},
        'edu':{'Label_name':'edu',
          'Label_mode':'BOOST',
          'Label_weight':'0.1',
          'Label_enable_for_facet_search':'true',
          'Rewrite':'site:.edu',
          'entities':[]},
}
# }}}

# 这个文件或许手修改更方便, 所以只生成该文件中的标签部分 {{{
def gen_cse_xml():
    root = ET.Element('Facet')       # 创建根节点
    tree = ET.ElementTree(root)      # 创建文档


    for facet in list(facet_items.values()):
        FacetItem = ET.Element('FacetItem')      # 子节点

        Label = ET.SubElement(FacetItem, 'Label')
        Label.set('name', facet['Label_name'])
        Label.set('mode', facet['Label_mode'])
        Label.set('weight',facet['Label_weight'])
        Label.set('enable_for_facet_search',facet['Label_enable_for_facet_search'])

        Rewrite = ET.SubElement(Label, 'Rewrite')
        rewrite_text = facet['Rewrite']
        if rewrite_text != '':
            Rewrite.text = rewrite_text

        entities = ET.SubElement(Label, 'entities')
        for mid in facet['entities']:
            entity = ET.SubElement(entities, 'entity')
            entity.set('mid', mid)

        Title = ET.SubElement(FacetItem, 'Title')
        Title.text = facet['Label_name']

        root.append(FacetItem)               # 放到根节点下

    __indent(root)          # 增加换行符
    tree.write(output + '/cse_FacetLabels.xml', encoding='utf-8', xml_declaration=True)
    ...

# }}}

# generate annotations.xml {{{
# https://vae-0118.github.io/2017/11/06/Python%E4%B8%ADXML%E7%9A%84%E8%AF%BB%E5%86%99%E6%80%BB%E7%BB%93/
def gen_annotations_xml():
    total_length = 0

    root = ET.Element('Annotations')       # 创建根节点
    tree = ET.ElementTree(root)            # 创建文档

    # add Annotation {{{

    # whitelists 总字典  { 'bbs':{'':[],'':[]}, 'blogs':{} }
    for k,v in whitelist_dics.items():
        print('k = {}, v={}'.format(k, v)) # 'wiki':{'domain':(prefix,suffix,score,description)}
        # 将 k 对应的字典转为存储到临时列表 lis
        gen_urls_list(v, True)
        # print(lis) # [[url, score, description], ['*.stackoverflow.com/*', '0.8', description]]

        # 遍历列表
        for each in lis:
            # each 的属性，权重
            element = ET.Element('Annotation') # 子节点
            element.set('about', each[0])      # about 存 url pattern
            element.set('score', each[1])      # str(score)

            Label = ET.SubElement(element, 'Label')
            Label.set('name', '_include_')
            Comment = ET.SubElement(element, 'Comment')
            Comment.text = each[2]             # description

            # 添加标签，如 <Label name="bbs"/>
            Label = ET.SubElement(element, 'Label')
            Label.set('name', facet_items[k]['Label_name'])

            root.append(element)               # 放到根节点下


        
        # 每次处理一张表, total_length 是递增的
        #print(lis, len(lis), end='\n')
        total_length += len(lis)
        lis.clear()

    # }}}

    # Annotations 的三个非必要属性
    root.set('start', '0')
    root.set('num', str(total_length))
    root.set('total', str(total_length))

    __indent(root)          # 增加换行符
    tree.write(output + '/annotations.xml', encoding='utf-8', xml_declaration=True)
# }}} 


def main():
    # txt, xml 的输出目录
    global output
    output = './whitelists'
    if not os.path.exists(output):
        os.mkdir(output)

    gen_subscription_txt()
    gen_subscription_combined_txt()
    gen_domain_name_txt()
    # BackgroundLabels 下的 Lables 只能有两个，且是两种(_include_ 和 _exclude_)
    gen_cse_xml()
    gen_annotations_xml()


if __name__ == '__main__':

    main()

