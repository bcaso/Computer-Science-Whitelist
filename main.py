import xml.etree.ElementTree as ET  # for xml

# import whitelist_dics {{{
import whitelist_dics.repository, \
        whitelist_dics.wiki, \
        whitelist_dics.blogs, \
        whitelist_dics.bbs, \
        whitelist_dics.software, \
        whitelist_dics.library, \
        whitelist_dics.videos

# https://magic.iswbm.com/c03/c03_02.html
# for python 3.9:
whitelist_dics = { 'repository':whitelist_dics.repository.Whitelist } | \
        {'wiki':whitelist_dics.wiki.Whitelist} | \
        {'blogs':whitelist_dics.blogs.Whitelist} | \
        {'bbs':whitelist_dics.bbs.Whitelist} | \
        {'software':whitelist_dics.software.Whitelist} | \
        {'library':whitelist_dics.library.Whitelist} | \
        {'videos':whitelist_dics.videos.Whitelist} 

# }}}

lis = []          # 临时列表
lis_total = []    # 总列表，递增添加所有名单，不减少


# generate urls_list {{{
'''
uBlacklist whitelist rule:
    with prefix
        @*://*.prefix.domain_name.suffix/*
    no prefix
        @*://*.domain_name.suffix/*
    no prefix and no domain name, only the suffix
        @*://*.suffix/*

cse whitelist rule:
    with prefix
        *.prefix.domain_name.suffix/*
        https://prefix.domain_name.suffix/*

    no prefix
        *.domain_name.suffix/*
    no prefix and no domain name, only the suffix
        *.suffix/*
'''
def gen_urls_list(whitelist_dic, startwith_at=False):
    if not startwith_at :
        for k,v in whitelist_dic.items(): 
            url = '@*://*.'
            # 前缀
            if v[0] != '':
                if v[0].startswith('http://') or v[0].startswith('https://'):   # http(s)://www.cnblogs.com/*
                    url = '@'+v[0]+'.'            # uBlacklist suppot rules like "@https://www.cnblogs.com/*"
                    ...
                elif v[0].startswith('www'): # www.cnblogs.com/*
                    # 在 cse.google.com 中，"*.www.cnblogs.com/*" 不会匹配 https://www.cnblogs.com/*
                    #              但是     "*.my.oschina.net/*"  能匹配到 https://my.oschina.net/*
                    # 没有更好的方法处理 http 或 https，全都改为 https://www.
                    # 如果是以 http 开头，就写到前缀中，这里处理不了
                    url = "@https://"+v[0]+'.'
                    ...
                else:
                    url+=v[0] + '.'
            # 加域名
            if k != '':
                url += k.lower() # uBlacklist 对域名区分大小写 @*://*.stackoverflow.com/* 与 @*://*.StackOverflow.com/* 拦截效果不同
            else:
                url = url[:-1]   # change url('@*://*.') to '@*://*', 为了添加指定后缀的域名，如 @*://*.edu

            # 后缀
            if v[1] != '':    
                # 添加不完全后缀, @*://*.docin.com/p-* , 多数文库的文章以 "p-" 开头，如 “https://www.docin.com/p-1706944942.html”
                if '/' in v[1]:
                    url+='.'+v[1]+'*'
                # 添加完全后缀, @*://*.mathsisfun.com/*
                else: 
                    url+='.'+v[1]+'/*'

            #print(url)
            lis.append(url)
            lis_total.append(url)
    else:
        for k,v in whitelist_dic.items(): 
            if(len(v) != 3):
                print('-------------','k is',k, 'v is ', v)
            url = '*.'
            # 前缀
            if v[0] != '':
                if v[0].startswith('http://') or v[0].startswith('https://'):   # http(s)://www
                    url = v[0]+'.'             
                    ...
                elif v[0].startswith('www'): # www.cnblogs.com/*
                    # 在 cse.google.com 中，"*.www.cnblogs.com/*" 不会匹配 https://www.cnblogs.com/*
                    #              但是     "*.my.oschina.net/*"  能匹配到 https://my.oschina.net/*
                    # 没有更好的方法处理 http 或 https，全都改为 https://www.
                    # 如果是以 http 开头，就写到前缀中，这里处理不了
                    url = "https://"+v[0]+'.'
                    ...
                else:
                    url+=v[0] + '.'
            # 加域名
            if k != '':
                url += k.lower()
            else:
                url = url[:-1]   # 为了添加指定后缀的域名，如 *.edu

            # 后缀
            if v[1] != '':    
                # 添加不完全后缀, *.docin.com/p-* , 多数文库的文章以 "p-" 开头，如 “https://www.docin.com/p-1706944942.html”
                if '/' in v[1]:
                    url+='.'+v[1]+'*'
                # 添加完全后缀, *.mathsisfun.com/*
                else: 
                    url+='.'+v[1]+'/*'

            #print(url)
            lis.append([url, v[2]]) # [url, score]
            lis_total.append(url)
        ...
# }}}

# generate subscription txt {{{
def gen_subscription_txt():
    # generate whitelist rule text
    with open('whitelists/whitelist.txt', 'w') as f:
        f.write(r'*://*/*')

    for k,v in whitelist_dics.items():
        #print(k, v)
        gen_urls_list(v)
        #gen_txt(k + '.txt', lis)
        filename = 'whitelists/' + k + '.txt'
        with open(filename, 'w') as f:
            for each in lis:
                f.write(each+'\n')

        lis.clear()
# }}}

# 汇总 txt {{{
# 汇总列表，for uBlacklist
def gen_subscription_combined_txt():
    with open('whitelists/whitelists_combined.txt', 'w') as f:
        for each in lis_total:
            f.write(each+'\n')

# 汇总域名列表，for other ways："cse.google.com"，油猴插件
def gen_domain_name_txt():
    with open('whitelists/domain_name.txt', 'w') as f:
        for each in lis_total:
            if each.startswith('@http'):  # @http(s)://www.cnblogs.com/*
                f.write(each[1:]+'\n')    # http(s)://www.cnblogs.com/*
                ...
            else:
                f.write(each[5:]+'\n') # *.prefix.domain_name.suffix
                #print(each[5:])
                ...

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
    tree.write('whitelists/cse_FacetLabels.xml', encoding='utf-8', xml_declaration=True)
    ...

# }}}

# generate annotations.xml {{{
# https://vae-0118.github.io/2017/11/06/Python%E4%B8%ADXML%E7%9A%84%E8%AF%BB%E5%86%99%E6%80%BB%E7%BB%93/
# TODO
def gen_annotations_xml():
    total_length = 0

    root = ET.Element('Annotations')       # 创建根节点
    tree = ET.ElementTree(root)            # 创建文档

    # add Annotation {{{

    # whitelists 总字典  { 'bbs':{'':[],'':[]}, 'blogs':{} }
    for k,v in whitelist_dics.items():
        # print(k, v)
        # 将 k 对应的字典转为 list
        gen_urls_list(v, True)

        # 遍历列表
        for each in lis:
            # each 的属性，权重
            element = ET.Element('Annotation') # 子节点
            element.set('about', each[0])      # about 存 url pattern
            element.set('score', each[1])
            # element.text = 'default'         # 节点中的文本内容

            Label = ET.SubElement(element, 'Label')
            Label.set('name', '_include_')
            Label = ET.SubElement(element, 'Label')
            Label.set('name', facet_items['wiki']['Label_name'])

            root.append(element)               # 放到根节点下

    total_length += len(lis)
    
    print(lis, len(lis), end='\n')
    lis.clear()

    # }}}

    # Annotations 的三个非必要属性
    root.set('start', '0')
    root.set('num', str(total_length))
    root.set('total', str(total_length))

    __indent(root)          # 增加换行符
    tree.write('whitelists/annotations.xml', encoding='utf-8', xml_declaration=True)
# }}} 


def main():
    gen_subscription_txt()
    gen_subscription_combined_txt()
    gen_domain_name_txt()
    # BackgroundLabels 下的 Lables 只能有两个，且是两种(_include_ 和 _exclude_)
    gen_cse_xml()
    gen_annotations_xml()

    ...


if __name__ == '__main__':

    main()

