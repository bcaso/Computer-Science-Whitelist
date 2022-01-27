import xml.etree.ElementTree as ET  # for xml

# import whitelist_dics {{{
import whitelist_dics.repository
import whitelist_dics.wiki
import whitelist_dics.blogs
import whitelist_dics.bbs
import whitelist_dics.software_download
import whitelist_dics.library

# }}}

lis = []
lis_total = []

# 规则 @*://*.v2ex.com 与 @*://v2ex.com/* 的拦截效果不同，后者没效果
# 规则 @*://前缀.域名.后缀/* 有时没效果
# 所以将所有的规则改为 @*://*.前缀.域名.后缀/*
# 如果前缀是 www. 就不要写在 Whitelist 的 value[0] 中 

'''
with prefix
@*://*.prefix.domain_name.suffix/*
no prefix
@*://*.domain_name.suffix/*
no prefix and no domain name, only the suffix
@*://*.suffix/*
'''

# generate url {{{
def gen_urls(whitelist_dic):
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
# }}}

def gen_txt(filename, lis):
    filename = 'whitelists/' + filename
    f = open(filename, 'w')
    for each in lis:
        f.write(each+'\n')
    f.close()

def gen_whitelist_rule_txt():
    f = open('whitelists/whitelist.txt', 'w')
    f.write(r'*://*/*')
    f.close()
      

# generate subscription txt {{{
def gen_subscription_txt():
    gen_whitelist_rule_txt()

    gen_urls(whitelist_dics.repository.Whitelist)
    gen_txt('仓库.txt', lis)

    lis.clear()

    gen_urls(whitelist_dics.wiki.Whitelist)
    gen_txt('wiki.txt', lis)

    lis.clear()

    gen_urls(whitelist_dics.blogs.Whitelist)
    gen_txt('博客.txt', lis)

    lis.clear()

    gen_urls(whitelist_dics.bbs.Whitelist)
    gen_txt('论坛.txt', lis)

    lis.clear()

    gen_urls(whitelist_dics.software_download.Whitelist)
    gen_txt('软件下载站.txt', lis)

    lis.clear()

    gen_urls(whitelist_dics.library.Whitelist)
    gen_txt('文库.txt', lis)

    lis.clear()
# }}}


# 汇总列表，for uBlacklist
def gen_subscription_combined_txt():
    f = open('whitelists/whitelists_combined.txt', 'w')
    for each in lis_total:
        f.write(each+'\n')
    f.close()

# 汇总域名列表，for other ways："cse.google.com"，油猴插件
def gen_domain_name_txt():
    f = open('whitelists/domain_name.txt', 'w')
    for each in lis_total:
        if each.startswith('@http'):  # @http(s)://www.cnblogs.com/*
            f.write(each[1:]+'\n')    # http(s)://www.cnblogs.com/*
            ...
        else:
            f.write(each[5:]+'\n') # *.prefix.domain_name.suffix
            #print(each[5:])
            ...

    f.close()


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

# 这个文件或许手修改更方便
def gen_cse_xml():
    ...


# generate annotations.xml {{{
# https://vae-0118.github.io/2017/11/06/Python%E4%B8%ADXML%E7%9A%84%E8%AF%BB%E5%86%99%E6%80%BB%E7%BB%93/
# TODO 给结果按权重排序
def gen_annotations_xml(list_of_domain):
    lis = []                          # TODO 列表中要添加更多的字段
    for each in list_of_domain:
        if each.startswith('@http'):  # @http(s)://www.cnblogs.com/*
            lis.append(each[1:])
        else:
            lis.append(each[5:])          # @*://*. 

    # print(lis)


    root = ET.Element('Annotations')       # 创建根节点
    tree = ET.ElementTree(root)            # 创建文档

    for link in lis:
        element = ET.Element('Annotation') # 子节点
        element.set('about', link)         # 这个属性的值可能只是注释
        # element.text = 'default'         # 节点中的文本内容

        Label = ET.SubElement(element, 'Label')
        Label.set('name', '_include_')

        AdditionalData = ET.SubElement(element, 'AdditionalData')
        AdditionalData.set('value', link)     # link 地址
        AdditionalData.set('attribute', 'original_url')


        root.append(element)               # 放到根节点下

    __indent(root)          # 增加换行符
    tree.write('whitelists/annotations.xml', encoding='utf-8', xml_declaration=True)
    ...

# }}}



def main():
    gen_subscription_txt()
    gen_subscription_combined_txt()
    gen_domain_name_txt()
    gen_annotations_xml(lis_total)

    ...


if __name__ == '__main__':

    main()

