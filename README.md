# Google-Chinese-Results-Whitelist

垃圾站点出现在 Google 中文搜索结果中，实在是恶心——于是这个白名单就这么出来了。

这个名单专注收集<b>问答论坛</b>，和具有 wiki 性质的高质量内容网站，类型偏向电脑技术。 

## 搜索引擎

只要是支持自定义过滤搜索结果的搜索引擎，都是不错的选择。

<a href="https://github.com/iorate/uBlacklist" target="_blank">uBlacklist</a> 目前支持搜索引擎有 Google, Bing, DuckDuckgo, Ecosia, Startpage

* 就访问速度上看，Bing 最快。

* 就样式上看，Bing 最好
  * 在使用油猴本 <a href="https://www.ntaow.com/aboutscript.html" target="_blank">AC-重定向</a> 将搜索结果多列显示时，Bing 的样式要比 Google 好看，Google 显得有些乱。
  * Bing 页面最底端没有相关搜索(几乎用不到，还占位置)，也没有搜索关键词对应的相关图片。


## 原理：

先添加规则 `*://*/*` 以屏蔽所有网址。

对于白名单，这样添加： `@:*//*.前缀.域名.后缀/*`，如 `@:*//*.github.com/`, 区分大小写

对网站进行分类，然后统一生成符合 uBlacklist 规则的白名单。

只获取网站下的博客部分，和问答交流部分，通过前后缀做区分，对应的网址不能放到同一个字典内，但可以把问答区的地址放入论坛名单，把博客放入到博客名单中。

如对于博客园规则，`'cnblogs':['www','com']`，加上前缀 `www` 就能过滤 园荐`recomm.cnblogs.com`


最后生成的名单可以汇总到 `whitelists_combined.txt` 中。

<a href="https://github.com/iorate/ublacklist/releases/tag/v7.0.0" target="_blank">uBlacklist 7.0</a> 支持对订阅规则的开关功能，所以可以定阅不同类别的白名单，然后根据搜索需要只开启一部分。

> 注：白名单会使得每一搜索页中的内容变得特别少，因为符合白名单的网站，可能不在结果的第一页，
> 因此，要在设置中，把每页搜索结果数调得尽可能大。
>
> 浏览器插件 <a href="https://chrome.google.com/webstore/detail/uautopagerize/kdplapeciagkkjoignnkfpbfkebcfbpb" target="_blank">uAutoPagerize</a> 支持在自动翻页的同时过滤搜索结果。


## 白名单与黑名单

黑名单是无限的。白名单可以是有限的，以有限的精力去维护有限的白名单。

两个 google 帐号，开两个 chrome, 一个用<a href="https://github.com/cobaltdisco/Google-Chinese-Results-Blocklist" target="_blank">黑名单</a>一个用白名单。

经过一段时间的积累，就可以转到白名单。

