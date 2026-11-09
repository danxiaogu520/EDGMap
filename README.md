# 归墟之门 · 世界图志

《欧陆风云 IV》模组《归墟之门》的 1444 年开局地图。点击国家可查看政体、统治者、外交和背景；地图支持中英切换和仅显示推荐国。

[打开地图](https://danxiaogu520.github.io/EDGMap/)

## 本地预览

在仓库根目录运行：

```sh
python -m http.server 8765 --bind 127.0.0.1 --directory dist
```

浏览器打开 [本地地图](http://127.0.0.1:8765/)。`dist/` 包含可直接部署的网页、地图数据、字体和图片，浏览及部署均不需要安装游戏。GitHub Pages 通过 [GitHub Actions](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) 发布 `dist/`，向 `main` 推送更新会重新部署。

`scripts/` 是在本地更新数据时使用的 Python 工具。地图导入需要已安装的游戏和脚本指定的 Steam 创意工坊模组；设定导入需要本地的 Word 原文件。部署使用仓库内已有的导出文件。

游戏界面素材和字体源自《欧陆风云 IV》及相关模组，设定文本源自《归墟之门设定》1.300。本站为非官方地图项目。
