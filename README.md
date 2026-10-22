# 基本astro的通用数据展示前端



已经安装好了astro框架

```sh
bun create astro@latest -- --template basics
```



## 🚀 目前文件结构



```text
/
├── public/
│   └── favicon.svg
├── src
│   ├── assets
│   │   └── astro.svg
│   ├── components
│   │   └── Welcome.astro
│   ├── layouts
│   │   └── Layout.astro
│   └── pages
│       └── index.astro
└── package.json
```



## 🧞 常用命令

All commands are run from the root of the project, from a terminal:

| Command               | Action                                           |
|:--------------------- |:------------------------------------------------ |
| `bun install`         | Installs dependencies                            |
| `bun dev`             | Starts local dev server at `localhost:4321`      |
| `bun build`           | Build your production site to `./dist/`          |
| `bun preview`         | Preview your build locally, before deploying     |
| `bun astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `bun astro -- --help` | Get help using the Astro CLI                     |

## task1: 实现一个通用幻灯片播放框架

- 幻灯片渲染、播放等功能通过`reveal.js`包来实现，已经安装。

- 创建一个内容集合，后端将每个幻灯片内容以json文件形式写入内容集合目录：`src/ppts/`

- 幻灯片文件结构示例如下：

  ```json
  {
      config: {
          autoslide: true,
          time: 6000,
          other: config
      },
      decks: [
          {
              template: "Cover",
              slide: {
                  title: "This Year",
                  subtitle: "by someone", 
              }
          },
          {
              template: "Default",
              slide: {
                  title: "This Year",
                  body: "by someone", 
              }
          }
      ]
      
  }
  ```

- 设置内容集合需要修改、编辑以下文件：

  - `tsconfig.json`

  - `src/content.config.js`

- `src/components/ppts`目录下为每一个模板建立一个组件。

- 为幻灯片演示创建一个布局组件：`src/layouts/PptLayout.astro`，接收json文件中的config参数，初始化revealjs。

- 在`src/pages/ppts`目录中创建动态路由和导航页：

  - `[slug].astro`: 以json文件做为路由，遍历json文件中的decks, 动态加载template参数所指的模板，然后渲染slide数据。**这里是难点和关键**

  - `index.astro`: 导航页。

- 网站首页添加导航栏，添加到ppts目录页的链接。

- 最后实现：在内容集合中添加一个json文件，build后会自动完成渲染、路由，前端代码零修改。
