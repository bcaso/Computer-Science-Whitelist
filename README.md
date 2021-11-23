# Google-Chinese-Results-Whitelist

垃圾站点出现在 Google 中文搜索结果中，实在是恶心——于是这个白名单就这么出来了。

这个名单专注收集<b>问答论坛</b>，和具有 wiki 性质的高质量内容网站，类型偏向电脑技术。 

# 原理：

添加规则，`*://*/*` 以屏蔽所有网址。

对于白名单，这样添加： `@:*//*.前缀.域名.后缀/*`，如 `@:*//*.github.com/`, 区分大小写

对网站进行分类，然后统一生成符合 uBlacklist 规则的白名单。

找到<a href="https://github.com/bcaso/Google-Chinese-Results-Whitelist/blob/main/uWhitelist_subscription.txt">uWhitelist_subscription.txt</a>，点击 `Raw`, 进入纯文本格式，可以拷贝这个地址到 uBlacklist 订阅中。


白名单会使得每一搜索页中的内容变得特别少，因为符合白名单的网站，可能不在结果的第一页，因此，要在设置中，把每页搜索结果数调得尽可能大。


# 白名单与黑名单

黑名单是无限的。白名单可以是有限的，以有限的精力去维护有限的白名单。

两个 google 帐号，开两个 chrome, 一个用<a href="https://github.com/cobaltdisco/Google-Chinese-Results-Blocklist">黑名单</a>一个用白名单。

经过一段时间的积累，就可以转到白名单。

