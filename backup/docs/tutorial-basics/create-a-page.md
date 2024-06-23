---
sidebar_position: 1
---

# 3小时英语学习

卡作（kazuo.ai）的定位是基于AI增强的卡片记忆学习  
因为部分社群小伙伴有一些现实困难，比如：  
1网络设置 2 配置困难 3 移动端的使用需求  
所以，我们为已经付费的用户增加了很多朗读英语功能支持  
同时，参考了Enjoy的语音评估功能与音高（Pitch）的可视化  
也通过这件事形成了“多模态卡片”等创新功能  
在这里感谢笑来老师的1000学习方法论与enjoy（https://1000h.org/）
从开始到现在，终身受益  
接下来，kazuo迈向新的里程碑   

以下，为做好新老学员的衔接，  
从“多模态”卡片的角度，来讲解kazuo使用方式：  


- `src/pages/index.js` → `localhost:3000/`
- `src/pages/foo.md` → `localhost:3000/foo`
- `src/pages/foo/bar.js` → `localhost:3000/foo/bar`

## Create your first React Page

Create a file at `src/pages/my-react-page.js`:

```jsx title="src/pages/my-react-page.js"
import React from 'react';
import Layout from '@theme/Layout';

export default function MyReactPage() {
  return (
    <Layout>
      <h1>My React page</h1>
      <p>This is a React page</p>
    </Layout>
  );
}
```

A new page is now available at [http://localhost:3000/my-react-page](http://localhost:3000/my-react-page).

## Create your first Markdown Page

Create a file at `src/pages/my-markdown-page.md`:

```mdx title="src/pages/my-markdown-page.md"
# My Markdown page

This is a Markdown page
```

A new page is now available at [http://localhost:3000/my-markdown-page](http://localhost:3000/my-markdown-page).
