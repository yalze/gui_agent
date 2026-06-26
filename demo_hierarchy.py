"""演示控件树结构和 LLM 看到的内容"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import uiautomator2 as u2

    print("=" * 60)
    print("  控件树演示脚本")
    print("=" * 60)

    # 连接设备
    print("\n[1] 连接设备...")
    device = u2.connect("127.0.0.1:5555")
    info = device.info
    print(f"  ✅ 当前App: {info['currentPackageName']}")

    # 获取控件树
    print("\n[2] 获取控件树（XML格式）...")
    xml = device.dump_hierarchy()

    print(f"  控件树总长度: {len(xml)} 字符")
    print(f"  节点数量: 约 {xml.count('<node')} 个")

    # 展示控件树的结构（前30个节点）
    print("\n[3] 控件树结构示例（前30个节点）:")
    print("-" * 60)

    # 解析并展示前几个节点
    import re
    nodes = re.findall(r'<node[^>]*>', xml)
    for i, node in enumerate(nodes[:30]):
        # 提取关键属性
        text = re.search(r'text="([^"]*)"', node)
        resource_id = re.search(r'resource-id="([^"]*)"', node)
        class_name = re.search(r'class="([^"]*)"', node)
        content_desc = re.search(r'content-desc="([^"]*)"', node)
        bounds = re.search(r'bounds="\[(\d+,\d+)\]\[(\d+,\d+)\]"', node)
        clickable = re.search(r'clickable="([^"]*)"', node)

        parts = []
        if text and text.group(1):
            parts.append(f'text="{text.group(1)[:30]}"')
        if resource_id and resource_id.group(1):
            parts.append(f'id="{resource_id.group(1)[-30:]}"')  # 只显示后30字符
        if class_name:
            cls = class_name.group(1)
            # 简化类名
            short_cls = cls.split('.')[-1] if '.' in cls else cls
            parts.append(f'class="{short_cls}"')
        if content_desc and content_desc.group(1):
            parts.append(f'desc="{content_desc.group(1)[:20]}"')
        if bounds:
            parts.append(f'bounds=[{bounds.group(1)}][{bounds.group(2)}]')
        if clickable and clickable.group(1) == "true":
            parts.append('clickable')

        indent = "  " if "ViewGroup" in (class_name.group(1) if class_name else "") else ""
        print(f"{indent}{i+1}. {', '.join(parts) if parts else '(空节点)'}")

    # 展示截断后给 LLM 看的内容
    print("\n[4] 截断后给 LLM 看的内容（最多15000字符）:")
    print("-" * 60)

    MAX_LEN = 15000
    if len(xml) > MAX_LEN:
        truncated = xml[:MAX_LEN]
        last_node = truncated.rfind('</node>')
        if last_node > MAX_LEN * 0.8:
            truncated = truncated[:last_node + 7]
        truncated += "\n<!-- XML 已截断，省略了部分子节点 -->"
        print(f"  截断后长度: {len(truncated)} 字符")
        print(f"  省略了约 {len(xml) - len(truncated)} 字符")
    else:
        truncated = xml
        print(f"  未截断（原长度 {len(xml)} 字符）")

    # 展示截断后的部分内容
    print("\n  截断后的 XML 示例（前100行）:")
    lines = truncated.split('\n')[:100]
    for line in lines:
        print(line)

    # 保存完整控件树到文件
    output_dir = os.path.join(os.path.dirname(__file__), "execution_agent", "output")
    os.makedirs(output_dir, exist_ok=True)

    # 保存原始 XML
    xml_file = os.path.join(output_dir, "demo_hierarchy_raw.xml")
    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"\n[5] 原始控件树已保存: {xml_file}")

    # 保存截断后的 XML
    truncated_file = os.path.join(output_dir, "demo_hierarchy_truncated.xml")
    with open(truncated_file, "w", encoding="utf-8") as f:
        f.write(truncated)
    print(f"  截断后的控件树已保存: {truncated_file}")

    # 截图
    screenshot_file = os.path.join(output_dir, "demo_screenshot.png")
    device.screenshot(screenshot_file)
    print(f"  截图已保存: {screenshot_file}")

    print("\n" + "=" * 60)
    print("  完成！你可以查看上述文件了解控件树结构")
    print("=" * 60)

except Exception as e:
    print(f"\n⚠️ 无法连接设备或获取控件树: {e}")
    print("\n如果你没有连接模拟器，下面展示一个典型控件树的结构示例:")

    # 展示典型控件树结构示例
    print("\n" + "=" * 60)
    print("  典型控件树结构示例（网易云音乐首页）")
    print("=" * 60)

    example_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<hierarchy rotation="0">
  <node index="0" text="" resource-id="" class="android.widget.FrameLayout" package="com.netease.cloudmusic" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][1080,1920]">
    <node index="0" text="" resource-id="" class="android.widget.LinearLayout" package="com.netease.cloudmusic" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][1080,1920]">
      <node index="0" text="" resource-id="android:id/statusBarBackground" class="android.widget.ViewStub" package="com.netease.cloudmusic" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,0][1080,24]"/>
      <node index="1" text="" resource-id="" class="android.widget.FrameLayout" package="com.netease.cloudmusic" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,24][1080,1920]">
        <node index="0" text="" resource-id="com.netease.cloudmusic:id/main_container" class="android.widget.FrameLayout" package="com.netease.cloudmusic" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[0,24][1080,1920]">
          <!-- 搜索框 -->
          <node index="0" text="" resource-id="com.netease.cloudmusic:id/search_bar" class="android.widget.LinearLayout" package="com.netease.cloudmusic" content-desc="搜索" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[20,50][960,100]">
            <node index="0" text="搜索歌曲、歌手、专辑" resource-id="com.netease.cloudmusic:id/search_hint" class="android.widget.TextView" package="com.netease.cloudmusic" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[50,60][400,90]"/>
          </node>
          <!-- 推荐歌曲列表 -->
          <node index="1" text="每日推荐" resource-id="com.netease.cloudmusic:id/daily_recommend_title" class="android.widget.TextView" package="com.netease.cloudmusic" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[20,120][200,150]"/>
          <node index="2" text="夜曲" resource-id="" class="android.widget.TextView" package="com.netease.cloudmusic" content-desc="夜曲 - 周杰伦" checkable="false" checked="false" clickable="true" enabled="true" focusable="true" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[20,160][300,200]">
            <node index="0" text="周杰伦" resource-id="" class="android.widget.TextView" package="com.netease.cloudmusic" content-desc="" checkable="false" checked="false" clickable="false" enabled="true" focusable="false" focused="false" scrollable="false" long-clickable="false" password="false" selected="false" bounds="[20,180][100,200]"/>
          </node>
          <!-- 更多节点... -->
        </node>
      </node>
    </node>
  </node>
</hierarchy>'''

    print("\n原始 XML 格式:")
    print("-" * 60)
    print(example_xml)

    print("\n\n关键属性解释:")
    print("-" * 60)
    print("""
每个 <node> 标签代表一个控件，关键属性：

1. text            - 控件显示的文字内容
                     例: text="搜索歌曲、歌手、专辑" (搜索框提示语)
                     例: text="夜曲" (歌曲名称)

2. resource-id     - 控件的唯一资源ID（最稳定的选择器）
                     例: resource-id="com.netease.cloudmusic:id/search_bar" (搜索框)
                     格式: <包名>:id/<控件名>

3. class           - 控件类型
                     例: class="android.widget.TextView" (文本)
                     例: class="android.widget.EditText" (输入框)
                     例: class="android.widget.Button"    (按钮)
                     例: class="android.widget.ImageView" (图片)

4. content-desc    - 无障碍描述（给视障用户看的）
                     例: content-desc="搜索" (搜索按钮的无障碍标签)
                     例: content-desc="夜曲 - 周杰伦" (歌曲条目的完整描述)

5. bounds          - 控件在屏幕上的坐标范围 [左上角][右下角]
                     例: bounds="[20,50][960,100]" (搜索框占据的区域)
                     格式: [x1,y1][x2,y2]，其中 (x1,y1) 是左上角坐标

6. clickable       - 是否可点击
                     例: clickable="true" (可以点击的控件)
                     例: clickable="false" (不可点击的纯文本)

7. scrollable      - 是否可滚动
                     例: scrollable="true" (列表、滚动区域)

8. package         - 所属App包名
                     例: package="com.netease.cloudmusic" (网易云音乐)
""")

    print("\nLLM 做控件匹配时看到的内容:")
    print("-" * 60)
    print("""
Prompt 会传入：
- step_intent: "在搜索框输入'夜曲'" (用户想做什么)
- hierarchy_xml: 截断后的 XML 控件树 (上面那种格式，最多15000字符)

LLM 需要在 XML 中找到"搜索框"，并返回：
{
  "action": "set_text",
  "target": {
    "text": "搜索歌曲、歌手、专辑",
    "resource_id": "com.netease.cloudmusic:id/search_hint",
    "class": "android.widget.TextView",
    "content_desc": "",
    "bounds": [50, 60, 400, 90]   // 注意：LLM 可能瞎猜bounds
  },
  "input_text": "夜曲",
  "reasoning": "用户要输入搜索词，找到提示语为'搜索歌曲...'的控件，..."
}

执行层拿到这个结果后：
1. 用 resource_id 构建选择器 → device(resourceId="com.netease.cloudmusic:id/search_hint")
2. 执行 set_text("夜曲")
3. 如果选择器失败 → 用 bounds 坐标降级点击 → 点击 (225, 75)
4. 验证页面是否真的变化了
""")